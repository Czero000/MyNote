### 安装依赖包
```
yum -y install gcc gcc-c++ m4 make automake libtool gettext openssl-devel pkgconfig perl-libwww-perl perl-XML-Parser curl curl-devel vsftpd libevent-devel libevent libidn-devel zlib-devel
```

### 下载transmission及必要软件
```
wget http://download-origin.transmissionbt.com/files/transmission-2.84.tar.xz
wget http://ftp.acc.umu.se/pub/gnome/sources/intltool/0.40/intltool-0.40.6.tar.gz
wget http://ftp.gnu.org/gnu/libiconv/libiconv-1.14.tar.gz
wget https://cloud.github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz
```

### 安装软件包
```
tar -zxf intltool-0.40.6.tar.gz 
cd intltool-0.40.6
./configure 
make && make install
 cd ..
tar -zxf libiconv-1.14.tar.gz 
./configure 
make && make install 
echo "/usr/local/lib" >> /etc/ld.so.conf
 ldconfig 
cd ..
tar -zxf libevent-2.0.21-stable.tar.gz 
cd libevent-2.0.21-stable
./configure 
make && make install 
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
cd ..
xz -d transmission-2.84.tar.xz 
tar -xf transmission-2.84.tar 
cd transmission-2.84
./configure --prefix=/usr/local/transmission CFLAGS=-liconv
make && make install 
```
### 配置
```
transmission-daemon -g /usr/local/transmission
killall transmission-daemon
```
以上命令需执行两次

然后就可以进行配置了
```
cat /usr/local/transmission/settings.json
{
    "alt-speed-down": 50,
    "alt-speed-enabled": false,
    "alt-speed-time-begin": 540,
    "alt-speed-time-day": 127,
    "alt-speed-time-enabled": false,
    "alt-speed-time-end": 1020,
    "alt-speed-up": 50,
    "bind-address-ipv4": "0.0.0.0",
    "bind-address-ipv6": "::",
    "blocklist-enabled": true,                
    "blocklist-url": "http://www.example.com/blocklist",
    "cache-size-mb": 4,
    "dht-enabled": true,                 //DHT支持
    "download-dir": "/data/transmission/Downloads",     //下载完成的保存路径
    "encryption": 1,
    "idle-seeding-limit": 30,
    "idle-seeding-limit-enabled": false,
    "incomplete-dir": "/data/transmission/Downloads",     //未下载完成的保存路径
    "incomplete-dir-enabled": false,
    "lazy-bitfield-enabled": true,
    "lpd-enabled": false,
    "message-level": 2,
    "open-file-limit": 32,
    "peer-congestion-algorithm": "",
    "peer-limit-global": 240,                //全局种子最大连接数
    "peer-limit-per-torrent": 60,          //单一种子最大连接数
    "peer-port": 51413,
    "peer-port-random-high": 65535,
    "peer-port-random-low": 49152,
    "peer-port-random-on-start": false,
    "peer-socket-tos": "default",
    "pex-enabled": true,
    "port-forwarding-enabled": true,
    "preallocation": 1,
    "prefetch-enabled": 1,
    "ratio-limit": 2,
    "ratio-limit-enabled": false,
    "rename-partial-files": true,
    "rpc-authentication-required": true,
    "rpc-bind-address": "0.0.0.0",
    "rpc-enabled": true,
    "rpc-password": "{096110376f678fa59ac93b4ba2ef383fba6a9edcBELB4tYF",         //密码
    "rpc-port": 9091,                            //网页GUI使用的端口
    "rpc-url": "/transmission/",
    "rpc-username": "",                   //用户名
    "rpc-whitelist": "*.*.*.*",              
    "rpc-whitelist-enabled": true,
    "script-torrent-done-enabled": false,
    "script-torrent-done-filename": "",
    "speed-limit-down": 100,
    "speed-limit-down-enabled": false,
    "speed-limit-up": 100,
    "speed-limit-up-enabled": false,
    "start-added-torrents": true,
    "trash-original-torrent-files": false,
    "umask": 18,           //这里改为0，可以控制默认下载文件权限为777
    "upload-slots-per-torrent": 14           //每个种子上传连接数
}
```
### 执行`transmission-daemon -g /usr/local/transmission`，通过浏览器登陆`（http://yourIP:9091/）`就可以控制了。

#### yum安装Transmission
以前装在VPS上安装Transmission当Seedbox使大多使用一些一键包，或者使用rpm包的方式安装，一键包的方式我一直不喜欢，经常出问题，而且一般版本都很旧。
rpm包的方式可以参考这篇文章，不过这里的版本也已经很旧了，geekery现在提供更加方便yum repo的方式安装，自动解决依赖问题，版本很新(目前是2.71)，并可通过yum更新。

安装方法非常简单，简单翻译了一下，原文可以参考这里:
```
cd /etc/yum.repos.d/
CentOS 5 x86

wget http://geekery.altervista.org/geekery-el5-i386.repo
CentOS 5 x86_64

wget http://geekery.altervista.org/geekery-el5-x86_64.repo
CentOS 6 x86

wget http://geekery.altervista.org/geekery-el6-i686.repo
CentOS 6 x86_64

wget http://geekery.altervista.org/geekery-el6-x86_64.repo
```
然后:
```
yum install -y transmission transmission-daemon
```
提示导入GPG Key的时候输y同意即可

注意：如果之前通过RPM包的方式安装过Transmission，需要卸载后再用yum安装。
装好后可以通过
```
service transmission-daemon start
```
来启动Transmission

配置文件位于`/var/lib/transmission/.config/transmission-daemon/settings.json(CentOS 5)`
或`/var/lib/transmission/settings.json(CentOS 6)`
修改配置文件前要先用
```
service transmission-daemon stop
```
关掉Transmission，否则配置不会生效。
具体的配置网上有很多，就不详细说了
```
    "rpc-authentication-required": true,
    "rpc-enabled": true,
    "rpc-password": "管理密码密码",
    "rpc-username": "管理用户名",
    "rpc-whitelist-enabled": false,
```
主要是把这几项改成我上面的样子就可以了，然后你就可以通过`http://你的IP地址:9091`的方式连接了。
远程管理建议使用*Transmission-Remote-GUI*
