### 查看当前系统内核
```
uname -r
2.6.32-431.el6.x86_64
```
### 下载linux内核包
```
wget https://www.kernel.org/pub/linux/kernel/v3.0/linux-3.18.20.tar.gz
tar -zxf linux-3.18.20.tar.gz 
cd linux-3.18.20
```
### 配置内核并安装
```
make mrproper  //清除环境变量，清除配置文件
cp /boot/config-2.6.32-431.el6.x86_64 .config  //复制原有系统的内核配置文件
make oldconfig  //读取当前目录下的.config文件，在.config文件里没有找到的选项则提示用户填写 sh -c 'yes "" | make oldconfig'
make menuconfig  //在菜单模式下选择需要编译的内核模块（未选择此类型）
make clean //确保所有都是最新状态
make bzImage //生成内核文件
make modules //编译模块
make modules_install //安装模块
```
### 修改grub引导，重启服务器
修改grub引导顺序，让新安装的内核作为默认内核，新安装的内核在第一位置，所以default=0
```
cat /boot/grub/grub.conf 
# grub.conf generated by anaconda
#
# Note that you do not have to rerun grub after making changes to this file
# NOTICE:  You have a /boot partition.  This means that
#          all kernel and initrd paths are relative to /boot/, eg.
#          root (hd0,0)
#          kernel /vmlinuz-version ro root=/dev/sda5
#          initrd /initrd-[generic-]version.img
#boot=/dev/sda
default=0
timeout=5
splashimage=(hd0,0)/grub/splash.xpm.gz
hiddenmenu
title CentOS (3.18.20)
        root (hd0,0)
        kernel /vmlinuz-3.18.20 ro root=UUID=0303a1aa-552b-4de9-ac52-6bc95361d832 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
        initrd /initramfs-3.18.20.img
title CentOS (2.6.32-431.el6.x86_64)
        root (hd0,0)
        kernel /vmlinuz-2.6.32-431.el6.x86_64 ro root=UUID=304a1aa-552b-4de9-ac52-6bc95361d832 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
        initrd /initramfs-2.6.32-431.el6.x86_64.img
```
### 重启系统
```
reboot
```

### 确认当前内核版本
```
uname -r
3.18.20
```
