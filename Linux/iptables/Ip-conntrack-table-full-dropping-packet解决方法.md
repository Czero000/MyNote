### 问题现象

监控报警，发现ping有持续丢包，ifconfig看到网卡dripped:xx 一直在增加，messages日志有以下内容
```
kernel: ip_conntrack: table full, dropping packet.
kernel: printk: 443 messages suppressed.
kernel: ip_conntrack: table full, dropping packet.
kernel: printk: 431 messages suppressed.
```
出现原因是ip_conntrack表满导致的，iptables开启后会加载ip_conntrack模块，来跟踪包。默认情况下ip_conntrack_max大小为65536，`nf_conntrack` 在CentOS 5 / kernel

### 解决方法

#### 关闭防火墙或者清除防火墙规则，简单粗暴，直接有效


#### 增加ip_conntrack表大小优化系统参数

查看ip_conntrack最大大小：
```
cat /proc/sys/net/ipv4/ip_conntrack_max
```

查看当前ip_conntrack大小：
```
wc -l /proc/net/ip_conntrack
```
状态跟踪表的最大行数的设定，理论最大值 `CONNTRACK_MAX = RAMSIZE (in bytes) / 16384 / (ARCH / 32)`

以64G的64位操作系统为例，`CONNTRACK_MAX = 64*1024*1024*1024/16384/2 = 2097152`
```
sysctl –w net.netfilter.nf_conntrack_max = 2097152
```

相关系统参数调优
```
cat /etc/sysctl.conf
net.netfilter.nf_conntrack_max  =   1048576  
net.netfilter.ip_conntrack_tcp_timeout_established  =   3600  
net.netfilter.nf_conntrack_tcp_timeout_close_wait  =   60  
net.netfilter.nf_conntrack_tcp_timeout_fin_wait  =   120  
net.netfilter.nf_conntrack_tcp_timeout_time_wait  =   120
```
sysctl -p  使其生效
这种解决方案，需要在每次iptables重启后，都要执行一遍sysctl -p， 也可以将sysctl -p写入到iptables启动脚本中。 不过ip_conntrack满的隐患还是存在的。

#### 不加载ip_conntrack模块

防火墙不加载任何额外模块 编辑`/etc/sysconfig/iptables-config`配置文件
```
IPTABLES_MODULES="" # 不需要任何附加模块
IPTABLES_MODULES_UNLOAD="no" # 避免iptables重启后sysctl中对应的参数被重置为系统默认值
IPTABLES_SAVE_ON_STOP="no"
IPTABLES_SAVE_ON_RESTART="no"
IPTABLES_SAVE_COUNTER="no"
IPTABLES_STATUS_NUMERIC="yes"
IPTABLES_STATUS_VERBOSE="no"
IPTABLES_STATUS_LINENUMBERS="no"
```

删除nf_conntrack和相关的依赖模块
```
rmmod nf_conntrack_ipv4
rmmod nf_conntrack_ipv6
rmmod xt_state
rmmod xt_CT
rmmod xt_conntrack
rmmod iptable_nat
rmmod ipt_REDIRECT
rmmod nf_nat
rmmod nf_conntrack
```

禁用追踪模块，把它加入黑名单`/etc/modprobe.d/blacklist.conf`
```
# 禁用 nf_conntrack 模块
blacklist nf_conntrack
blacklist nf_conntrack_ipv6
blacklist xt_conntrack
blacklist nf_conntrack_ftp
blacklist xt_state
blacklist iptable_nat
blacklist ipt_REDIRECT
blacklist nf_nat
blacklist nf_conntrack_ipv4
```

/etc/sysconfig/iptables 不要配置状态的规则
```
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
```

优化conntrack模块，请参考下面文章
http://wiki.khnet.info/index.php/Conntrack_tuning
http://blog.yorkgu.me/wp-content/uploads/2012/02/netfilter_conntrack_perf-0.8.txt
