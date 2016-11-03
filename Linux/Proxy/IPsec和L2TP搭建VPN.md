# 利用 IPsec 和 L2TP 搭建 VPN

## 安装 EPEL 源
```
yum install epel-release -y
```

## 安装 软件包
Openswan 是 linux 下 VPN 协议 IPSec的一种实现，CentOS7安装源中有它的开源社区版，叫做 libreswan，先在来安装
```
yum install libreswan xl2tpd ppp lsof -y
```

## 设置内核参数
```
echo "net.ipv4.ip_forward = 1" |  tee -a /etc/sysctl.conf
echo "net.ipv4.conf.all.accept_redirects = 0" |  tee -a /etc/sysctl.conf
echo "net.ipv4.conf.all.send_redirects = 0" |  tee -a /etc/sysctl.conf
for vpn in /proc/sys/net/ipv4/conf/*; do echo 0 > $vpn/accept_redirects; echo 0 > $vpn/send_redirects; done
for i in /proc/sys/net/ipv4/conf/*;do echo 0 > $i/rp_filter;done
sysctl -p
```

## 添加 rc.local 文件
```
for vpn in /proc/sys/net/ipv4/conf/*; do echo 0 > $vpn/accept_redirects; echo 0 > $vpn/send_redirects; done
for i in /proc/sys/net/ipv4/conf/*;do echo 0 > $i/rp_filter;done
```

## 修改IPsec配置文件

- 在 `/etc/ipsec.d/` 目录下，新建配置文件 `l2tp.conf`，并添加如下内容
```
#conn %default
#    Forceencaps=yes
conn L2TP-PSK-NAT  
    rightsubnet=vhost:%priv
    also=L2TP-PSK-noNAT

conn L2TP-PSK-noNAT  
    authby=secret
    pfs=no
    auto=add
    type=transport
    keyingtries=3
    rekey=no
    ikelifetime=8h
    salifetime=1h
    left=serverIP
    leftprotoport=17/1701
    right=%any
    rightprotoport=17/%any
```

- 设置共享秘钥
```
cat /etc/ipsec.d/l2tp.secrets
59.151.49.125 %any: PSK "linekong"
```

## 启动 IPSec
```
systemctl start ipsec
systemctl enable ipsec
```

## 验证 IPSec 是否正常
```
ipsrc verify
Verifying installed system and configuration files

Version check and ipsec on-path                         [OK]
Libreswan 3.15 (netkey) on 3.10.0-229.el7.x86_64
Checking for IPsec support in kernel                    [OK]
 NETKEY: Testing XFRM related proc values
         ICMP default/send_redirects                    [OK]
▽        ICMP default/accept_redirects                  [OK]
         XFRM larval drop                               [OK]
Pluto ipsec.conf syntax                                 [OK]
Hardware random device                                  [N/A]
Two or more interfaces found, checking IP forwarding    [OK]
Checking rp_filter                                      [OK]
Checking that pluto is running                          [OK]
 Pluto listening for IKE on udp 500                     [OK]
 Pluto listening for IKE/NAT-T on udp 4500              [OK]
 Pluto ipsec.secret syntax                              [OK]
Checking 'ip' command                                   [OK]
Checking 'iptables' command                             [OK]
Checking 'prelink' command does not interfere with FIPSChecking for obsolete ipsec.conf options                 [OK]
Opportunistic Encryption
//  可以根据提示信息，修改相应配置，多数是内核参数
```


## 配置 xl2tpd

编辑配置文件
```
vim /etc/xl2tpd/xl2tpd.conf
[global]
listen-addr = serverIP
auth file = /etc/ppp/chap-secrets
ipsec saref = yes
; force userspace = yes
; debug tunnel = yes

[lns default]
ip range = 10.0.2.128-10.0.2.254
local ip = 1.1.1.1
require chap = yes
refuse pap = yes
require authentication = yes
name = LinuxVPNserver
ppp debug = yes
pppoptfile = /etc/ppp/options.xl2tpd
length bit = yes
```


## 配置 PPP
编辑配置文件`/etc/ppp/options.xl2tpd`
```
require-mschap-v2
ms-dns 8.8.8.8
ms-dns 8.8.4.4
asyncmap 0
auth
crtscts
lock
hide-password
modem
debug
name l2tpd
proxyarp
lcp-echo-interval 30
lcp-echo-failure 4
```

## 添加测试用户
```
vim chap-secrets
#
# Secrets for authentication using CHAP
# client        server  secret                  IP addresses
test            l2tpd   123456                  10.0.12.100
```

## 启动 IPSec
```
systemctl start xl2tpd
systemctl enable xl2tpd
```

## 利用 iptable 配置转发规则

- gw.sh
```
#!/bin/bash

/sbin/iptables -t nat -F

/sbin/iptables -t nat -A POSTROUTING -s 10.0.12.0/24 -d 172.16.0.0/16 -o eth1 -j SNAT --to-source 172.16.1.125
/sbin/iptables -t nat -A POSTROUTING -s 10.0.12.0/24 ! -d 10.0.12.0/24 -o eth0 -j SNAT --to-source 59.151.49.125
/sbin/iptables -t nat -A POSTROUTING -s 10.0.12.0/24 ! -d 172.16.0.0/16 -o eth0 -j SNAT --to-source 59.151.49.125

```

- forward.sh
```
// 172.16.3.100 为办公电脑IP
#!/bin/bash
/sbin/iptables -F FORWARD

##[test]
/sbin/iptables -A FORWARD -s 10.0.12.100 -p tcp -d 172.16.3.100 -j ACCEPT

##[default]
/sbin/iptables -A FORWARD -s 10.0.12.0/24 -d 172.16.0.0/255.255.0.0 -j DROP
#/sbin/iptables -A FORWARD -s 10.0.12.0/24 -d 59.151.39.0/255.255.255.0 -j DROP
#/sbin/iptables -A FORWARD -s 10.0.12.0/24 -d 59.151.49.0/255.255.255.0 -j DROP
```
