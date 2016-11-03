CMDB新系统上线，设计整体架构要实现高可用，避免出现单点故障，设计使用keepalived+nginx部署前端Web Server。

# Keepalived介绍
Keepalived 是一个基于VRRP协议来实现服务器高可用或热备解决方案，Keepalived可以用来防止服务器单点故障(单点故障是指一旦某一点出现故障就会导致整个系统架构的不可用)的发生，通过配合Nginx可以实现web前端服务的高可用。

## VRRP协议
VRRP全称 Virtual Router Redundancy Protocol，即 虚拟路由冗余协议。可以认为它是实现路由器高可用的容错协议，即将N台提供相同功能的路由器组成一个路由器组(Router Group)，这个组里面有一个master和多个backup，但在外界看来就像一台一样，构成虚拟路由器，拥有一个虚拟IP（vip，也就是路由器所在局域网内其他机器的默认路由），占有这个IP的master实际负责ARP相应和转发IP数据包，组中的其它路由器作为备份的角色处于待命状态。master会发组播消息，当backup在超时时间内收不到vrrp包时就认为master宕掉了，这时就需要根据VRRP的优先级来选举一个backup当master，保证路由器的高可用。

在VRRP协议实现里，虚拟路由器使用 00-00-5E-00-01-XX 作为虚拟MAC地址，XX就是唯一的 VRID （Virtual Router IDentifier），这个地址同一时间只有一个物理路由器占用。在虚拟路由器里面的物理路由器组里面通过多播IP地址 224.0.0.18 来定时发送通告消息。每个Router都有一个 1-255 之间的优先级别，级别最高的（highest priority）将成为主控（master）路由器。通过降低master的优先权可以让处于backup状态的路由器抢占（pro-empt）主路由器的状态，两个backup优先级相同的IP地址较大者为master，接管虚拟IP。

## 与heartbeat/corosync等比较
>Heartbeat、Corosync、Keepalived这三个集群组件我们到底选哪个好，首先我想说明的是，Heartbeat、Corosync是属于同一类型，Keepalived与Heartbeat、Corosync，根本不是同一类型的。Keepalived使用的vrrp协议方式，虚拟路由冗余协议 (Virtual Router Redundancy Protocol，简称VRRP)；Heartbeat或Corosync是基于主机或网络服务的高可用方式；简单的说就是，Keepalived的目的是模拟路由器的高可用，Heartbeat或Corosync的目的是实现Service的高可用。

>所以一般Keepalived是实现前端高可用，常用的前端高可用的组合有，就是我们常见的LVS+Keepalived、Nginx+Keepalived、HAproxy+Keepalived。而Heartbeat或Corosync是实现服务的高可用，常见的组合有Heartbeat v3(Corosync)+Pacemaker+NFS+Httpd 实现Web服务器的高可用、Heartbeat v3(Corosync)+Pacemaker+NFS+MySQL 实现MySQL服务器的高可用。总结一下，Keepalived中实现轻量级的高可用，一般用于前端高可用，且不需要共享存储，一般常用于两个节点的高可用。而Heartbeat(或Corosync)一般用于服务的高可用，且需要共享存储，一般用于多节点的高可用。这个问题我们说明白了。

>又有博友会问了，那heartbaet与corosync我们又应该选择哪个好啊，我想说我们一般用corosync，因为corosync的运行机制更优于heartbeat，就连从heartbeat分离出来的pacemaker都说在以后的开发当中更倾向于corosync，所以现在corosync+pacemaker是最佳组合。

## Keepalived+nginx 配置方案

1. Nginx+Keepalived主从方式
多个主机使用一个VIP地址，一个做为主服务器，剩下的为备用服务器，正常下只有一个在工作，只有当主服务器出现故障时，被服务器才会被启用

2. Nginx+Keepalived双主(多主)方式
要求使用两个或两个以上的VIP地址，两个服务器互为主备或一主多备，同时在工作，当一台出现故障，请求转移到备用服务器，本文采用这种方式


## 整体架构图
![global](http://ofc9x1ccn.bkt.clouddn.com/web/nginx/keepalived-nginx.png)

# 安装

## 系统环境介绍

|用途|ip|备注|
|---|----|
|CMDB-DB-M|172.16.8.140|Ubuntu-16.04 LTS|
|CMDB-DB-S|172.16.8.144|Ubuntu-16.04 LTS|
|CMDB-Calc|172.16.8.244|Ubuntu-16.04 LTS|
|Gjobs-DB-M|172.16.8.158|Ubuntu-16.04 LTS|
|Gjobs-DB-S|172.16.8.169|Ubuntu-16.04 LTS|
|Gjob-Ansible|172.16.8.176|Ubuntu-16.04 LTS|
|Greports-DB-M|172.16.8.164|Ubuntu-16.04 LTS|
|Greports-DB-S|172.16.8.197|Ubuntu-16.04 LTS|
|Greports-Calc|172.16.8.204|Ubuntu-16.04 LTS|
|Nginx-PHP-M/B|172.16.8.156|Ubuntu-16.04 LTS|
|Nginx-PHP-B/M|172.16.8.178|Ubuntu-16.04 LTS|
|Nginx-Django-M/B|172.16.8.180|Ubuntu-16.04 LTS|
|Nginx-Django-B/M|172.16.8.243|Ubuntu-16.04 LTS|
|VIP|172.16.8.209|绑定到Nginx-PHP-M/B|
|VIP|172.16.8.208|绑定到Nginx-PHP-B/m|
|VIP|172.16.8.212|绑定到Nginx-Django-M/B|
|VIP|172.16.8.225|绑定到Nginx-Django-B/M|


## 安装keepalived
主备两个服务器都要安装keepalived

-  安装依赖软件包

```shell
apt install gcc g++ make cmake openssl libssl-dev libpopt-dev -y
```
- 源码方式

```
wget http://www.keepalived.org/software/keepalived-1.2.23.tar.gz
tar -zxf keepalived-1.2.23.tar.gz
cd keepalived-1.2.23/
./configure --prefix=/usr/local/keepalived
make && make install
cd /usr/local/keepalived/
cp etc/rc.d/init.d/keepalived /etc/init.d/
mkdir /etc/keepalived/
cp etc/keepalived/keepalived.conf /etc/keepalived/
cp etc/sysconfig/keepalived /etc/default/
ln -s /usr/local/keepalived/sbin/keepalived /usr/sbin/
```
- apt方式
```
apt install keepalived -y
```

## 启动Keepalived
先在就可以先尝试启动keepalived服务，不过刚刚拷贝的init脚本并不适用在Ubuntu系统上(适用于CentOS/RHEL)，要稍作修改即可使用,下面的是keepalived apt方式安装的init脚本，直接拿来即可使用。
```
vim /lib/systemd/system/keepalived.service
[Unit]
Description=Keepalive Daemon (LVS and VRRP)
After=network-online.target
Wants=network-online.target
# Only start if there is a configuration file
ConditionFileNotEmpty=/etc/keepalived/keepalived.conf

[Service]
Type=forking
KillMode=process
# Read configuration variable file if it is present
EnvironmentFile=-/etc/default/keepalived
ExecStart=/usr/sbin/keepalived $DAEMON_ARGS
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```
[INIT-keepalived](https://czero000.github.io/upload/nginx/init-keepalived)
```
/etc/init.d/keepalived start
```
## 安装Nginx
略

# 配置

## 配置keepalived

- 主

```
! Configuration File for keepalived

global_defs {
   notification_email {
        cc@zerounix.com
   }
   notification_email_from mail.zerounix.com
   smtp_server mail.zerounix.com
   smtp_connect_timeout 30
   router_id LVS_Master
}

vrrp_script chk_nginx {
    script "/usr/local/nginx/sbin/nginx_check"
    interval 2
    weight 2
}
vrrp_instance Nginx_PHP_1 {
    state MASTER
    interface enp3s0
    virtual_router_id 156
    mcast_src_ip 172.16.8.178
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        172.16.8.208
    }
    track_script {
        chk_nginx
    }
    track_interface {
        enp3s0
    }
}

vrrp_instance Nginx_PHP_2 {
    state BACKUP
    interface enp3s0
    virtual_router_id 178
    mcast_src_ip 172.16.8.178
    priority 190
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        172.16.8.209
    }
    track_script {
        chk_nginx
    }
    track_interface {
        enp3s0
    }
}
```

```
more nginx_check
#!/bin/bash
A=`ps -C nginx --no-header |wc -l`              
if [ $A -eq 0 ];then                                      
                /usr/local/nginx/sbin/nginx
                sleep 3
                if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
                       killall keepalived
                fi
fi
```

## 测试keepalived
1. 主Nginx停止Nginx或直接断网情况下（backup正常），访问虚拟IP：172.16.8.208/209的相关Web服务，正常，测试通过
2. backup Nginx停止Nginx或直接断网情况下（Master正常），访问虚拟IP：172.16.8.208/209的相关Web服务，正常，测试通过
