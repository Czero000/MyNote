### rsync的优点和缺点

  与传统的cp、tar备份方式相比，rsync具有安全性高、备份迅速、支持赠礼备份等优点，通过rsync可以解决实时性能不高的数据备份需求，例如定期的备份文件到异地服务器，对本地磁盘做数据镜像等。
  随着对数据安全性和可靠性的更高要求，rsync也逐渐暴露出不足。首先rsync同步数据时，需要扫描所有文件后进行比对，进行差量传输。如果数据达到百万或者是千万的量级，扫描文件将耗费大量事件，而发生变化的往往是其中极少的一部分，这是非常低效的方式，其次rsync不能实时去监测、同步数据，虽然可以通过守护进程方式或者是crontab等方式进行触发，但是动作会有一定的时间差，这会导致两地数据可能会出现不一致，无法保证数据或者应用的安全性。

### inotify简介

  Inotify 是一种强大的、细粒度的、异步的文件系统事件监控机制，linux内核从2.6.13起，加入了Inotify支持，通过Inotify可以监控文件系统中添加、删除，修改、移动等各种细微事件，利用这个内核接口，第三方软件就可以监控文件系统下文件的各种变化情况，而inotify-tools就是这样的一个第三方软件。rsync可以实现触发式的文件同步，但是通过crontab守护进程方式进行触发，同步的数据和实际数据会有差异，而inotify可以监控文件系统的各种变化，当文件有任何变动时，就触发rsync同步，这样刚好解决了同步数据的实时性问题。
 
### 安装inotfiy工具inotifytools
  由于inotofy需要Linux内核的支持，在安装inotify-tools前要先确认系统内核师傅支持，如果Linux内核低于2.6.13版本，就需要重启编译内核加入inotify的支持，如何知道你的Linux内核是否支持Inotify机制呢，执行下面命令：
```
grep INOTIFY_USER /boot/config-$(uname -r)
CONFIG_INOTIFY_USER=y
如果输出“CONFIG_INOTIFY_USER=y”，那么就可以享受Inotify之旅了。
```
#### 软件下载地址
官方地址：https://github.com/rvoicilas/inotify-tools/wiki

#### 下载安装软件包
```
wget --no-check-certificate https://github.com/downloads/rvoicilas/inotify-tools/inotify-tools-3.14.tar.gz
tar -zxf inotify-tools-3.14.tar.gz 
cd inotify-tools-3.14
./configure --prefix=/usr/local/inotify
make && make install 
```

### 配置rsync、inotify

#### 系统环境
CentOS_5.4_i386
更新服务器：172.16.6.100
目标服务器：172.16.6.98

#### 配置目标服务器
##### 检查rsync是否安装
如果没有安装可以源码安装或者`yum -y install rsync`，rsync3.0相对与2.0有很多的改进，3.0是边对边边同步，2.0是完全对比之后在同步。
```
rpm -qa rsync
rsync-2.6.8-3.1
```

##### 定义rsync配置文件/etc/rsyncd.conf
```
cat >> /etc/rsyncd.conf <uid=nobody 
gid=nobody
use chroot = no 
max connections = 100
timeout = 600
pid file = /var/run/rsyncd.pid
lock file = /var/run/rsyncd.lock
log file = /var/log/rsyncd.log
secrets file = /etc/rsyncd.passwd
hosts allow = 172.16.6.100
[website]
path = /data/website/
comment = Web Site
read only = no
ignore errors
list = no
auth users = website
EOF
```

##### 配置rsync密码文件，修改密码文件权限，是其他用户无权查看
```
cat >> /etc/rsyncd.passwd << EOF
website:website
EOF
chmod 600 /etc/rsyncd.passwd
```

##### 启动服务
```
/usr/bin/rsync --daemon --config=/etc/rsyncd.conf 
lsof -i:873
COMMAND   PID USER   FD   TYPE     DEVICE SIZE NODE NAME
rsync   25469 root    3u  IPv6 1038838496       TCP *:rsync (LISTEN)
rsync   25469 root    5u  IPv4 1038838497       TCP *:rsync (LISTEN)
```

##### 客户端测试，同步代码
```
rsync -vzrtopg --progress website@172.16.6.98::website --password-file=/etc/rsync.passwd /data/website/
sent 26731 bytes  received 6831971 bytes  4572468.00 bytes/sec
total size is 19027624  speedup is 2.77
```

##### 同步脚本
```
#!/bin/bash
inotifywait='/usr/local/inotify/bin/inotifywait'
LOCAL=172.16.6.98
SRC=/data/website/
USER=website
COMMAND=/usr/bin/rsync 
Option="-vzrtopg --progress --delete" 
Module=website
PASSFILE=/etc/rsync.passwd
$inotifywait -mrq --timefmt '%y-%m-%d %H:%M' --format '%T %w%f %e' --event modify,delete,create,attrib $SRC | while read date time files
do
        $COMMAND $Option --password-file=$PASSFILE $SRC $USER@$LOCAL::$Module
        echo "$files was rsyncd" >> /var/log/rsync.log 2>&1
done
```
把脚本使用nohup放入后台执行nohup ./rsync.sh &  
这样将更新的文件提交到更新源服务器上，就可以通过Inotify和rsync的配合批量的将更新文件同步到所有服务器中。
