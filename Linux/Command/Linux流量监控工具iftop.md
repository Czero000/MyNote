在类unix系统中，大家熟悉的top命令可以查看系统资源、进程、内存占用等信息，且动态实时显示。要查看网络状态可以使用netstat、nmap等工具。若要查看实时的网络流量，监控TCP/IP连接等，则可以使用iftop。

#### iftop简介
类似于top的实时监控系统资源和进程等，iftop是一个实时流量监控工具。iftop可以用来监控网卡的实时流量（可以指定网段）、反向解析IP、显示端口信息等。

#### 安装iftop
```
Debian系统 运行：apt-get install iftop
CentOS系统 运行：yum install iftop
```


#### 详解
```
界面上面显示的是类似刻度尺的刻度范围，为显示流量图形的长条作标尺用的。

中间的 这两个左右箭头，表示的是流量的方向。
TX：发送流量
RX：接收流量
TOTAL：总流量
Cumm：运行iftop到目前时间的总流量
peak：流量峰值
rates：分别表示过去 2s 10s 40s 的平均流量
```

#### 参数
```
-h                  display this message                                       
-n                  don't do hostname lookups                                  
-N                  don't convert port numbers to services                     
-p                  run in promiscuous mode (show traffic between other
	                           hosts on the same network segment)
-b                  don't display a bar graph of traffic
-B                  Display bandwidth in bytes
-i interface        listen on named interface
-f filter code      use filter code to select packets to count
				    (default: none, but only IP packets are counted)
-F net/mask         show traffic flows in/out of IPv4 network
-G net6/mask6       show traffic flows in/out of IPv6 network
-l                  display and count link-local IPv6 traffic (default: off)
-P                  show ports as well as hosts
-m limit            sets the upper limit for the bandwidth scale
-c config file      specifies an alternative configuration file
-t                  use text interface without ncurses

Sorting orders:
-o 2s                Sort by first column (2s traffic average)
-o 10s               Sort by second column (10s traffic average) [default]
-o 40s               Sort by third column (40s traffic average)
-o source            Sort by source address
-o destination       Sort by destination address
The following options are only available in combination with -t
-s num              print one single text output afer num seconds, then quit
-L num              number of lines to print
														      ```
