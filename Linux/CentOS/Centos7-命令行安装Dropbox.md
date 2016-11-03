Dropbox 这货也被Q了，想要使用需要搭梯子，可以参照Shadowsocks安装，搭建一个梯子。

Dropbox 守护程序可在所有 32 位与 64 位 Linux 服务器上正常运行。若要安装，请在 Linux 终端运行下列命令。

### 下载Dropbox
访问[官方下载页面](https://www.dropbox.com/install?os=lnx)根据不同平台，选择下载不同的安装包

### 安装Dropbox
我的操作系统是CentOS，选择下载RPM包来安装
```
https://linux.dropbox.com/packages/fedora/nautilus-dropbox-2015.02.12-1.fedora.x86_64.rpm
yum localinstall nautilus-dropbox-2015.02.12-1.fedora.x86_64.rpm
```
### 启动Dropbox
```
dropbox start
Starting Dropbox...
The Dropbox daemon is not installed!
Run "dropbox start -i" to install the daemon
```
执行
```
dropbox start -i
Starting Dropbox...
Dropbox is the easiest way to share and store your files online. Want to learn more? Head to https://www.dropbox.com/

In order to use Dropbox, you must download the proprietary daemon. [y/n] y
Downloading Dropbox... 100%
Unpacking Dropbox... 100%
Done!
```
启动Dropbox
```
dropbox start
Dropbox is already running!
```

### 配置Dropbox
执行命令
```
~/.dropbox-dist/dropboxd

This computer isn't linked to any Dropbox account...
Please visit https://www.dropbox.com/cli_link_nonce?nonce=94f031bb1e619bda13898fd5e9c8a44e to link this device.
```
用另外一个终端``lynx https://www.dropbox.com/cli_link_nonce?nonce=94f031bb1e619bda13898fd5e9c8a44e``
这样就完成了

下载官方工具
```
wget "http://www.dropbox.com/download?dl=packages/dropbox.py"
chmod 755 dropbox.py
./dropbox.py help (或是 start, stop等指令, 预设位置为~/Dropbox)
```
