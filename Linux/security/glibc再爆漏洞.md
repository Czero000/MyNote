

## 漏洞详情 ##

近日，Google和Red Hat的安全人员发现GNU C Library (glibc)中存在严重的安全漏洞，可导致Linux软件被攻击者劫持，进而在Linux平台上执行任意代码，获取密码，监视用户，甚至控制计算机。CVE编号为[CVE-2015-7547](https://access.redhat.com/security/cve/CVE-2015-7547)。
![glibc_bug](http://ofc9x1ccn.bkt.clouddn.com/system/security/glibc_bug.jpg)

glibc是GNU发布的libc库，即c运行库。它是Linux系统中最底层的API，几乎其它运行库都会依赖于glibc。glibc应用于众多Linux发行版本中，所以此类漏洞影响范围十分广泛。

### 漏洞概述 ###
glibc的DNS客户端解析器中存在基于栈的缓冲区溢出漏洞。当软件用到getaddrinfo库函数(处理名字到地址以及服务到端口的转换)时，攻击者便可借助特制的域名、DNS服务器或中间人攻击利用该漏洞，控制软件，并试图控制整个系统。

攻击者使用恶意的DNS域名服务器创建类似于evildomain.com的域名，然后向目标用户发送带有指向该域名的链接的邮件，一旦用户点击该链接，客户端或浏览器将会开始查找ildomain.com，并最终得到恶意服务器的buffer-busting响应。该域名被嵌入服务器日志中，一旦解析就会触发远程代码执行，SH客户端也会因此被控制。或者，位于目标用户网络中的中间人攻击者可以篡改DNS响应，向恶意代码中动态注入负载。

据目前的调查情况，此漏洞影响自2.9之后的所有版本，其他旧版本也可能受到影响。
![glibc_system_version](http://ofc9x1ccn.bkt.clouddn.com/system/security/glibc_system_version.png '收到影响的RHEL系统版本')

其他系统还包括
```
CentOS6 所有版本
CentOS7所有版本
SUSE Linux Enterprise Server 11 SP3
SUSE Linux Enterprise Server 12
Ubuntu Server 14.04.1 LTS 32位
Ubuntu Server 14.04.1 LTS 64位
Ubuntu Server 12.04 LTS 64位
Ubuntu Server 12.04 LTS 64位（Docker）
Debian8.2 32位
Debian8.2 64位
Debian7.8 32位
Debian7.8 64位
Debian7.4 64位
CoreOS717.3.0 64位
```

### 技术细节 ###

glibc通过alloca()函数在栈中为`_nss_dns_gethostbyname4_r`函数2048字节的空间，用于托管DNS响应。若响应大于2048字节，程序会从堆中重新分配一个缓冲区，并更新所有信息(缓冲区指针，缓冲区大小和响应大小)。

在一定条件下，会出现栈缓冲区和新分配的堆内存的错误匹配，导致超过栈缓冲区大小的响应仍然存储在栈中，进而发生缓冲区溢出。触发该漏洞的利用向量十分普遍，并且ssh、sudo和curl等工具中。


### 缓解 ###
该漏洞存在于resolv/res_send.c文件中，当getaddrinfo()函数被调用时会触发该漏洞。技术人员可以通过将TCP DNS响应的大小限制为1024字节，并丢弃所有超过512字节的UDPDNS数据包来缓解该问题。值得庆幸的是，许多嵌入式Linux设备，例如家庭路由器，更倾向于使用uclibc库，因此可以免受该漏洞的影响。

### 漏洞的成因及POC使用测试 ###
据悉，漏洞的成因在于DNS Server Response返回过量的(2048 ) 字节, 导致接下来的response 触发栈溢出。目前，Google已提供了POC，据其博客中所述，该漏洞应该是可以绕过内存防护技术，从而形成代码执行漏洞。
具体POC 地址如下：github.com/fjserna/CVE-2015-7547
  对此，乌云白帽子路人甲在自己的本地lubuntu 上进行了测试，libc 版本为 2.19。lubuntu系列也属于Debian 的一个发行版，故理论上满足漏洞条件。测试过程如下：
根据漏洞描述，我们可以做一个假的DNS Server 作为中间人，来验证该漏洞。更改DNS 解析为 127.0.0.1，刷新DNS 缓存 sudo /etc/init.d/nscd restart 执行 CVE-2015-7547-poc.py , 注意无需更改 ip_addr 。编译 CVE-2015-7547-client.c , 执行CVE-2015-7547-client
若含有漏洞，会造成Segmentation Fault。
![glibc_bug_info](http://ofc9x1ccn.bkt.clouddn.com/system/security/glibc_bug_info.png)


文件下载链接：
[CVE-2015-7547-master.zip](https://czero000.github.io/upload/security/CVE-2015-7547-master.zip)


## 修复过程 ##

1. 更新glibc版本
```
//rhel¢os
yum -y update glibc* nscd


//debian&ubuntu
apt-get update
apt-get install libc6; apt-get install libc-bin

```
2. 重启服务
由于本次漏洞为glibc的漏洞，涉及多种应用程序，最安全并且推荐的修复方法是重启系统生效。
如果你的系统无法重启，请执行如下命令查询仍然在使用老版本glibc的程序。
```
lsof +c0 -d DEL | awk 'NR==1 || /libc-/ {print $2,$1,$4,$NF}' | column -t
```
根据查询的结果, 识别哪些是对外提供服务的程序，重启对应的服务。

## 解决 ##
公司大部分服务器都是centos 6.x和7.x ，CentOS 社区也在2016年2月17日 更新了最新的glibc版本，那么升级起来就很方便了，写了个升级脚本，内容如下，先让脚本跑一会。
```
cat repair_glibc.sh 
#!/bin/bash
######################################################
## Title:  Repair glibc getaddrinfo() Bug 18665     ##
## Version: 1.0                                     ##
## Date: 2016-02-18                                 ##
## Author: Charlie.Cui                              ##
## License: General Public License (GPL)            ##
## Copyright© 2015, Charlie.Cui All Rights Reserved ##
######################################################

system=`cat /etc/redhat-release| awk '{print $1}'`
release=`rpm -qa | grep ^kernel-[0-9] |head -n 1 | awk -F'.' '{print $4}'`
glibc_version=`rpm -qa glibc`
FRed="\E[31;40m"; FGreen="\E[32;40m"; FBlue="\E[34;40m"; St0="\033[1m"; St1="\033[5m"; Ed="\033[0m" 

# el6 Update glibc
el6() {
wget http://172.16.6.18/resource/files/CentOS6.x/local_mirror.repo -O /etc/yum.repos.d/local_mirror.repo
wget http://172.16.6.18/resource/files/CentOS6.x/epel.repo -O /etc/yum.repos.d/epel.repo
yum clean all;yum makecache
yum update glibc -y
if [ $glibc_version = glibc-2.12-1.166.el6_7.7.x86_64 ];then
  echo -e " $FGreen $glibc_version Update Sucesed! $Ed"
else 
  echo -e " $FRed $glibc_version Update Faild! $Ed"
fi
}

# el7 Update glibc
el7() {
wget http://172.16.6.18/resource/files/CentOS7.x/local_mirror.repo -O /etc/yum.repos.d/local_mirror.repo
wget http://172.16.6.18/resource/files/CentOS7.x/epel.repo -O /etc/yum.repos.d/epel.repo
yum clean all;yum makecache
yum update glibc -y
if [ $glibc_version = glbc-2.17-106.el7_2.4.x86_64 ];then
  echo -e " $FGreen $glibc_version Update Sucesed! $Ed"
else 
  echo -e " $FRed $glibc_version Update Faild! $Ed"
fi
}

# Check System 
if [ $system = CentOS ];then
  echo -e "$FGreen This System Version Is: $system continue update glibc version... $Ed"
  # Check release
  if [ $release = el6 ];then
    if [ `rpm -qa glibc` = glibc-2.12-1.166.el6_7.7.x86_64 ];then
      echo -e " $FGreen $glibc_version is the latest version $Ed"
    else 
      el6
    fi
  elif [ $release = el7 ];then
    if [ `rpm -qa glibc` = glibc-2.17-106.el7_2.4.x86_64 ];then
      echo -e " $FGreen $glibc_version is the latest version $Ed"
    else
      el7
    fi
  else 
    echo -e "$FRed Unknow Error $Ed"
    exit;
  fi
else
  echo -e "$FRed This System Version Is Not CentOS $Ed"
  exit;
fi
```
