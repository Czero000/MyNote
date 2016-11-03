  pptpd的日志主要大部分都在/var/log/messages, /var/log/daemon等文件里面，但是仔细看了发现里面没有用户名，不知道用户是用了哪一个帐号登录上来的。于是就看了一下pppd的man，里面发现了一些环境变量如：IPLOCAL, IPREMOTE等，经过测试发现 PEERNAME就是用户名，这样在/etc/ppp/ip-up和/etc/ppp/ip-down里面记录一下就可以了，另外没有发现用户的ip。后来发现pppd是spawn出一个子进程来控制pptpd连接的，子进程的命令行里面已经带有了用户的ip，经过多次试验，发现ip-up被调用的时候是有命令行参数的，$6就是用户ip，于是在ip-up里面手工用echo命令写了一下，算是pptpd的比较完整日志，里面有时间，有来源ip，有用户名，有被分配的ppp的ip等
 在`/etc/ppp/ip-up`和`/etc/ppp/ip-down`中加入脚本
```
echo "time: `date -d today +%F_%T`" >> /var/log/pptpd.log  
echo "clientIP: $6" >> /var/log/pptpd.log  
echo "username: $PEERNAME" >> /var/log/pptpd.log  
echo "device: $1" >> /var/log/pptpd.log  
echo "vpnIP: $4" >> /var/log/pptpd.log  
echo "assignIP: $5" >> /var/log/pptpd.log 
```
