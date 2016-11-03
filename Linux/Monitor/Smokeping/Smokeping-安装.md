### Smokeping 监控网络质量

#### 什么是Smokeping

Smokeping是 rrdtool 的作者 Tobi Oetiker 的作品，所以它在图形显示方面有很大优势，也是一个很有特点的 opensource 工具：
* 多种探测方式，包括 fping、echoping、dig、curl 等；
* 易用可扩展的插件；master/slave 的工作方式，可以在多个节点收集同一个监测点的数据；
* 很有特色的 alert 设置，不只是简单的设置一个阀值。

#### Smokeping架构组件
smokeping 是一个用 perl 写的程序，所以不需要安装，但是他需要使用一些工具。Smokeping 有以下组件组成：RRDtool、Fping、Echoping、Curl、Dig、SSh、Perl 模块，Perl、FCGI、Apache 等。

#### Smokeping 相关资源
* Smokeping官方网站：[http://oss.oetiker.ch/smokeping/](http://oss.oetiker.ch/smokeping/)
* Smokeping官方文档：[http://oss.oetiker.ch/smokeping/doc/index.en.html](http://oss.oetiker.ch/smokeping/doc/index.en.html)

### 安装Smokeping

#### 安装RRDTOOL

  RRDTool 是由Tobias Oetiker 开发的开源软件，它使用RRD（Round Rebin Databases）作为存储格式，Round robin 是一种处理定量数据以及当前元素指针的技术，RRDTool 主要用来跟踪对象的变化情况，生成改对象变化的趋势图。
 
    
  依赖软件包：
```
yum install cairo-devel libxml2-devel pango-devel pango libpng-devel freetype freetype-devel libart_lgpl-devel libidn libidn-devel httpd httpd-devel apr-util-devel apr-devel -y
```

如果nginx作为webserver，则要安装perl模块`perl-Net-Telnet perl-Net-DNS perl-LDAP perl-CGI-SpeedyCGI perl-libwww-perl perl-RadiusPerl perl-IO-Socket-SSL perl-Socket`


执行安装
```
wget http://oss.oetiker.ch/rrdtool/pub/rrdtool-1.4.7.tar.gz
tar -zxf rrdtool-1.4.7.tar.gz
cd rrdtool-1.4.7
./configure --prefix=/usr/local/rrdtool
make && make install
```

 检验安装是否成功：
```
/usr/local/rrdtool/bin/rrdtool
RRDtool 1.4.7  Copyright 1997-2012 by Tobias Oetiker 
               Compiled May 21 2013 13:42:05
 
Usage: rrdtool [options] command command_options
Valid commands: create, update, updatev, graph, graphv,  dump, restore,
                last, lastupdate, first, info, fetch, tune,
                resize, xport, flushcached
 
RRDtool is distributed under the Terms of the GNU General
Public License Version 2. (www.gnu.org/copyleft/gpl.html)
 
For more information read the RRD manpages
```
执行命令如果出现以上输出，表示安装成功，并列出了使用该命令的帮助信息。


#### 安装fping
```
wget http://oss.oetiker.ch/smokeping/pub/fping-2.4b2_to3-ipv6.tar.gz
tar -zxf fping-2.4b2_to3-ipv6.tar.gz
cd fping-2.4b2_to3-ipv6
./configure
make && make install
```

#### 安装echoping
```
wget http://sourceforge.net/projects/echoping/files/latest/download
tar -zxf echoping-6.0.2.tar.gz
cd echoping-6.0.2
./configure
make && make install
```

#### 安装fcgi
```
wget http://cpan.communilink.net/authors/id/F/FL/FLORA/FCGI-0.74.tar.gz
tar -zxf FCGI-0.74.tar.gz
cd FCGI-0.74
perl Makefile.PL
make && make install
```

#### 安装mod_fastcgi

```
wget http://www.fastcgi.com/dist/mod_fastcgi-2.4.6.tar.gz
tar zxf mod_fastcgi-2.4.6.tar.gz
cd mod_fastcgi-2.4.6
	apxs -o mod_fastcgi.so -c *.c
apxs -i -a -n fastcgi .libs/mod_fastcgi.so
确保httpd.conf有如下配置：
LoadModule fastcgi_module     /usr/lib/httpd/modules/mod_fastcgi.so
```
如果apache为源码安装
```
wget http://www.fastcgi.com/dist/mod_fastcgi-2.4.6.tar.gz
tar -zxf mod_fastcgi-2.4.6.tar.gz
cd mod_fastcgi-2.4.6
cp Makefile.AP2 Makefile
make top_dir=/usr/local/apache
make install top_dir=/usr/local/apache
```

#### 安装smokeping
```
wget http://oss.oetiker.ch/smokeping/pub/smokeping-2.6.9.tar.gz
tar -zxf smokeping-2.6.9.tar.gz
cd smokeping-2.6.9
./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib/perl5/
```
报错
```
checking checking for gnu make availablility... /usr/bin/gmake is GNU make
checking checking for perl module 'RRDs'... Failed
checking checking for perl module 'FCGI'... Ok
checking checking for perl module 'CGI'... Ok
checking checking for perl module 'CGI::Fast'... Ok
checking checking for perl module 'Config::Grammar'... Failed
checking checking for perl module 'Digest::HMAC_MD5'... Ok
checking checking for perl module 'LWP'... Ok
```
解决
```
 ./setup/build-perl-modules.sh /usr/local/smokeping/thirdparty
```
或者`yum –y install perl-[FAIL-MOUDLES]`
 
报错
```
checking checking for perl module 'RRDs'... Failed
```
解决
```
32位：
ln -s /usr/local/rrdtool/lib/perl/5.10.1/i386-linux-thread-multi/RRDs.pm /usr/lib/perl5/
ln -s /usr/local/rrdtool/lib/perl/5.10.1/i386-linux-thread-multi/auto/RRDs/RRDs.so /usr/lib/perl5/
 64位：
ln -s /usr/local/rrdtool/lib/perl/5.10.1/x86_64-linux-thread-multi/RRDs.pm /usr/lib64/perl5/
ln -s /usr/local/rrdtool/lib/perl/5.10.1/x86_64-linux-thread-multi/auto/RRDs/RRDs.so /usr/lib64//perl5/
```

在执行下面操作，完成安装
```
make clean
./configure –prefix=/usr/local/smokeping
/usr/bin/gmake install
```

### 配置smokeping

#### 修改相关文件
```
/usr/local/smokeping/bin/smokeping
/usr/local/smokeping/bin/smokeping_cgi
将第八行         use lib qw(); # PERL5LIB
修改为：         use lib qw(/usr/local/rrdtool/lib/perl); # PERL5LIB
 
/usr/local/smokeping/htdocs/smokeping.fcgi.dist：
mv /usr/local/smokeping/htdocs/smokeping.fcgi.dist /usr/local/smokeping/htdocs/smokeping.fcgi
 
进入 /usr/local/smokeping/etc
mv config.dist config
mv basepage.html.dist basepage.html
mv smokemail.dist smokemail
mv tmail.dist tmail
mv smokeping_secrets.dist smokeping_secrets
```

#### 修改主配置config

````
*** General ***                                                         ##全局配置
owner    = charlie.cui@zerounix.com                                          ##联系人（显示在网页上）
contact  = charlie.cui@zerounix.com                                         ##联系人邮箱
mailhost = mail.zerounix.com                                                ##邮件服务主机
sendmail = /usr/sbin/sendmail                                           ##发送邮件件的二进制可执行程序
# NOTE: do not put the Image Cache below cgi-bin
# since all files under cgi-bin will be executed ... this is not
# good for images.
imgcache = /usr/local/smokeping/cache                                   ##生成图片的缓存
imgurl   = cache                                                ##cache 定义cgi程序显示图片的url目录
datadir  = /usr/local/smokeping/data                                    ##rrd文件的位置
piddir  = /usr/local/smokeping/var
cgiurl   = http://some.url/smokeping.cgi                        ##smokeping访问地址
smokemail = /usr/local/smokeping/etc/smokemail                          ##发送邮件的邮件内容模板
tmail = /usr/local/smokeping/etc/tmail                                  ##HTML邮件模板的路径
# specify this to get syslog logging
syslogfacility = local0                                                 ##syslog日志记录的设备编号
# each probe is now run in its own process
# disable this to revert to the old behaviour
# concurrentprobes = no
 
*** Alerts ***                                                          ##报警配置
to =  monitor@zerounix.com                                    
from = mon@zerounix.com
 
+网络中断
type = rtt
pattern = !=U,==U
comment = 网络中断
priority = 1
 
+中断恢复
type = rtt
pattern = ==U,!=U,!=U
comment = 中断恢复
priority = 2
 
+严重丢包
type = loss
pattern = >50%
comment = 丢包大于50%
priority = 3
 
+丢包报警
type = loss
pattern = >10%,>10%,>10%
comment = 连续3次丢包10%以上
priority = 4
 
+网络延迟
type = rtt
pattern = >180,>180,>180
comment = 连续3次延时180以上
priority = 5
 
 
*** Database ***
 
step     = 60
pings    = 10
 
# consfn mrhb steps total
 
AVERAGE  0.5   1  1008
AVERAGE  0.5  12  4320
    MIN  0.5  12  4320
    MAX  0.5  12  4320
AVERAGE  0.5 144   720
    MAX  0.5 144   720
    MIN  0.5 144   720
 
*** Presentation ***
 
template = /usr/local/smokeping/etc/basepage.html
 
+ charts
 
menu = Charts
title = The most interesting destinations
 
++ stddev
sorter = StdDev(entries=>4)
title = Top Standard Deviation
menu = Std Deviation
format = Standard Deviation %f
 
++ max
sorter = Max(entries=>5)
title = Top Max Roundtrip Time
menu = by Max
format = Max Roundtrip Time %f seconds
 
++ loss
sorter = Loss(entries=>5)
title = Top Packet Loss
menu = Loss
format = Packets Lost %f
 
++ median
sorter = Median(entries=>5)
title = Top Median Roundtrip Time
menu = by Median
format = Median RTT %f seconds
 
+ overview
 
width = 600
height = 50
range = 10h
 
+ detail
 
width = 600
height = 200
unison_tolerance = 2
 
"Last 3 Hours"    3h
"Last 30 Hours"   30h
"Last 10 Days"    10d
"Last 400 Days"   400d
 
#+ hierarchies
#++ owner
#title = Host Owner
#++ location
#title = Location
 
*** Probes ***
 
+ FPing
 
binary = /usr/local/sbin/fping
 
+ DNS
binary = /usr/bin/dig
lookup = name.example
*** Slaves ***
secrets=/usr/local/smokeping/etc/smokeping_secrets
+boomer
display_name=boomer
color=0000ff
 
+slave2
display_name=another
color=00ff00
 
*** Targets ***
 
probe = FPing
 
menu = Top
title = Network Latency Grapher
remark = Welcome to the SmokePing website of xxx Company. \
         Here you will learn all about the latency of our network.
 
+ Test
menu= Targets
#parents = owner:/Test/James location:/
 
++ James
 
menu = James
title =James
alerts = someloss
slaves = boomer slave2
host = james.address
 
++ MultiHost
 
menu = Multihost
title = James and James as seen from Boomer
host = /Test/James /Test/James~boomer
```

监控主机是分层结构，用+表示
例如第一层“+”，第二层“++”一次类推
 
master/slave的方式，后面会介绍。

#### 修改其他配置
 
根据配置文件所写的，创建数据文件目录：
```
mkdir /usr/local/smokeping/{htdocs/var,cache,data}
```
 
修改数据文件目录的属主及属组
```
chown nobody:nobody /usr/local/smokeping/{htdocs/var,cache,data}
```
 
`/usr/local/smokeping/etc/smokeping_secrets`这个文件存放的是`master/slave`之间的验证密码，现在暂时不用
 
#### 启动smokeping
```
sudo -u nobody /usr/local/smokeping/bin/smokeping --logfile=/var/log/smokeping.log --restart
```

报错：`ERROR: FPing must be installed setuid root or it will not work
 at (eval 29) line 1`
解决
```
whereis fping
fping: /usr/local/sbin/fping
chmod +s /usr/local/sbin/fping
```

#### 配置apache的配置文件
```shell
Alias /ping /usr/local/smokeping/htdocs/
<Directory "/usr/local/smokeping/htdocs">
       DirectoryIndex index.html smokeping.fcgi
       Options FollowSymLinks ExecCGI
       AllowOverride None
       AddHandler cgi-script .cgi .fcgi
       Order allow,deny
       Allow from all
       AuthName "Smokeping Access"
       AuthType Basic
       AuthUserFile /usr/local/smokeping/htdocs/htpasswd.user
       Require valid-user
</Directory>
```

### FAQ
不出图解决思路

* 使用--debug方式启动smokeping，排查错误
* 查看smokeping的log
* 查看apache的error.log
* 查看文件权限，包括数据文件目录及数据文件，apache和smokeping的启动用户，rrd文件是否有数据