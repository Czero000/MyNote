随之服务器系统从CentOS5.x逐步升级到CentOS6.x，发现原来熟悉的eth0、eth1全部变成了em1、em2。接口名变化并不会对平时的运维工作有影响，不过某些应用可能会收到影响，所以还是改过来，比较好。
经过资料整理，有两种方式：

### 更改配置文件
dmesg中看到如下一行信息：`kernel: udev: renamed network interface eth0 to em1`

原来是udev这个设备管理进程在开机过程中将系统默认的eth0改名为em1了，其实em1对应的就是系统原本的eth0网卡；由于我在mini安装过程中没有对网络进行配置，所以系统默认没有将网卡激活导致ifconfig看不到任何网卡；只需要在`/etc/sysconfig/network-scripts/ifcfg-em1`中将参数`ONBOOT=no`改为yes，然后`service network restart` 网卡em1就出现了！

总觉得Linux的网卡代号变成了em1不习惯，想还原为一直以来熟悉的eth0也是可以的，调整udev的网卡命名规则配置文件`/etc/udev/rules.d/70-persistent-net.rules`,将文件中em2 替换为eth1，em1替换为eth0，这样系统就会把网卡命名还原回来，还要把网卡配置文件中的设备名改回来。重启系统，这样熟悉的eth0、eth1就回来了

### 修改系统grub

* 增加biosdevname=0 启动参数

```
     kernel /vmlinuz-2.6.32-431.el6.i686 ro root=UUID=84316edf-b537-486c-bf2e-616aa51ede2f rd_NO_LUKS rd_NO_L

VM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM biosdevname=0 rhgb quiet
```

* 删除udev的配置文件 
```
rm -f /etc/udev/rules.d/70-persistent-net.rules
```

* 重命名当前网卡配置文件
````
mv ifcfg-em1 ifcfg-eth0
```

* 修改网卡配置文件内容，将em1替换为eth0


重启服务器，这样熟悉的eth0、eth1就回来了
 
