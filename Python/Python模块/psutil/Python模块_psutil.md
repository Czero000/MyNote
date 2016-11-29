# 系统性能信息模块--psutil
    psutil是一个跨平台库,能够实现获取系统运行程序和系统利用率(CPU、内存、磁盘、网络、用户)，主要用于监控系统、性能分析、进程管理。可以实现ps、top、lsof、netstat、ifconfig、who、df、 kill、free、nice、ionice、iostat、iotop、uptime、pidof、tty、taskset、pmap命令功能，支持的系统有Linux, Windows, OSX, FreeBSD and Sun Solaris，32和64位系统都支持，同时支持pyhton2.6到3.5

- 官网地址为：[http://pythonhosted.org/psutil/](http://pythonhosted.org/psutil/) （文档上有详细的api）
- github地址为：[https://github.com/giampaolo/psutil/](https://github.com/giampaolo/psutil/)

# 下载安装psutil
[官网下载地址]：https://pypi.python.org/pypi/psutil#downloads

- Ubuntu、Debian

```shell
sudo apt-get install gcc python-devel
pip install psutil
```

- RedHat、CentOS

```shell
yum install gcc python-devel python-pip
pip install psutil
```

- 源码安装

```shell
tar -zxf psutil-4.3.0.tar.gz & cd psutil-4.3.0
python setup.py install
```

# 获取系统性能信息
采集系统的基本信息包括CPU、内存、磁盘、网络等，可以完整描述当前系统的运行状态及质量。psutil模块已经封装了很多方法，用户可以根据应用场景，调用相应的方法来满足需求。

## CPU信息
Linux操作系统CPU利用率有以下部分：
- User time，执行用户进程的时间百分比
- System times，执行内核进程和中断的时间百分比
- Wait io，由于io等待而是CPU处于idle状态的时间百分比
- Idle，cpu处于idle状态的时间百分比

可以使用Python的psutil.cpu_times()方法得到上面信息

```python
>>> import psutil                 #加载模块
>>> psutil.cpu_times()            #使用cpu_times方法获取CPU完整信息
scputimes(user=507021.98, nice=28.69, system=143507.66, idle=62107633.21, iowait=203.93, irq=0.3, softirq=987.58, steal=8027.35, guest=0.0, guest_nice=0.0)

>>> psutil.cpu_times(percpu=True)     #指定方法变量percpu=True，获取所有cpu信息
[scputimes(user=64266.12, nice=5.24, system=17882.09, idle=7758087.66, iowait=38.64, irq=0.01, softirq=622.19, steal=1394.21, guest=0.0, guest_nice=0.0), scputimes(user=47351.6, nice=4.53, system=14771.42, idle=7779416.44, iowait=31.22, irq=0.0, softirq=147.85, steal=1165.37, guest=0.0, guest_nice=0.0), scputimes(user=45731.81, nice=3.47, system=14174.38, idle=7785751.62, iowait=31.35, irq=0.0, softirq=5.14, steal=942.39, guest=0.0, guest_nice=0.0), scputimes(user=59921.91, nice=2.82, system=16358.87, idle=7769122.46, iowait=26.79, irq=0.1, softirq=21.33, steal=981.62, guest=0.0, guest_nice=0.0), scputimes(user=61618.43, nice=3.21, system=17520.64, idle=7769826.77, iowait=23.5, irq=0.0, softirq=2.29, steal=747.6, guest=0.0, guest_nice=0.0), scputimes(user=72698.55, nice=3.22, system=20959.17, idle=7755390.1, iowait=18.22, irq=0.0, softirq=1.87, steal=729.66, guest=0.0, guest_nice=0.0), scputimes(user=77419.64, nice=1.99, system=21197.0, idle=7740338.57, iowait=9.52, irq=0.17, softirq=172.94, steal=1315.78, guest=0.0, guest_nice=0.0), scputimes(user=78021.53, nice=4.18, system=20646.29, idle=7750652.03, iowait=24.65, irq=0.0, softirq=13.95, steal=750.81, guest=0.0, guest_nice=0.0)]

>>> psutil.cpu_times().user         #获取单项数据信息
507037.32

>>> psutil.cpu_count()              #CPU的逻辑个数，默认logical=True
8

>>> psutil.cpu_count(logical=False) #获取CPU的物理个数
8

>>> for x  in range(8):             #cpu使用率，间隔时间为一秒，                 
...     psutil.cpu_percent(interval=1,percpu=True)
... 
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[0.0, 0.0, 8.0, 0.0, 1.0, 0.0, 0.0, 0.0]
[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[8.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

>>> for x  in range(5):                    #5秒内，cpu信息        
...     psutil.cpu_times_percent(interval=1, percpu=False)
... 
scputimes(user=0.0, nice=0.0, system=0.0, idle=100.0, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
scputimes(user=0.7, nice=0.0, system=0.2, idle=99.0, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
scputimes(user=0.0, nice=0.0, system=0.0, idle=100.0, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
scputimes(user=0.0, nice=0.0, system=0.0, idle=100.0, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
scputimes(user=1.0, nice=0.0, system=0.1, idle=98.9, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
```

## 内存信息
Linux系统的内存利用率信息包含total（内存总数）、userd（已使用的内存数）、free（空闲内存数）、buffers（缓冲使用数）、cache（缓存使用数）、swap（交换分区使用数）等，可以使用`psutil.virtual_memory()`和`psutil.swap.memory()`方法获取信息。
```python
>>> psutil.virtual_memory()                    #内存完整信息
svmem(total=8203100160L, available=7477055488L, percent=8.9, used=2860314624L, free=5342785536L, active=1288581120, inactive=907857920, buffers=712704L, cached=2133557248)

>>> psutil.virtual_memory().buffers             #内存单项信息
712704L

>>> psutil.swap_memory()                        #swap内存信息
sswap(total=4294963200L, used=0L, free=4294963200L, percent=0.0, sin=0, sout=0)
```

## 磁盘信息
在系统的所有磁盘信息中，对磁盘利用率和I/O信息更加关注，其中磁盘利用率使用`psutil.disk_usage`方法获取。磁盘I/O信息包括`read_count`（读IO数）、`write_count`（写IO数）、`read_bytes`（IO读字节数）、`write_bytes`（IO写字节数）、`read_time`(磁盘读时间)、`write_time`（磁盘写时间）等，这些I/O信息可以使用`psutil.disk_io_counters()`获取。

```python
>>> psutil.disk_partitions()       #获取磁盘完整信息
[sdiskpart(device='/dev/vda5', mountpoint='/', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota'), sdiskpart(device='/dev/vda3', mountpoint='/var', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota'), sdiskpart(device='/dev/vda1', mountpoint='/boot', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota')]

>>> psutil.disk_usage('/')        #获取分区信息
sdiskusage(total=205846061056, used=3637903360, free=202208157696, percent=1.8)

>>> psutil.disk_io_counters()     #磁盘IO总数
sdiskio(read_count=16559, write_count=2009810, read_bytes=404972544, write_bytes=12419297280, read_time=114481, write_time=51731850)

>>> psutil.disk_io_counters(perdisk=False)  #磁盘IO信息
iostat(read_count=59622, write_count=16312, read_bytes=862336000, write_bytes=636302336, read_time=591520, write_time=245236)

>>> psutil.disk_io_counters(perdisk=True)    #获取单个分区IO数
{'vda5': sdiskio(read_count=11785, write_count=775923, read_bytes=278560768, write_bytes=5013288448, read_time=79238, write_time=29957220), 'vda4': sdiskio(read_count=5, write_count=0, read_bytes=14336, write_bytes=0, read_time=13, write_time=0), 'vda1': sdiskio(read_count=1175, write_count=1112, read_bytes=26194432, write_bytes=2294784, read_time=4332, write_time=1751), 'vda3': sdiskio(read_count=3393, write_count=1232791, read_bytes=99379712, write_bytes=7403784704, read_time=30185, write_time=21773070), 'vda2': sdiskio(read_count=201, write_count=0, read_bytes=823296, write_bytes=0, read_time=713, write_time=0)}
```

## 网络信息
系统的网络信息和磁盘IO信息类似，涉及到几个关键点，包含`bytes_sent`(发送字节数)、`bytes_recv=28220119`(接受字节数)、`packets_sent=200978`(发送数据包数量)、`packets_recv=212672`(接收数据包数量),这些信息可以使用`psutil.net_io_counters()`方法获取。

```python 
>>> psutil.net_io_counters()      #网络IO信息
iostat(bytes_sent=3489439, bytes_recv=23439122, packets_sent=34900, packets_recv=139300, errin=0, errout=0, dropin=5579, dropout=0)
>>> psutil.net_io_counters(pernic=True)   #各个网络接口IO信息
{'lo': iostat(bytes_sent=27015, bytes_recv=27015, packets_sent=330, packets_recv=330, errin=0, errout=0, dropin=0, dropout=0), 'eth0': iostat(bytes_sent=3464728, bytes_recv=23423824, packets_sent=34592, packets_recv=139081, errin=0, errout=0, dropin=5580, dropout=0)}
>>> psutil.net_io_counters(pernic=False)

>>> psutil.net_connections()      #网络连接信息，可选选项'all', 'udp', 'tcp', 'unix', 'tcp6', 'tcp4', 'inet6', 'inet4', 'udp6', 'udp4', 'inet'
[sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 48895), raddr=('172.16.8.21', 3306), status='TIME_WAIT', pid=None), sconn(fd=23, family=10, type=2, laddr=('fe80::5054:ff:fec0:b2b3', 123), raddr=(), status='NONE', pid=565), sconn(fd=3, family=2, type=1, laddr=('0.0.0.0', 22), raddr=(), status='LISTEN', pid=891), sconn(fd=18, family=2, type=2, laddr=('127.0.0.1', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 37089), raddr=('172.16.8.47', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('42.62.9.210', 46794), raddr=('124.167.232.94', 80), status='TIME_WAIT', pid=None), sconn(fd=21, family=2, type=2, laddr=('42.62.9.210', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 56979), raddr=('172.16.11.158', 3306), status='TIME_WAIT', pid=None), sconn(fd=6, family=2, type=2, laddr=('0.0.0.0', 57011), raddr=(), status='NONE', pid=514), sconn(fd=4, family=2, type=1, laddr=('172.16.11.210', 6379), raddr=(), status='LISTEN', pid=2271), sconn(fd=22, family=2, type=2, laddr=('172.16.11.210', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 41703), raddr=('172.16.1.51', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 37088), raddr=('172.16.8.47', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 51769), raddr=('172.16.11.222', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 34888), raddr=('172.16.18.227', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 58160), raddr=('172.16.254.135', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 55164), raddr=('172.16.254.195', 3306), status='TIME_WAIT', pid=None), sconn(fd=3, family=2, type=1, laddr=('42.62.9.210', 39493), raddr=('10.254.95.115', 3306), status='SYN_SENT', pid=26785), sconn(fd=3, family=2, type=1, laddr=('172.16.11.210', 52646), raddr=('172.16.4.9', 3306), status='SYN_SENT', pid=26761), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 56980), raddr=('172.16.11.158', 3306), status='TIME_WAIT', pid=None), sconn(fd=17, family=10, type=2, laddr=('::', 123), raddr=(), status='NONE', pid=565), sconn(fd=4, family=10, type=1, laddr=('::', 22), raddr=(), status='LISTEN', pid=891), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 51768), raddr=('172.16.11.222', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 48894), raddr=('172.16.8.21', 3306), status='TIME_WAIT', pid=None), sconn(fd=19, family=10, type=2, laddr=('::1', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 58155), raddr=('172.16.254.135', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 45734), raddr=('172.16.253.86', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 34889), raddr=('172.16.18.227', 3306), status='TIME_WAIT', pid=None), sconn(fd=16, family=2, type=2, laddr=('0.0.0.0', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 55185), raddr=('172.16.9.28', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 41582), raddr=('172.16.6.98', 3306), status='TIME_WAIT', pid=None), sconn(fd=24, family=10, type=2, laddr=('fe80::5054:ff:feee:c3c7', 123), raddr=(), status='NONE', pid=565), sconn(fd=-1, family=2, type=1, laddr=('42.62.9.210', 46795), raddr=('124.167.232.94', 80), status='TIME_WAIT', pid=None), sconn(fd=3, family=2, type=1, laddr=('172.16.11.210', 22), raddr=('172.16.3.131', 56774), status='ESTABLISHED', pid=9821), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 55162), raddr=('172.16.254.195', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 46726), raddr=('172.16.6.86', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 44082), raddr=('172.16.2.132', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 44081), raddr=('172.16.2.132', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 45733), raddr=('172.16.253.86', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 55186), raddr=('172.16.9.28', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 41704), raddr=('172.16.1.51', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 53921), raddr=('172.16.1.107', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 53922), raddr=('172.16.1.107', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 46727), raddr=('172.16.6.86', 3306), status='TIME_WAIT', pid=None), sconn(fd=-1, family=2, type=1, laddr=('172.16.11.210', 41584), raddr=('172.16.6.98', 3306), status='TIME_WAIT', pid=None)] 

>>> psutil.net_if_addrs()     # 网卡信息
{'lo': [snic(family=2, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None), snic(family=10, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None), snic(family=17, address='00:00:00:00:00:00', netmask=None, broadcast=None, ptp=None)], 'eth1': [snic(family=2, address='172.16.11.210', netmask='255.255.255.0', broadcast='172.16.11.255', ptp=None), snic(family=10, address='fe80::5054:ff:fec0:b2b3%eth1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snic(family=17, address='52:54:00:c0:b2:b3', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'eth0': [snic(family=2, address='xx.xx.xx.xx', netmask='255.255.255.0', broadcast='xx.xx.xx.xx', ptp=None), snic(family=10, address='fe80::5054:ff:feee:c3c7%eth0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snic(family=17, address='52:54:00:ee:c3:c7', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)]}

>>> psutil.net_if_stats()  #网卡物理信息
{'lo': snicstats(isup=True, duplex=0, speed=0, mtu=65536), 'eth1': snicstats(isup=True, duplex=0, speed=0, mtu=1500), 'eth0': snicstats(isup=True, duplex=0, speed=0, mtu=1500)}
```

## 其他系统信息
除了上面几种获取系统信息方法，psutil模块还可以获取用户登录，开机时间等信息。
```python 
>>> psutil.users()            #用户登录信息
[suser(name='root', terminal='pts/0', host='172.16.3.131', started=1466577408.0), suser(name='root', terminal='pts/1', host='172.16.3.131', started=1466577536.0), suser(name='root', terminal='pts/2', host='172.16.3.131', started=1466566272.0)]

>>> psutil.boot_time()       #获取开机时间，以linux时间戳方式返回
1459135266.0

>>> import datetime
>>> datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H: %M: %S")
'2016-03-28 11: 21: 06'
```

# 系统进程管理
获取当前系统的进程信息，可以让SA得知程序的运行状态，包括进程的启动时间、查看或设置CPU亲和度、内存使用率、IO信息、socket连接、线程数等。

## 进程信息
psutil模块在获取进程信息方面提供了支持，包括使用`psutil.pids()`方法获取所有进程的PID，使用`psutil.Process()`方法获取。
```python
>>> psutil.pids()            #列出当前系统所有进程PID
[1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36, 37, 38, 39, 41, 42, 43, 44, 46, 47, 48, 49, 51, 52, 53, 54, 56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 77, 78, 86, 88, 91, 111, 140, 295, 299, 300, 301, 302, 307, 318, 319, 320, 321, 322, 323, 324, 325, 330, 380, 381, 382, 391, 392, 402, 412, 419, 426, 470, 480, 481, 482, 483, 485, 486, 488, 489, 490, 491, 512, 514, 519, 527, 530, 537, 538, 539, 545, 565, 891, 3544, 4205, 4287, 4614, 5318, 9821, 9953, 11025, 12194, 16289, 16748, 18785, 21354, 23249, 23675, 23875, 24308, 24979, 25347, 25590, 25809, 26091, 28151, 28316, 29454, 30364, 31539, 32478]

>>> p = psutil.Process(29454)   #实例化一个Process对象
>>> p.name()                    #进程名称
'redis-server'

>>> p.exe()                      #进程bin路径
'/usr/bin/redis-server'

>>> p.cwd()                      #进程工作路径
'/var/lib/redis'

>>> p.status()                  #进程状态
'sleeping'

>>> p.create_time()             #进程创建时间
1467018142.41
>>> p.uids()                    #进程uid信息
puids(real=995, effective=995, saved=995)          
>>> p.gids()                    #进程gid信息
pgids(real=992, effective=992, saved=992)
>>> p.cpu_times()               #进程cpu时间信息
pcputimes(user=0.08, system=0.27)
>>> p.cpu_affinity()            #进程cpu亲和度
[0, 1, 2, 3, 4, 5, 6, 7]
>>> p.memory_percent()         #进程内存使用率
0.07100378986473328
>>> p.memory_info()             #进程rss、vms信息
pmem(rss=5824512, vms=146112512)
>>> p.io_counters()              #进程IO信息
pio(read_count=3844, write_count=14, read_bytes=0, write_bytes=4096)
>>> p.connections()              #打开进程socket的namedutples列表
[pconn(fd=4, family=2, type=1, laddr=('172.16.11.210', 6379), raddr=(), status='LISTEN')]
>>> p.num_threads()              #进程开启线程数           
3
>>> p.open_files()               #进程打开文件
[]
```

## popen类的使用
psutil提供的popen类的作用是获取用户启动的应用进程信息，以便跟踪程序进程的运行装。
```python 
>>> import psutil
>>> from subprocess import PIPE
>>> p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
>>> p.name()
'python'
>>> p.username()
'root'
>>> p.communicate()
('hello\n', None)
>>> p.cpu_times()
pcputimes(user=0.01, system=0.01)
```
