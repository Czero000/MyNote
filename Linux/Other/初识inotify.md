### 概述

在工作中，人们往往需要知道在某些文件、目录上都有那些变化，比如：

* 通知配置文件的改变
* 追踪某些关键的系统文件变化
* 系统崩溃时进行自动清理
* 自动触发备份进程
* 向服务器上传文件结束时发出通知

通常使用文件轮询的通知机制，但是这种机制只适用经常改变的文件（因为它可以确保没过x秒就可以得到i/o），其他情况下都非常低效，并且有时候会丢失某些类型的变化，例如文件的修改时间没有改变。像Tripwire这样的数据完整性系统，他们基于时间调度来追踪文件变化，但是如果想实时监控文件的变化，那么时间调度就束手无策了，Inotify就这样应运而生了。

### Inorify是什么

  在日常的运维过程中，经常需要备份某些文件，或者对系统的某些文件进行监控，比如重大服务的配置文件。如果需要做到实时同步或是监控，就需要使用内核的inotify机制。Linux内核从2.6.13开始引入Inotify，现在几乎所有的主流Linux发行版都已经支持Inotify机制，Inotify是基于inode级别的文件系统监控技术，是一种强大的、细粒度的、异步的机制，他满足各种各样的文件监控需要，不仅限于安全和性能。
Inotify不需要对监视的目标打开文件描述符，而且如果被监视目录在可移动介质上，那么在umount该介质的文件系统后，被监视目标的watch将被自动删除，并且会产生一个umount事件。

* Inotify既可以监视文件，亦可以监视目录
* Inotify使用系统调用而非Sigio来通知文件系统事件
* Inotify使用文件描述符作为接口，因而可以使用通常的文件I/O操作select和poll来监视文件系统的变化

如何知道你的Linux内核是否支持Inotify机制呢，执行下面命令：
```
grep INOTIFY_USER /boot/config-$(uname -r)
CONFIG_INOTIFY_USER=y
```
如果输出`CONFIG_INOTIFY_USER=y`，那么就可以享受Inotify之旅了。

### 安装inotify-tools

#### 软件下载地址

官方地址：`[https://github.com/rvoicilas/inotify-tools/wiki]([https://github.com/rvoicilas/inotify-tools/wiki)`

#### 下载安装软件包
```
wget --no-check-certificate https://github.com/downloads/rvoicilas/inotify-tools/inotify-tools-3.14.tar.gz
tar -zxf inotify-tools-3.14.tar.gz 
cd inotify-tools-3.14
./configure --prefix=/usr/local/inotify
make && make install
```

### 使用Inotify

#### Inotify可监视的文件系统事件

* IN_ACCESS：   即文件被访问
* IN_MODIFY：    文件被write
* IN_ATTRIB：    文件属性被修改，如chmod、chown、touch等
* IN_CLOSE_WRITE：    可以文件被close
* IN_CLOSE_NOWRITE：   不可写文件被close
* IN_OPEN：    文件被打开
* IN_MOVED_FROM：    文件被移走，如mv
* IN_MOVED_TO：    文件被移来，如mv、cp
* IN_CREATE：    创建新文件
* IN_DELETE：    文件被删除，如rm
* IN__DELETE_SELF： 自删除，挤一个可执行文件在执行时删除自己
* IN_MOVE_SELF：    自移动，即一个可执行文件在执行时移动自己
* IN_UNMOUNT：    宿主文件系统被umount
* IN_CLOSE：    文件被关闭，等同于（IN_CLOSE_WRITE|IN_CLOSE_NOWRITE）
* IN_MOVE：     文件被移动，等同于（IN_MOVED_FROM|IN_MOVED_TO）

#### inotify的默认内核参数
* **/proc/sys/fs/inotify/max_queued_events**     默认值：16384 该文件中的值为调用inotify_init时分配给inotify instatnce中可排队的event的数目最大值，超出这个值的时间被丢弃，但会触发IN_Q_OVERFLOW事件
* **/proc/sys/fs/inotify/max_user_instances**     默认值：128 指定了每个read user ID可创建的inotify instatnces的数量上限
* **/proc/sys/fs/inotify/max_user_watches**         默认值：8192 指定了每个inotify instance相关的watches的上限

**PS：max_queued_events是Inotify管理的队列的最大长度，文件系统变化越频繁，这个值就应该越大
如果在日志中看到Event Queue Overflow，说明max_queued_events大小需要调整参数后再次使用**


#### 使用incron实现重要配置文件监控

incron是inotify的cron系统，与本身的cron一样，包含一个后台守护进程（incrond）和一个事件编辑器（incrontab）与系统本身的cron不同的仅仅是触发时间的是os对某个文件或者文件夹的操作而不再是时间，由于系统事件触发的机制，对于应用系统来说，几乎做到实时性。
安装incron包
```
rpm -Uvh http://mirrors.sohu.com/fedora-epel/5Server/i386/incron-0.5.5-2.el5.i386.rpm
```
查看incron支持的事件类型：`incrontab -t `，编辑配置文件使用`incrontab -e`
配置文件爱你格式说明：（默认配置在/var/spool/incron/ 目录下）
```
   
```

选项说明：

* path ：    需要监控的文件和目录
* event ：    系统对监控对象发生的事件，多个事件可以用逗号隔离，
* command  ：    command可以是系统命令，也可以是脚本，不能使用系统的重定向，除非重定向写在脚本中
*  command 还可以使用下面变量：
  * $@ ：代表 ，即监控对象
  * $#：    发生系统时间的对象（如果监控的是某个文件夹，某个文件发生变化，那么$#就代表了该文件）
  * $%：    代表 ，即发生的事件
* event  监控事件如下：
  * IN_ACCESS
  * IN_MODIFY
  * IN_ATTRIB
  * IN_CLOSE_WRITE
  * IN_CLOSE_NOWRITE
  * IN_OPEN
  * IN_MOVED_FROM
  * IN_MOVED_TO
  * IN_CREATE
  * IN_DELETE
  * IN_DELETE_SELF
  * IN_CLOSE
  * IN_MOVE
  * IN_ONESHOT
  * IN_ALL_EVENTS
  * IN_DONT_FOLLOW    ：
  * IN_ONLYDIR            ：只监控目录
  * IN_MOVE_SELF        ：仅监控一次事件

配置举例：
```
incrontab -e
/opt/test/a.txt IN_MODIFY           echo "$@ $#"             表示文件a.txt一旦被修改，就执行echo "$@ $#"
/opt/test/        IN_ALL_EVENTS   echo "$@ $# $%"       表示目录下文件任何事件触发，就执行echo "$@ $# $%"
```
启动incrond
```
/etc/init.d/incrond start），然后在/opt/test/ 目录创建a.txt，并修改、删除，查看/var/log/cron，如下输出：
Nov 10 18:12:28 ssq-54-100 incrond[11908]: stopping service
Nov 10 18:12:28 ssq-54-100 incrond[12072]: starting service (version 0.5.5, built on Oct  2 2009 12:18:20)
Nov 10 18:12:28 ssq-54-100 incrond[12073]: loading system tables
Nov 10 18:12:28 ssq-54-100 incrond[12073]: loading user tables
Nov 10 18:12:28 ssq-54-100 incrond[12073]: loading table for user root
Nov 10 18:12:28 ssq-54-100 incrond[12073]: ready to process filesystem events
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test  IN_OPEN,IN_ISDIR")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test  IN_CLOSE_NOWRITE,IN_ISDIR")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo  "/opt/test/a.txt ")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test a.txt IN_MODIFY")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test a.txt IN_OPEN")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test a.txt IN_MODIFY")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo  "/opt/test/a.txt ")
Nov 10 18:12:41 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test a.txt IN_CLOSE_WRITE")
Nov 10 18:12:45 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test  IN_OPEN,IN_ISDIR")
Nov 10 18:12:45 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test  IN_CLOSE_NOWRITE,IN_ISDIR")
Nov 10 18:12:53 ssq-54-100 incrond[12073]: (root) CMD (echo "/opt/test a.txt IN_DELETE")
```
总体来说，文件和目录的监控还是很有效的

### linux下使用inotify

`/usr/local/inotify/bin/inotifywait`仅执行阻塞，等待inotify事件。可以监视任何一组文件和目录，或监控这个目录树（目录、子目录）

脚本示例：
```
#!/bin/bash
inotifywait='/usr/local/inotify/bin/inotifywait'
$inotifywait -mrq --timefmt '%y-%m-%d %H:%M' --format '%T %w%f %e' --event modify,delete,create,attrib /opt/test | while read date t
ime file event 
do      
        case $event in 
                MODIFY|CREATE|MOVE|MODIFY,ISDIR|CREATE,ISDIR|MODIFY,ISDIR)
                        echo $event'-'$file
                ;;
                MOVED_FROM|MOVED_FROM,ISDIR|DELETE|DELETE,ISDIR)
                        echo $event'-'$file
                ;;
        esac
done
```
执行脚本输出如下：`touch test.txt、echo "This is a test" > test.txt rm test.txt -f`
```
sh inotifywaith.sh 
CREATE-/opt/test/test.txt
MODIFY-/opt/test/test.txt
DELETE-/opt/test/test.txt
```

inotifywait命令常用选项如下：
* --exclude        排除某些文件
* --excludei        排除某些文件,并忽略大小写
* -m|--monitor    持续行的监控
* -q|-quiet        打印出监控事件
* -d|--daemon 
* -r|--recursive  　递归监控指定目录下的所有文件，包括新建的文件或子目录；如果要监控的目录中文件数量巨大，则通常需要修改/proc/sys/fs/inotify/max_users_watchs内核参数

`/usr/local/inotify/bin/inotifywatch`收集关于被监视的文件系统的统计数据，包括每个inotify时间发生多少次
假如想知道某个指定文件夹上有什么操作，可以这么做：
```
#!/bin/bash
inotifywatch='/usr/local/inotify/bin/inotifywatch'
$inotifywatch  -v -e access,modify,attrib,close_write,close_nowrite,close,open,moved_to,moved_from,move,create,delete,delete_self
 -t 120 -r /opt/test
sh inotifywatch.sh  
Establishing watches...
Setting up watch(es) on /opt/test
OK, /opt/test is now being watched.
Total of 1 watches.
Finished establishing watches, now collecting statistics.
Will listen for events for 120 seconds.
total  modify  attrib  close_write  close_nowrite  open  moved_from  moved_to  create  delete  filename
19     2       1       2            4              6     1           1         1       1       /opt/test/
```
