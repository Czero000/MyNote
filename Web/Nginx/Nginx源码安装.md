# 环境介绍
nginx已经在工作中大量使用，但是之前并没有及时总结，每次都是从网上找配置在更改为自己需要的，先在整理一份安装、配置文档，包括http、https、负载均衡、反向代理、缓存等不同应用环境

## 系统版本
系统环境默认采用`CentOS Linux release 7.1.1503 (Core)`，
部分使用 `Ubuntu-16.04 LTS`

## 软件获取

官方网站：[http://nginx.org](http://nginx.org)
最新稳定版本：[nginx-1.8.1.tar.gz](http://nginx.org/download/nginx-1.8.1.tar.gz)
帮助文档：[http://nginx.org/en/docs](http://nginx.org/en/docs)
编译参数说明：[http://nginx.org/en/docs/configure.html](http://nginx.org/en/docs/configure.html)

## 软件仓库

- CentOS

yum仓库包含`centos`官方和`epel`两个安装源
```
rpm -ivh http://mirrors.yun-idc.com/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
```
- Ubuntu
使用官方源即可

# Nginx安装 #

## CentOS

### 安装依赖软件

1. CentOS

```
yum install gcc gcc-c++ make autoconf pcre pcre-devel openssl openssl-devel zlib-devel -y
```

2. Ubuntu
```
apt install gcc g++ make autoconf libpcre3 libpcre3-dev zlib1g-dev openssl libssl-dev build-essential
```

- 安装pcre，使nginx支持rewrite功能
- 安装openssl，ssl支持
- 安装zlib，使nginx支持页面压缩
- 以上软件包也可以通过源码安装

### 安装nginx ###

```
tar -zxf nginx-1.8.1.tar.gz 
cd nginx-1.8.1/
./configure --prefix=/usr/local/nginx --with-http_ssl_module  --with-http_stub_status_module --with-pcre --with-http_gzip_static_module
make && make install 
```

参数解释

```
--with-http_ssl_module            ---支持https
--with-http_stub_status_module    ---支持nginx状态查询
--with-http_gzip_static_module    ---支持页面压缩
--with-pcre                       ---支持rewrite
```

#n ginx启动、停止、重启

## 启动
现在nginx就可以启动，不需要更改任何配置文件。

```
\\-c参数指定了配置文件的路径，如果不加-c，nginx就会默认加载其安装目录下面的conf目录下面的nginx.conf文件
/usr/local/nginx/sbin/nginx 
```
## 停止

```
/usr/local/nginx/sbin/nginx -s stop[quit,reopen,reload]
```
Nginx的停止命令有很多，一般都是通过发送系统信号给nginx的主进程来停止nginx,例如：
```
\\停止nginx
kill –QUIT `主进程号`
kill -QUIT `cat /usr/local/nginx/logs/nginx.pid`
 
\\快速停止nginx
kill –TERM `主进程号`
kill –TERM `cat /usr/local/nginx/logs/nginx.pid`

kill –INT `主进程号`
kill –INT`cat /usr/local/nginx/logs/nginx.pid`

\\强制停止nginx
Kill -9 nginx
```

## 重启

```
/usr/local/nginx/sbin/nginx -s reload[stop,quit,reopen]
```
同样可以通过信号来重启nginx
```
Kill –HUB `主进程号`
kill –HUB `cat /usr/local/nginx/logs/nginx.pid`
```

## init脚本

```
#! /bin/bash
#
# nginx   Start up the nginx server daemon
#
# chkconfig: 2345 55 25
# Description: starts and stops the nginx web server
#
### BEGIN INIT INFO
# Provides:       nginx
# Required-Start:      $all
# Required-Stop:      $all
# Default-Start:        2 3 4 5
# Default-Stop:        0 1 6
# Description:         starts and stops the nginx web server
### END INIT INFO

# To install:
#   copy this file to /etc/init.d/nginx
#   shell> chkconfig –add nginx (RedHat)
#   shell> update-rc.d -f nginx defaults (debian)

# To uninstall:
#   shell> chkconfig –del nginx (RedHat)
#   shell> update-rc.d -f nginx remove

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
NAME=nginx
DAEMON=/usr/local/nginx/$NAME
CONFIGFILE=/usr/local/nginx/$NAME.conf
PIDFILE=/var/run/$NAME.pid
ULIMIT=10240

set -e
[ -x “$DAEMON” ] || exit 0

do_start() {
   echo “Starting $NAME …”
   ulimit -SHn $ULIMIT
   $DAEMON -c $CONFIGFILE
}

do_stop() {
   echo “Shutting down $NAME …”
   kill `cat $PIDFILE`
}

do_reload() {
   echo “Reloading $NAME …”
   kill -HUP `cat $PIDFILE`
}

case “$1” in
   start)
     [ ! -f “$PIDFILE” ] && do_start || echo “nginx already running”
  echo -e “.\ndone”
     ;;
   stop)
    [ -f “$PIDFILE” ] && do_stop || echo “nginx not running”
  echo -e “.\ndone”
     ;;
  restart)
  [ -f “$PIDFILE” ] && do_stop || echo “nginx not running”
     do_start
  echo -e “.\ndone”
     ;;
  reload)
   [ -f “$PIDFILE” ] && do_reload || echo “nginx not running”
  echo -e “.\ndone”
     ;;
    *)
    N=/etc/init.d/$NAME
    echo “Usage: $N {start|stop|restart|reload}” >&2
    exit 1
    ;;
esac

exit 0
```
