### Cobbler介绍
Cobbler是一个快速网络安装linux的服务，而且在经过调整也可以支持安装windows。该工具使用python开发，小巧轻便，使用简单的命令即可完成PXE网络安装环境的配置，同时还可以管>理DHCP、DNS，以及yum包镜像。Cobbler支持命令行管理、web界面管理，还提供了API接口，方便二次开发。和kickstart不同的是，使用Cobbler不会因为在局域网中启用DHCP而导致有些机器
因为默认从PXE启动在重启服务器后加载tftp内容导致启动终止.

### 系统环境准备

#### 系统环境
CentOS release 6.5 (Final) x86_64

#### 软件包
软件包采用yum 安装方式，yum源采用自建的yum源

### 安装Cobbler

#### 安装cobbler相关软件包
```
yum install -y cobbler cobbler-web pykickstart fence-agents
```

#### 安装debmirror（需要用debmirror来下载ubuntu源，用于本地安装）
```
yum install -y debmirror
```

### 配置Cobbler
#### 设置tftp服务和rsync服务
```
sed -i '/disable/c\\tdisable\t\t\t= no' /etc/xinetd.d/tftp
sed -i -e 's/\=\ yes/\=\ no/g' /etc/xinetd.d/rsync 
/etc/init.d/xinetd restart
chkconfig --level 3 xinetd on 
```

#### 设置Web登录
```
sed -i 's/authn_denyall/authn_configfile/g' /etc/cobbler/modules.conf 
```
之前版本都是需要更改认证设置，但是2.6版本默认就是这样设置

#### 设置Cobbler Web登录用户登录密码
```
htdigest /etc/cobbler/users.digest "Cobbler" cobbler
Changing password for user cobbler in realm Cobbler
New password: 
Re-type new password: 
```

#### 设置Cobbler登录服务器地址
```
sed -i '/^server: /s/server: 127.0.0.1/server: 10.10.3.64/g' /etc/cobbler/settings 
```

####  ks脚本关闭pxe，这样就不会重复安装
  pxe_just_once预防由于服务器设置从网络引导，导致循环安装，激活此设置，机器会告诉Cobbler安装也完成。Cobbler会将对象的netboot标志改为false，这会强制服务器从本地引导。
```
sed -i 's/pxe_just_once: 0/pxe_just_once: 1/g' /etc/cobbler/settings 
```

#### 设置TFTP服务器IP地址
```
sed -i 's/next_server: 127.0.0.1/next_server: 10.10.3.64/g' /etc/cobbler/settings
```

#### 设置Cobbler管理rsync
```
sed -i 's/manage_rsync: 0/manage_rsync: 1/g' /etc/cobbler/settings 
```

#### 设置Cobbler管理DHCP
```
sed -i 's/manage_dhcp: 0/manage_dhcp: 1/g' /etc/cobbler/settings 
```
DHCP服务由Cobbler来管理， /etc/cobbler/dhcp.template.
```
ddns-update-style interim;

allow booting;
allow bootp;

ignore client-updates;
set vendorclass = option vendor-class-identifier;

option pxe-system-type code 93 = unsigned integer 16;

subnet 10.10.3.0 netmask 255.255.255.0 {
     option routers             10.10.3.64;
     option domain-name-servers 10.10.3.64;
     option subnet-mask         255.255.255.0;
     range dynamic-bootp        10.10.3.168 10.10.3.191;
     default-lease-time         21600;
     max-lease-time             43200;
     next-server                $next_server;
     class "pxeclients" {
          match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
          if option pxe-system-type = 00:02 {
                  filename "ia64/elilo.efi";
          } else if option pxe-system-type = 00:06 {
                  filename "grub/grub-x86.efi";
          } else if option pxe-system-type = 00:07 {
                  filename "grub/grub-x86_64.efi";
          } else {
                  filename "pxelinux.0";
          }
     }

}
```

#### 设置Cobbler管理DNS（可选）
```
sed -i 's/manage_dns: 0/manage_dns: 1/g' /etc/cobbler/settings  
```

#### 设置root默认密码
这个设置只对CentOS/RHEL有效
```
openssl passwd -1 -salt 'random-phrase-here' 'your-password-here'
```
修改`/etc/cobbler/settings`
```
default_password_crypted: "$1$mF86/UHC$WvcIcX2t6crBz2onWxyac."
```

#### 启动相关服务
```
/etc/init.d/cobblerd start
/etc/init.d/httpd start
chkconfig httpd on
chkconfig cobblerd on
```

#### 设置debmirror
```
sed -i -e 's/@dists=/#@dists=/g' /etc/debmirror.conf
sed -i -e 's/@arches=/#@arches=/g' /etc/debmirror.conf  
```

#### 开启动态更新
```
sed -i 's/allow_dynamic_settings: 0/allow_dynamic_settings: 1/g' /etc/cobbler/settings 
```

#### 下载启动菜单
```
cobbler get-loaders
```

#### 检查Cobbler "cobbler check"
Cobbler提供了一个检查工具，检查你的设置，有问题会提示给你。按照提示去修复问题
```
cobbler check      
No configuration problems found.  All systems go.
```

#### 命令行查看、修改*setting*文件
```
cobbler setting report      
allow_duplicate_hostnames               : 0
allow_duplicate_ips                     : 0
allow_duplicate_macs                    : 0
allow_dynamic_settings                  : 1
always_write_dhcp_entries               : 0
anamon_enabled                          : 0
auth_token_expiration                   : 3600
authn_pam_service                       : login
bind_chroot_path                        : 
bind_master                             : 127.0.0.1
build_reporting_email                   : ['root@localhost']
build_reporting_enabled                 : 0
build_reporting_ignorelist              : ['']
build_reporting_sender                  : 
build_reporting_smtp_server             : localhost
build_reporting_subject                 : 
build_reporting_to_address              : 
buildisodir                             : /var/cache/cobbler/buildiso
cheetah_import_whitelist                : ['random', 're', 'time']
client_use_https                        : 0
client_use_localhost                    : 0
cobbler_master                          : 
consoles                                : /var/consoles
createrepo_flags                        : -c cache -s sha
default_deployment_method               : ssh
default_kickstart                       : /var/lib/cobbler/kickstarts/default.ks
default_name_servers                    : []
default_name_servers_search             : []
default_ownership                       : ['admin']
default_password_crypted                : $1$7NQM/hse$Uh9IBVPme4E1E3dTo3kH/1
default_template_type                   : cheetah
default_virt_bridge                     : xenbr0
default_virt_disk_driver                : raw
default_virt_file_size                  : 5
default_virt_ram                        : 512
default_virt_type                       : xenpv
enable_gpxe                             : 0
enable_menu                             : 1
func_auto_setup                         : 0
func_master                             : overlord.example.org
http_port                               : 80
isc_set_host_name                       : 0
iso_template_dir                        : /etc/cobbler/iso
kerberos_realm                          : EXAMPLE.COM
kernel_options                          : {'ksdevice': 'eth1', 'lang': ' ', 'text': '~'}
kernel_options_s390x                    : {'vnc': '~', 'ip': False, 'RUNKS': 1, 'ramdisk_size': 40000, 'ro': '~', 'root': '/dev/ram0'}
ldap_anonymous_bind                     : 1
ldap_base_dn                            : DC=example,DC=com
ldap_management_default_type            : authconfig
ldap_port                               : 389
ldap_search_bind_dn                     : 
ldap_search_passwd                      : 
ldap_search_prefix                      : uid=
ldap_server                             : ldap.example.com
ldap_tls                                : 1
ldap_tls_cacertfile                     : 
ldap_tls_certfile                       : 
ldap_tls_keyfile                        : 
manage_dhcp                             : 1
manage_dns                              : 0
manage_forward_zones                    : []
manage_reverse_zones                    : []
manage_rsync                            : 1
manage_tftp                             : 1
manage_tftpd                            : 1
mgmt_classes                            : []
mgmt_parameters                         : {'from_cobbler': 1}
next_server                             : 10.10.3.64
power_management_default_type           : ipmitool
power_template_dir                      : /etc/cobbler/power
puppet_auto_setup                       : 0
puppet_parameterized_classes            : 1
puppet_server                           : puppet
puppet_version                          : 2
puppetca_path                           : /usr/bin/puppet
pxe_just_once                           : 1
pxe_template_dir                        : /etc/cobbler/pxe
redhat_management_key                   : 
redhat_management_permissive            : 0
redhat_management_server                : xmlrpc.rhn.redhat.com
redhat_management_type                  : off
register_new_installs                   : 0
remove_old_puppet_certs_automatically   : 0
replicate_repo_rsync_options            : -avzH
replicate_rsync_options                 : -avzH
reposync_flags                          : -l -n -d
restart_dhcp                            : 1
restart_dns                             : 1
restart_xinetd                          : 1
run_install_triggers                    : 1
scm_track_enabled                       : 0
scm_track_mode                          : git
serializer_pretty_json                  : 0
server                                  : 10.10.3.64
sign_puppet_certs_automatically         : 0
signature_path                          : /var/lib/cobbler/distro_signatures.json
signature_url                           : http://www.cobblerd.org/signatures/latest.json
snippetsdir                             : /var/lib/cobbler/snippets
template_remote_kickstarts              : 0
virt_auto_boot                          : 1
webdir                                  : /var/www/cobbler
xmlrpc_port                             : 25151
yum_distro_priority                     : 1
yum_post_install_mirror                 : 1
yumdownloader_flags                     : --resolv
```
通过命令行编辑setting
```
cobbler setting edit --name=option --value=value
```

### Web登录

访问*http://10.10.3.64/cobbler_web*用户密码就是上面设置的

* Cobbler的使用，主要集中在Web界面的几个菜单里：
* Distros：这个其实就是发行版，类似CentOS、Ubuntu、SUSE。CenOS6.2和Centos6.5，是不同的Distros
* Porfiles：针对Distors设置的，一个Distros可以对应多个Profiles，包括不同的kickstart文件。
* Systems：针对每个节点，可以指定节点IP地址，DNS、还有就是ipmi的用户和密码，实现远程开机关机。这个是个重点，对机器的操作可以全部在System的菜单里实现。System可以指定节点使用那个Profile
* Repos：针对Redhat和CentOS，可以管理源，并且这些源可以在profile里面添加。对ubuntu的源，只能在kickstart脚本里指定
* Images：针对不能pxe的服务器，采用ISO启动
* Kickstart Templates：Cobbler内置了几个KS文件模版，导入一个Distros，Cobbler 会默认关联一个KS文件。不需要任何设置，就可以把os自动安装完毕
* Snippets：这个是Cobbler的精华。一些常用的设置，写成一个模块，让ks文件来调用，方便灵活。例如CentOS网络固定IP地址的设置，就是通过这里来实现

### 设置Apache根目录访问
希望直接访问ip地址，就可以看到源的目录，尤其对与ubuntu来说，这样这样看起来更加规范
```
cat /etc/httpd/conf.d/welcome.conf 
# 
# This configuration file enables the default "Welcome"
# page if there is no default index page present for
# the root URL.  To disable the Welcome page, comment
# out all the lines below.
#

    <LocationMatch "^/+$">
    Options Indexes FollowSymLinks
        Order allow,deny
        Allow from all
    </LocationMatch>

```
重启apache，登录http://10.10.3.64看到的目录，实际就是/var/www/html

### 安装常见问题

#### 校验cobbler check出错
```
cobbler check
Traceback (most recent call last):
  File "/usr/bin/cobbler", line 36, in 
    sys.exit(app.main())
  File "/usr/lib/python2.6/site-packages/cobbler/cli.py", line 655, in main
    rc = cli.run(sys.argv)
  File "/usr/lib/python2.6/site-packages/cobbler/cli.py", line 270, in run
    self.token         = self.remote.login("", self.shared_secret)
  File "/usr/lib/python2.6/xmlrpclib.py", line 1199, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.6/xmlrpclib.py", line 1489, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.6/xmlrpclib.py", line 1253, in request
    return self._parse_response(h.getfile(), sock)
  File "/usr/lib/python2.6/xmlrpclib.py", line 1392, in _parse_response
    return u.close()
  File "/usr/lib/python2.6/xmlrpclib.py", line 838, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: :'login failed'">
```
解决方法：此为BUG，按照下面方法即可
```
etc/init.d/cobblerd restart
cobbler get-loaders
```
