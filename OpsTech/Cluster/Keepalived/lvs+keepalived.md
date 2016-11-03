# LVS+Keepalived介绍

lVS是Linux Virtual Server的简写，即Linux虚拟服务器，是一个虚拟的服务器集群系统，LVS项目在1998年5月由章文嵩博士成立，是中国国内最早出现的自由软件项目之一。目前有三种IP负载均衡技术（VS/NAT、VS/TUN和VS/DR）；十种调度算法`（rrr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq）`。
Keepalived是一个类似于layer3，4&5交换机制的软件，主要用作RealServer的健康状态检查以及LoadBalance主机和BackUP主机之间failover的实现。高可用架：`LVS+Keepalived+Nginx/Apache+php+eaccelerator[+nfs]`

##简单负载均衡架构
![结构图](http:7xlw3d.com1.z0.glb.clouddn.com/tech/cluster/lvs-keepalived.jpg)

IP信息列表：

|名称|IP|
|---|---|
|LVS-VIP|172.16.7.55|
|LVS-Master|172.16.7.56|
|LVS-Slave|172.16.7.57|
|Web-RealServer|172.16.7.16|
|Web-RealServer|172.16.7.144

# 安装LVS和Keepalived
IPVS (IP Virtual Server)是整个负载均衡的基础，如果没有这个基础，故障隔离与切换就毫无意义。IPVS基本上是一种高效的Layer-4交换机，它提供负载平衡的功能。当一个TCP连接的初始SYN报文到达时，IPVS就选择一台服务器，将报文转发给它。此后通过查发报文的IP和TCP报文头地址，保证此连接的后继报文被转发到相同的服务器。这样，IPVS无法检查到请求的内容再选择服务器，这就要求后端的服务器组是提供相同的服务，不管请求被送到哪一台服务器，返回结果都应该是一样的。但是在有一些应用中后端的服务器可能功能不一，有的是提供HTML文档的Web服务器，有的是提供图片的Web服务器，有的是提供CGI的Web服务器。这时，就需要基于内容请求分发 (Content-Based Request Distribution)，同时基于内容请求分发可以提高后端服务器上访问的局部性。IPVS具体实现是由Ipvsadm这个程序来完成，因此判断一个系统是否具备ipvs功能，只要查看Ipvsadm程序是否安装，最简单的办法便是执行命令ipvsadm。

## 下载相关软件包

```
cd /usr/local/src/
wget http://www.linuxvirtualserver.org/software/kernel-2.6/ipvsadm-1.26.tar.gz
wget http://www.keepalived.org/software/keepalived-1.2.17.tar.gz
```

## 安装LVS和Keepalived

```
lsmod | grep ip_vs                                                     #查看是否加载模块
uname -r                                                              #查看内核版本   
2.6.18-164.el5
ln -s /usr/src/kernels/2.6.18-164.el5-i686/ /usr/src/linux            #防止ipvsadm找不到系统内核，需要安装kernel-devel
tar -zxf ipvsadm-1.24.tar.gz                                          #解压源代码
cd ipvsadm-1.24                                                       #切换目录
make && make install                                                  #编译安装
find / -name ipvsadm                                                  #查找安装后文件位置
/etc/rc.d/init.d/ipvsadm                       
/usr/local/src/ipvsadm-1.24/ipvsadm
/sbin/ipvsadm

# ipvsadm                                                               #检验ipvsadm是否正确安装
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
 -> RemoteAddress:PortForward Weight ActiveConn InActConn
lsmod | grep ip_vs                                                    #内核是否加载模块
ip_vs77441  0
```
**报错：**

```
make[1]: *** [libipvs.o] Error 1
make[1]: Leaving directory `/usr/local/src/ipvsadm-1.26/libipvs'
make: *** [libs] Error 2
```

**解决：**
```
yum install libnl* popt* -y
```

## 安装Keepalive

```
cd ..
tar -zxf keepalived-1.1.15.tar.gz
cd keepalived-1.1.15
./configure --prefix=/usr/local/keepalived \
-with-kernel-dir=/usr/src/kernels/2.6.18-164.el5-i686
Keepalived configuration
------------------------
Keepalived version       : 1.1.15
Compiler: gcc
Compiler flags: -g -O2
Extra Lib: -lpopt -lssl -lcrypto
Use IPVS Framework       : Yes
IPVS sync daemon support : Yes
Use VRRP Framework       : Yes
Use LinkWatch: No
Use Debug flags: No
make && make install
find / -name keepalived
/usr/local/keepalived
/usr/local/keepalived/etc/sysconfig/keepalived
/usr/local/keepalived/etc/rc.d/init.d/keepalived
/usr/local/keepalived/etc/keepalived
/usr/local/keepalived/sbin/keepalived
cd /usr/local/keepalived/
cp etc/rc.d/init.d/keepalived /etc/rc.d/init.d/
cp etc/sysconfig/keepalived /etc/sysconfig/
mkdir /etc/keepalived
cp etc/keepalived/keepalived.conf /etc/keepalived/
ln -s /usr/local/keepalived/sbin/keepalived /usr/sbin/
```
# 配置LVS及Keepalived

## 编写配置脚本
绑定VIP地址到LVS_Master上，并设定LVS工作模式为dr(此脚本不适用在Keepalived方案中，只可单独使用)，代码如下

```
cat lvs_dr
#!/bin/bash
# description: Start LVS of DirectorServer
# Write by:Charlie.Cui

FRed="\E[31;40m"; FGreen="\E[32;40m"; FBlue="\E[34;40m"; St0="\033[1m"; St1="\033[5m"; Ed="\033[0m"  
# Set website director vip.
LVS_VIP=172.16.7.55
LVS_RIP1=172.16.7.16
LVS_RIP2=172.16.7.144

. /etc/rc.d/init.d/functions

logger $0 called with $1
case "$1" in
start)
    # set LVS vip
    echo -e Starting LVS Of DirectorServer:"\t""$FGreen$Sto[OK]$Ed"
    echo -e Set LVS_VIP:"\t""$FGreen$Sto$LVS_VIP$Ed"
    /sbin/ipvsadm --set 30 5 60
    /sbin/ifconfig eth1:0 $LVS_VIP broadcast $LVS_VIP netmask 255.255.255.255 broadcast $LVS_VIP up
    /sbin/route add -host $LVS_VIP dev eth1:0
    /sbin/ipvsadm -A -t $LVS_VIP:80 -s wrr -p 3
    /sbin/ipvsadm -a -t $LVS_VIP:80 -r $LVS_RIP1:80 -g -w 1
    /sbin/ipvsadm -a -t $LVS_VIP:80 -r $LVS_RIP2:80 -g -w 1
    touch /var/lock/subsys/ipvsadm >/dev/null 2>&1
;;
stop)
    /sbin/ipvsadm -C
    /sbin/ipvsadm -Z
    /sbin/route del -host $LVS_VIP dev eth1:0
    /sbin/ifconfig eth1:0 down
    /bin/rm -rf /var/lock/subsys/ipvsadm >/dev/null 2>&1
    echo -e Stoping LVS Of DirectorServer:"\t""$FGreen$Sto[OK]$Ed"
;;

status)
    if [ ! -e /var/lock/subsys/ipvsadm ];then
        echo -e "$FRed ipvsadm is stoped $Ed"
        exit 1
    else
        echo -e "$FGreen$Sto ipvsadm is running $Ed"
    fi
;;
*)
    echo "Usage: $0 {start|stop|status}"
    exit 1
esac
exit 0
```

用ipvsadm -Ln查看虚拟服务器IP
```
ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:PortForward Weight ActiveConn InActConn
TCP  172.16.7.55:80 wrr persistent 3
  -> 172.16.7.16:80Route   1      00
  -> 172.16.7.144:80Local   1      00    
```  

查看LVS_VIP 是否绑定到Master上

```
ip addr
1: lo:  mtu 16436 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
3: eth1:  mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 00:50:56:9f:00:38 brd ff:ff:ff:ff:ff:ff
    inet 172.16.7.56/24 brd 172.16.7.255 scope global eth1
    inet 172.16.7.55/32 brd 172.16.7.55 scope global eth1:0
    inet6 fe80::250:56ff:fe9f:38/64 scope link
valid_lft forever preferred_lft forever
4: sit0:  mtu 1480 qdisc noop
    link/sit 0.0.0.0 brd 0.0.0.0
```

## 配置Keepalived
修改/etc/keepalived/keepalived.conf,以下是Master的配置文件，Backup的只需要将红色的子修改即可。

```
cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
    notification_email {
    charlie.cui@hotmail.com                             #配置管理员邮箱，用于报警一行设置一个，可以设置多个
   }

    notification_email_from mail.hotmail.com             #设置邮件发送地址
    smtp_server 127.0.0.1                        #smtp Server地址
    smtp_connect_timeout 30                              #与smtp服务超时时间
    router_id LVS_Master                                 #路由ID和backup要不同，不然会报错
}

#set VIP
vrrp_instance VIP {                                    

    state MASTER                                 #指定Keepalived的角色，master代表主，backup代表辅
    interface eth1                                       #指定HA检测网络的接口
    virtual_router_id 51                         #虚拟路由标示，同一个vrrp_instance下面master和backup要一样
    priority 100                                 #优先级，数字大，优先级高，master要大于backup
    advert_int 1                                 #设定master与backup之间存活检查的时间间隔
    authentication {                                     #设定验证类型和密码
        auth_type PASS                                   #设置验证类型，主要有PASS和AH两种
        auth_pass 1111                                   #设置验证密码，master和backup要一样，这样才能正常通信
    }           
    virtual_ipaddress {                                 
        172.16.7.55                                      #设置虚拟IP地址，可以设置多个，每行一个
    }
}

virtual_server 172.16.7.55 80 {                         #设置虚拟服务器，需要指定ip地址和监听端口
    delay_loop 6                                 #健康检测时间，单位是秒
    lb_algo rr                                           #设置负载调度算法，这里是rr，即轮询算法
    lb_kind DR                                           #设置LVS实现负载均衡的机制，还可以为NAT和TUN
    persistence_timeout 50                               #会话保持时间，单位是秒，这个选项对于动态网页是非常有用的，为集群中的session共享提供了一个很好的解决方案。有个这个会话保持功能用户的请求会被一直分发到某个服务节点，直到超过这个会话保持时间，需要注意的是，这个会话保持时间，是最大无响应超时时间，也就是说用户在操作动态页面时，如果在50秒内没有执行任何操作，那么接下来的操作会被分发的其他节点，但是如果一直操作，则不受50秒限制。

    protocol TCP                                 #指定转发协议类型，有tcp和udp两种
    real_server 172.16.7.16 80 {                     #配置RealServer信息，需要指定ip地址和监听端口    
        weight 3                                 #配置节点权重，数字大，权重大，服务器好可以设置较大的值，可以充分理由服务器资源
        TCP_CHECK {                                      #RealServer的状态检测，单位秒
            connect_timeout 3                             #超时无响应时间
            nb_get_retry 3                                #重试次数
            delay_before_retry 3                  #重试间隔
        }
    }

real_server 172.16.7.144 80 {
    weight 3
    TCP_CHECK {
        connect_timeout 3
    nb_get_retry 3
    delay_before_retry 3
    }
    }
}

```

## 配置RealServer

```
cat lvs_real
#!/bin/bash
##Description: Start realserver
FRed="\E[31;40m"; FGreen="\E[32;40m"; FBlue="\E[34;40m"; St0="\033[1m"; St1="\033[5m"; Ed="\033[0m"  
VIP=172.16.7.55
source= /etc/rc.d/init.d/functions
case "$1" in
start)
    echo -e "$FRed$St0 Start LVS of Realserver $Ed "
    echo -e "$FGreen$St0 Set VIP: $VIP $Ed"
    /sbin/ifconfig lo:0 $VIP broadcast $VIP netmask 255.255.255.255 up
    echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
;;

stop)
    echo -e "$FRed$St0 Close LVS Directorserver $Ed"
    /sbin/ifconfig lo:0 down
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
;;

*)
    echo "Usage:$0 {start|stop}"
exit 1
esac
```

## 测试LVS+Keepalived

### 在2台RealServer上面绑定LVS虚拟IP及抑制arp

```
/opt/lvs_real start
 Start LVS of Realserver
 Set VIP: 172.16.7.55
ip addr
1: lo:  mtu 16436 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet 172.16.7.55/32 brd 172.16.7.55 scope global lo:0
    inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
3: eth1:  mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 00:e0:81:b9:a4:88 brd ff:ff:ff:ff:ff:ff
    inet 172.16.7.16/24 brd 172.16.7.255 scope global eth1
    inet6 fe80::2e0:81ff:feb9:a488/64 scope link
valid_lft forever preferred_lft forever
4: sit0:  mtu 1480 qdisc noop
    link/sit 0.0.0.0 brd 0.0.0.0
```

### 启动LVS_Master的keepalived服务，并查看日志

```
[root@ssq-58-56 opt]# /etc/init.d/keepalived start
Starting keepalived:[  OK  ]
[root@ssq-58-56 ~]# tail -f /var/log/messages
Apr  2 10:45:37 ssq-56 Keepalived: Terminating on signal
Apr  2 10:45:37 ssq-56 Keepalived_vrrp: Terminating VRRP child process on signal
Apr  2 10:45:37 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) removing protocol VIPs.
Apr  2 10:45:37 ssq-56 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.55 removed
Apr  2 10:45:37 ssq-56 Keepalived_healthcheckers: Terminating Healthchecker child process on signal
Apr  2 10:45:37 ssq-56 Keepalived: Stopping Keepalived v1.1.15 (03/19,2013)
Apr  2 10:46:07 ssq-56 Keepalived: Starting Keepalived v1.1.15 (03/19,2013)
Apr  2 10:46:07 ssq-56 Keepalived: Starting Healthcheck child process, pid=14324
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Using MII-BMSR NIC polling thread...
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Netlink reflector reports IP 115.182.58.56 added
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.56 added
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Registering Kernel netlink reflector
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Registering Kernel netlink command channel
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Opening file '/etc/keepalived/keepalived.conf'.
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Configuration is using : 12025 Bytes
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Activating healtchecker for service [172.16.7.16:80]
Apr  2 10:46:07 ssq-56 Keepalived_healthcheckers: Activating healtchecker for service [172.16.7.144:80]
Apr  2 10:46:07 ssq-56 Keepalived: Starting VRRP child process, pid=14325
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Using MII-BMSR NIC polling thread...
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Netlink reflector reports IP 115.182.58.56 added
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Netlink reflector reports IP 172.16.7.56 added
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Registering Kernel netlink reflector
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Registering Kernel netlink command channel
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Registering gratutious ARP shared channel
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Opening file '/etc/keepalived/keepalived.conf'.
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: Configuration is using : 36411 Bytes
Apr  2 10:46:07 ssq-56 Keepalived_vrrp: VRRP sockpool: [ifindex(3), proto(112), fd(8,9)]
Apr  2 10:46:08 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) Transition to MASTER STATE
Apr  2 10:46:09 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) Entering MASTER STATE
Apr  2 10:46:09 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) setting protocol VIPs.
Apr  2 10:46:09 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) Sending gratuitous ARPs on eth1 for 172.16.7.55
Apr  2 10:46:09 ssq-56 Keepalived_vrrp: Netlink reflector reports IP 172.16.7.55 added
Apr  2 10:46:09 ssq-56 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.55 added
Apr  2 10:46:14 ssq-56 Keepalived_vrrp: VRRP_Instance(VIP) Sending gratuitous ARPs on eth1 for 172.16.7.55
```

### 启动backup的Keepalived服务，并查看日志

```
[root@ssq-58-57 opt]# /etc/init.d/keepalived start
Starting keepalived:[  OK  ]
[root@ssq-58-57 ~]# tail -f /var/log/messages
Apr  2 10:51:44 ssq-57 Keepalived: Starting Keepalived v1.1.15 (03/19,2013)
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Using MII-BMSR NIC polling thread...
Apr  2 10:51:44 ssq-57 Keepalived: Starting Healthcheck child process, pid=28840
Apr  2 10:51:44 ssq-57 Keepalived: Starting VRRP child process, pid=28841
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Netlink reflector reports IP 115.182.58.57 added
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.57 added
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Registering Kernel netlink reflector
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Registering Kernel netlink command channel
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Opening file '/etc/keepalived/keepalived.conf'.
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Configuration is using : 12023 Bytes
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Activating healtchecker for service [172.16.7.16:80]
Apr  2 10:51:44 ssq-57 Keepalived_healthcheckers: Activating healtchecker for service [172.16.7.144:80]
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Using MII-BMSR NIC polling thread...
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Netlink reflector reports IP 115.182.58.57 added
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Netlink reflector reports IP 172.16.7.57 added
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Registering Kernel netlink reflector
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Registering Kernel netlink command channel
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Registering gratutious ARP shared channel
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Opening file '/etc/keepalived/keepalived.conf'.
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: Configuration is using : 36409 Bytes
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Entering BACKUP STATE
Apr  2 10:51:44 ssq-57 Keepalived_vrrp: VRRP sockpool: [ifindex(3), proto(112), fd(8,9)]
```

### 使用ipvsadm查看lvs状态

```
[root@ssq-56 opt]# ipvsadm -Ln               
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:PortForward Weight ActiveConn InActConn
TCP  172.16.7.55:80 rr persistent 50
  -> 172.16.7.144:80Route   3      00
  -> 172.16.7.16:80Route   3      00    

[root@ssq-57 opt]# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:PortForward Weight ActiveConn InActConn
TCP  172.16.7.55:80 rr persistent 50
  -> 172.16.7.144:80Route   3      00
  -> 172.16.7.16:80Route   3      00
```

### 测试负载均衡

- 在172.16.7.16和172.16.7.144分别创建以本机IP命令的index.html文件，放到apache的DocumentRoot中（这里放置不同内容是为了方便测试，在生产环境中应该是相同文件）

```
[root@comp ~]# echo "172.16.7.16" > /var/www/html/index.html
[root@ssq-144 ~]# echo "172.16.7.144" > /var/www/html/index.html
```

- 用两台不同机器访问VIP

```
[root@ssq-58-112 ~]# curl 172.16.7.55
172.16.7.16
[root@ssq-58-113 ~]# curl 172.16.7.55
172.16.7.144
```

看到两台机器访问VIP，得到的内容不一样，说明负载均衡成功。

### 测试高可用

1. 关闭master的Keepalived服务器，并查看backup日志

```
[root@ssq-58-56 opt]# /etc/init.d/keepalived stop
Stopping keepalived:[  OK  ]
[root@ssq-58-57 ~]# tail -f /var/log/messages
Apr  2 11:10:19 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Transition to MASTER STATE
Apr  2 11:10:20 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Entering MASTER STATE
Apr  2 11:10:20 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) setting protocol VIPs.
Apr  2 11:10:20 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Sending gratuitous ARPs on eth1 for 172.16.7.55
Apr  2 11:10:20 ssq-57 Keepalived_vrrp: Netlink reflector reports IP 172.16.7.55 added
Apr  2 11:10:20 ssq-57 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.55 added
Apr  2 11:10:25 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Sending gratuitous ARPs on eth1 for 172.16.7.55
```

说明backup已经接管服务，测试访问

```
curl 172.16.7.55
172.16.7.144

curl 172.16.7.55
172.16.7.16
```
web访问并没有受到影响

2. 启动master的Keepalived服务，并查看backup日志

```
/etc/init.d/keepalived start
Starting keepalived:[  OK  ]
[root@ssq-58-57 ~]# tail -f /var/log/messages
Apr  2 11:13:48 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Received higher prio advert
Apr  2 11:13:48 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) Entering BACKUP STATE
Apr  2 11:13:48 ssq-57 Keepalived_vrrp: VRRP_Instance(VIP) removing protocol VIPs.
Apr  2 11:13:48 ssq-57 Keepalived_vrrp: Netlink reflector reports IP 172.16.7.55 removed
Apr  2 11:13:48 ssq-57 Keepalived_healthcheckers: Netlink reflector reports IP 172.16.7.55 removed
```

在master工作后，backup又将工作交还给master
