MegaCli这个命令可以用来监控raid状态、磁盘状况等，最近上了一批ubuntu系统，问题是MegaCli在官网上只有rpm格式的包，没有deb的包，但是还是有办法解决的，rpm包也是可以在debian&&ubuntu上安装的。
 
### 下载最新的zip文件
```
http://www.lsi.com/Search/Pages/results.aspx?k=MegaCLI&r=productfacet%3D%22AQxNZWdhUkFJRCBTQVMMcHJvZHVjdGZhY2V0AQJeIgIiJA%3D%3D%22%20os%3D%22AQVMaW51eAJvcwEBXgEk%22
```
我下载的是8.00.48_Linux_MegaCLI.zip
 
### 预先安装需要的其他包
```
apt-get -y install  rpm2cpio libsysfs2 libsysfs-dev unzip
```
### 安装完成后执行如下命令
```
cd /lib/x86_64-linux-gnu/
ln -s libsysfs.so.2.0.1 libsysfs.so.2.0.2
```
### 进入 8.00.48_Linux_MegaCLI.zip包所在的目录，执行如下命令
``` 
unzip 8.00.48_Linux_MegaCLI.zip
unzip MegaCliLin.zip
rpm2cpio Lib_Utils-1.00-09.noarch.rpm | cpio -idmv
rpm2cpio MegaCli-8.00.48-1.i386.rpm | cpio -idmv
cp opt/MegaRAID/MegaCli/MegaCli64 /sbin/
cp opt/MegaRAID/MegaCli/MegaCli /sbin/
```
MegaCli不但能查询raid的状态，还能设置raid的状态，所以还是由管理员掌握比较好，这样就安装完毕了。
 
下面几个是常用的检查raid状态的命令：
 
* MegaCli64 -LDInfo -Lall -aALL    可以检查raid级别
* MegaCli64 -PDList -aALL    可以检查所有物理盘的状态
* MegaCli64 -AdpAllInfo -aALL    显示所有的raid信息
* MegaCli64  -cfgdsply -aALL     显示所有的磁盘信息
* MegaCli64 -FwTermLog -Dsply -aALL    这个包含一些用于的日志
* MegaCli的其他强大功能还请查看官方文档。
