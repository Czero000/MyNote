主辅DN数据同步，首先master修改完成并重启服务后，将传送notify给slave。slave将查询master的SOA记录，master收到请求后将SOA记录发送给Slave，Slave收到后同时对比查询结果中的serial值，如果serial值不大于本机的话将结束数据同步过程；但是如果serial值大于本机的话，slave将发送zone transfer请求要求（AXFR/IXFR）。Master响应zone transfer请求并传送结果，直到整个slave更新完成。

## 安装软件包(主从服务器)
```
yum install bind bind-chroot bind-utils bind-libs
```

## 配置Master服务器
### 编辑bind主配置文件
```
cat /var/named/chroot/etc/named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 162.243.134.106; };                    \\监听ip及端口
        directory       "/var/named";                              \\dns工作目录
        dump-file       "/var/named/data/cache_dump.db";           \\ 缓存转存文件
        statistics-file "/var/named/data/named_stats.txt";         \\内存使用统计信息
        allow-query     { any; };                                  \\ 允许查询的主机，默认是localhost
        recursion no;                                              \\是否递归查询
        allow-transfer  { 162.243.134.107; };                      \\允许同步ip

};

logging {                                                          \\定义bind服务日志
        channel "named_log" {
        file "logs/named.log" versions 10 size 5m;
        severity dynamic;
        print-category yes;
        print-severity yes;
        print-time yes;
};

channel "query_log" {                                              \\定义查询日志
        file "logs/query.log" versions 10 size 5m;
        severity debug;
        print-severity yes;
        print-time yes;
};

category default { named_log; };
category queries { query_log; };
};

zone "." IN {
        type hint;                                                 \\定义根区域
        file "named.ca";                                           \\区域文件  
};

include "/etc/rndc.key";

zone "zerounix.com" IN {                                           \\用户区域文件                    
        type master;
        masters { 162.243.134.106; };
        file "zerounix.com.db";
};
rm -f /etc/named.conf
ls -s /var/named/chroot/etc/named.conf /etc/named.conf
```

###  增加zerounix.com区域文件
```
cat /var/named/chroot/var/named/zerounix.com.db
$TTL    60
@       IN      SOA     ns1.zerounix.com.    hostmaster.zerounix.com. (
                        2015101702
                        3600
                        300
                        604800
                        600
                        )

                IN      NS      ns1.zerounix.com.
                IN      NS      ns2.zerounix.com.
                IN      MX      5       mail.zerounix.com.
                IN              A       162.243.134.106
www             IN              CNAME   web.zerounix.com
web             IN              A       162.243.134.106
```
### 启动bind服务
```
/etc/init.d/named start
```

### 测试解析是否正常
```
dig www.zerounix.com @162.243.134.106

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.37.rc1.el6_7.4 <<>> www.zerounix.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20243
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.zerounix.com.              IN      A

;; ANSWER SECTION:
www.zerounix.com.       9       IN      CNAME   web.zerounix.com.
web.zerounix.com.       9       IN      A       162.243.134.106

;; Query time: 362 msec
;; SERVER: 162.243.134.106#53(162.243.134.106)
;; WHEN: Mon Oct 19 17:22:21 2015
;; MSG SIZE  rcvd: 68
```

## 配置Slave服务器

### 编辑bind配置文件
```
 cat /var/named/chroot/etc/named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 162.243.134.107; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        allow-query     { any; };
        recursion no;
        allow-transfer  { 162.243.134.106; 162.243.134.107;};

};

logging {
        channel "named_log" {
        file "logs/named.log" versions 10 size 5m;
        severity dynamic;
        print-category yes;
        print-severity yes;
        print-time yes;
};

channel "query_log" {
        file "logs/query.log" versions 10 size 5m;
        severity debug;
        print-severity yes;
        print-time yes;
};

category default { named_log; };
category queries { query_log; };
};

zone "." IN {
        type hint;
        file "named.ca";
};

include "/etc/rndc.key";

zone "zerounix.com" IN {
        type slave;
        masters { 162.243.134.106; };
        file "zerounix.com.db";
        transfer-source 162.243.134.107;
};
rm -f /etc/named.conf
ls -s /var/named/chroot/etc/named.conf /etc/named.conf
```

### 启动bind服务
```
/etc/init.d/named start
```

### 验证主辅同步
#### 查看日志
```
tail -f /var/named/chroot/var/named/logs/named.log
19-Oct-2015 17:39:42.825 notify: info: client 162.243.134.106#3133: received notify for zone 'zerounix.com'
19-Oct-2015 17:39:42.827 general: info: zone zerounix.com/IN: Transfer started.
19-Oct-2015 17:39:42.828 xfer-in: info: transfer of 'zerounix.com/IN' from 162.243.134.106#53: connected using 162.243.134.107#50919
19-Oct-2015 17:39:42.830 general: info: zone zerounix.com/IN: transferred serial 2015101701
19-Oct-2015 17:39:42.830 xfer-in: info: transfer of 'zerounix.com' from 162.243.134.106#53: Transfer completed: 1 messages, 7 record
s, 222 bytes, 0.001 secs (222000 bytes/sec)
```

#### 查看zone文件
```
cat /var/named/chroot/var/named/zerounix.com.db
$ORIGIN .
$ORIGIN .
$TTL 60 ; 1 minute
zerounix.com              IN SOA  ns1.zerounix.com. hostmaster.zerounix.com. (
                                2015101702 ; serial
                                3600       ; refresh (1 hour)
                                300        ; retry (5 minutes)
                                604800     ; expire (1 week)
                                600        ; minimum (10 minutes)
                                )
                        NS      ns1.zerounix.com.
                        NS      ns2.zerounix.com.
                        A       162.243.134.106
                        MX      5 mail.zerounix.com.
$ORIGIN zerounix.com.
www                     CNAME   web.zerounix.com.
web                     A       162.243.134.106
```

### 测试解析
```
dig www.zerounix.com @162.243.134.107

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.37.rc1.el6_7.4 <<>> www.zerounix.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20272
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.zerounix.com.              IN      A

;; ANSWER SECTION:
www.zerounix.com.       9       IN      CNAME   web.zerounix.com.
web.zerounix.com.       9       IN      A       162.243.134.106

;; Query time: 379 msec
;; SERVER: 162.243.134.107#53(162.243.134.107)
;; WHEN: Mon Oct 19 17:35:21 2015
;; MSG SIZE  rcvd: 68
```
