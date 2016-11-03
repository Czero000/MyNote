本篇接上篇文章，继续介绍cobbler的使用方法。
### RedHat/CentOS

#### 导入CentOS6.5 ISO镜像
```
mount -t auto -o loop CentOS-6.5-x86_64-bin-DVD1.iso /mnt/
```
导入ISO镜像
由于CentOS镜像信息较多，所以导入的时候，会同时创建distro，profile，并且还会设置repo，不过这个repo只包含DVD1，如果想要包含DVD2，还需要做设置。
```
cobbler import --path=/mnt --name=CentOS6.5 --arch=x86_64
task started: 2014-11-19_175649_import
task started (id=Media import, time=Wed Nov 19 17:56:49 2014)
Found a candidate signature: breed=redhat, version=rhel6
Found a matching signature: breed=redhat, version=rhel6
Adding distros from path /var/www/cobbler/ks_mirror/CenOS6.5-x86_64:
creating new distro: CenOS6.5-x86_64
trying symlink: /var/www/cobbler/ks_mirror/CenOS6.5-x86_64 -> /var/www/cobbler/links/CenOS6.5-x86_64
creating new profile: CenOS6.5-x86_64
associating repos
checking for rsync repo(s)
checking for rhn repo(s)
checking for yum repo(s)
starting descent into /var/www/cobbler/ks_mirror/CenOS6.5-x86_64 for CenOS6.5-x86_64
processing repo at : /var/www/cobbler/ks_mirror/CenOS6.5-x86_64
need to process repo/comps: /var/www/cobbler/ks_mirror/CenOS6.5-x86_64
looking for /var/www/cobbler/ks_mirror/CenOS6.5-x86_64/repodata/*comps*.xml
Keeping repodata as-is :/var/www/cobbler/ks_mirror/CenOS6.5-x86_64/repodata
*** TASK COMPLETE ***
```

#### 在*profile*文件中设置*Kickstart*文件

*profile*文件中默认采用*/var/lib/cobbler/kickstarts/sample.ks*作为ks文件。可以指定自己之前的ks文件也可以改这个文件来用
修改profile文件中ks可以用几种方法：

* 直接修改profile文件
```
vim /var/lib/cobbler/config/profiles.d/CentOS6.5-x86_64.json 
```

* 通过命令行修改profile文件
```
cobbler profile edit --name=CentOS6.5-x86_64 --kickstart=/data/htdocs/kscfg/ks.cfg-CentOS6.5-x86_64
```

* 通过Web界面修改profile文件
![cobbler-profile](http://ofc9x1ccn.bkt.clouddn.com/cobbler/cobbler-profile.png)

修改之后，可以通过下面命令来查看自己修改的信息
```
cobbler profile report    
Name                           : CentOS6.5-x86_64
TFTP Boot Files                : {}
Comment                        : 
DHCP Tag                       : default
Distribution                   : CentOS6.5-x86_64
Enable gPXE?                   : 0
Enable PXE Menu?               : 1
Fetchable Files                : {}
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart                      : /data/htdocs/kscfg/ks.cfg-CentOS6.5-x86_64
Kickstart Metadata             : {}
Management Classes             : []
Management Parameters          :  <>
Name Servers                   : []
Name Servers Search Path       : []
Owners                         : ['admin']
Parent Profile                 : 
Proxy                          : 
Red Hat Management Key         :  <>
Red Hat Management Server      :  <>
Repos                          : []
Server Override                :  <>
Template Files                 : {}
Virt Auto Boot                 : 1
Virt Bridge                    : xenbr0
Virt CPUs                      : 1
Virt Disk Driver Type          : raw
Virt File Size(GB)             : 5
Virt Path                      : 
Virt RAM (MB)                  : 512
Virt Type                      : kvm
```

#### 添加一个System

IPMI地址为10.10.3.157  user：root    pass：superuser

```
cobbler system add \
> --name=ssq-54-157 \
> --hostname=ssq-54-157 \
> --dns-name=ssq-54-157 \
> --profile=CentOS6.5-x86_64 \
> --interface=eth1 \
> --mac=00:E0:81:B9:5A:B6 \
> --ip-address=172.16.6.157 \
> --netmask=255.255.255.0 \
> --static=1 \
> --power-type=ipmilan \
> --power-user=root \
> --power-pass=superuser \
> --power-address=10.10.3.157
```
由于Cobbler不能支持同时配置两块网卡，所以要分为两步。

```
cobbler system edit --name=ssq-54-157 --interface=eth0 --mac=00:e0:81:b9:5a:b5 --ip-address=10.10.54.157 --netmask=255.255.255.0 --static=1 --gateway=10.10.54.1
```

这些都可以在Web中完成，只不过比较繁琐，还是命令行更加方便
Cobbler所有设置和修改，都需要通过cobbler sync 来生效，让我们查看以下刚才添加的System
```
cobbler system report --name=ssq-54-157
```
需要留意的一个参数是：netboot-enabled，当Cobbler安装完OS后，这个参数就换自动变为0，如果希望重新安装，就需要变成1
```
cobbler system edit --name=ssq-54-157 --netboot-enabled=ture
```

安装客户端：
设置远程机器有pxe启动：
```
ipmitool -H 10.10.3.157 -Uroot -Psuperuser chassis bootdev pxe
```
重启远程服务器，可以有两种方法：
```
ipmitool -H 10.10.3.157 -Uroot -Psuperuser power reset

cobbler system reboot --name=ssq-54-157 
task started: 2014-11-20_142114_power
task started (id=Power management (reboot), time=Thu Nov 20 14:21:14 2014)
cobbler power configuration is:
      type   : ipmilan
      address: 10.10.3.157
      user   : root
      id     : 
running: /usr/sbin/fence_ipmilan
received on stdout: Powering off machine @ IPMI:10.10.3.157...Done
received on stderr: 
cobbler power configuration is:
      type   : ipmilan
      address: 10.10.3.157
      user   : root
      id     : 
running: /usr/sbin/fence_ipmilan
received on stdout: Powering on machine @ IPMI:10.10.3.157...Done
received on stderr: 
*** TASK COMPLETE ***
```
#### 添加epel源到Cobbler

命令行如下操作，添加epel和epel-test的repo源
```
cobbler repo add --mirror=http://mirrors.yun-idc.com/epel/6Server/x86_64/ --name=epel6-x86_64 --breed=yum
cobbler repo add --mirror=http://mirrors.sohu.com/fedora-epel/testing/6/x86_64/ --name=epel6-x86_64-testing --breed=yum
cobbler repo add --mirror=http://172.16.8.32/centos/6/os/x86_64/Packages/ --name=Local_CentOS6.5_x86_64  --breed=yum
```

这个只对CentOS有效，如果把repo加到profile中，他会自动添加到节点的repo上，指向内网非常方便
```
cobbler profile edit --name=CentOS6.5-x86_64 --repos="epel6-x86_64 epel6-x86_64-testing"
```


#### 通过koan重装系统

重新安装节点的系统，可以在Cobbler上设置，无论是在Web还是命令行，其实还有一种选择，就是直接在节点上进行

koan：Kickstart Over A Network。就可以实现这个

```
yum install -y koan
```
koan命令的使用方法，非常简单可以查看man文档
```
koan --server=10.10.3.64 --list=systems
- looking for Cobbler at http://10.10.3.64/cobbler_api
ssq-54-157
```
当然还可以看其他信息，***Systems***、***Profiles***
```
koan --server=10.10.3.64 --display --system=ssq-54-157
- looking for Cobbler at http://10.10.3.64/cobbler_api
- reading URL: http://10.10.3.64/cblr/svc/op/ks/system/ssq-54-157
install_tree: http://10.10.3.64/cblr/links/CentOS6.5-x86_64
                name  : ssq-54-157
              distro  : CentOS6.5-x86_64
             profile  : CentOS6.5-x86_64
           kickstart  : http://10.10.3.64/cblr/svc/op/ks/system/ssq-54-157
             ks_meta  : tree=http://@@http_server@@/cblr/links/CentOS6.5-x86_64 
        install_tree  : http://10.10.3.64/cblr/links/CentOS6.5-x86_64
              kernel  : /var/www/cobbler/ks_mirror/CentOS6.5-x86_64/images/pxeboot/vmlinuz
              initrd  : /var/www/cobbler/ks_mirror/CentOS6.5-x86_64/images/pxeboot/initrd.img
     netboot_enabled  : False
      kernel_options  : ks=http://10.10.3.64/cblr/svc/op/ks/system/ssq-54-157 ksdevice=eth1 kssendmac lang= text 
               repos  : epel6-x86_64
            virt_ram  : 512
           virt_type  : xenpv
           virt_path  : 
      virt_auto_boot  : 0
```
重装系统就可以使用下面命令，当然也可以指定*Profil*
```
koan --server=10.10.3.64 --system=ssq-54-157 --replace-self
```
这个时候，重启系统，不需要指定PXE启动，他就会自动安装系统。
