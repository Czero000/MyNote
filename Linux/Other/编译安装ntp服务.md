## 升级背景

### NTP服务漏洞
![NTP.BUG](https://czero000.github.io/ntp/ntp-bug.png)
>“未经过身份验证的攻击者能够迫使网络时间协议守护进程（ntpd）与恶意的时间服务器源进行同步，这样一来，攻击者就可以随意修改目标 系统的系统时间了。网络时间协议守护进程（ntpd）在处理某些经过加密的、没有得到应答的网络数据包时，会发生错误。”
总的来说，恶意攻击者能够迫使目标主机的网络时间协议守护进程（ntpd）与恶意的时间同步源进行同步，并且干扰目标系统的系统时钟。
除此之外，网络时间协议守护进程（ntpd）也可以与特定类型的同步请求进行响应。
根据思科Talos安全情报研究团队的描述：“在大多数的配置文件下，如果网络时间协议守护进程（ntpd）接收到了这样的一个数据包，如果网络时间协议守 护进程（ntpd）能够验证这个数据包的有效性，那么它就会让计算机与请求的发送端建立一个短暂的链接。比如说，当网络时间协议守护进程（ntpd）接收 到一个请求数据包时，ntpd会对数据包的有效性进行一系列的检测。” 在某些操作系统中，恶意地更改系统时间将会带来非常严重的影响，攻击者可以利用这一漏洞来实现：
* 利用过期的账号和密码进行身份验证；
* 让TLS客户端接收已经过期作废的证书，并拒绝当前有效的证书；
* 绕过现代Web安全防御机制，例如证书绑定以及HTTP安全传输机制；
* 强制刷新缓存系统中的缓存数据，从而导致系统性能显著下降，例如DNS和CDN等；
* 攻击基于物理的实时网络系统；

### 谁将受到这些问题的影响？
>这一漏洞将会影响ntp 4.2.8p3，正如Talos团队的专家所述，这一漏洞早在2009年的ntp 4.2.5p186版本中就已经存在了。
因此，在所有ntp-4发行版的版本中，4.2.5p186至4.2.8p3版本的ntp都存在这一漏洞。在所有ntp－4开发版的版本中，4.3.0至4.3.76版本的ntp也存在这一漏洞。除此之外，所有整合了上述版本ntpd的产品也将会受到这一漏洞的影响。
除此之外，Talos安全情报研究团队的专家们还发现了下列漏洞：


* 整型溢出将引起守护进程的崩溃；
* NTP的密码管理器中存在一个用后释放（UAF）漏洞和一个缓冲区溢出漏洞；
* 一个VMS目录遍历漏洞；
* NTPQ中的一个漏洞；
* 远程攻击者可以向目标主机发送一个恶意的配置文件，从而对目标主机发动拒绝服务（DoS）攻击；
* 守护进程中存在一个缓冲区溢出漏洞；

NTP项目小组建议广大用户应当尽快安装ntp-4.2.8p4来修复这一问题，并且采用BCP 38数据包输入输出过滤。

## 升级步骤
### 系统环境
测试主机：CentOS release 6.5 (Final) i386

### 卸载系统自带软件

```
rpm -qa ntp
ntp-4.2.6p5-1.el6.centos.i686
rpm -e ntp-4.2.6p5-1.el6.centos.i686 --nodeps
warning: /etc/ntp.conf saved as /etc/ntp.conf.rpmsave
```

### 下载软件源码
```
wget http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/ntp-4.2.8p4.tar.gz
```

### 安装NTP
```
tar -zxf ntp-4.2.8p4.tar.gz 
cd ntp-4.2.8p4
./configure --enable-all-clocks --enable-parse-clocks --enable-linuxcaps 
make && make install 
```
### 配置NTP
```
cat /etc/ntp.conf         
# For more information about this file, see the man pages
# ntp.conf(5), ntp_acc(5), ntp_auth(5), ntp_clock(5), ntp_misc(5), ntp_mon(5).

driftfile /var/lib/ntp/drift

# Permit time synchronization with our time source, but do not
# permit the source to query or modify the service on this system.
restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery

# Permit all access over the loopback interface.  This could
# be tightened as well, but to do so would effect some of
# the administrative functions.
restrict 127.0.0.1 
restrict -6 ::1

# Hosts on local network are less restricted.
restrict 172.16.0.0 mask 255.255.0.0 nomodify notrap

# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
server 3.cn.pool.ntp.org perfer  
server 1.cn.pool.ntp.org
server 0.asia.pool.ntp.org

#broadcast 192.168.1.255 autokey        # broadcast server
#broadcastclient                        # broadcast client
#broadcast 224.0.1.1 autokey            # multicast server
#multicastclient 224.0.1.1              # multicast client
#manycastserver 239.255.254.254         # manycast server
#manycastclient 239.255.254.254 autokey # manycast client

restrict 3.cn.pool.ntp.org nomodify notrap noquery
restrict 1.cn.pool.ntp.org nomodify notrap noquery
restrict 0.asia.pool.ntp.org nomodify notrap noquery


server  127.127.1.0     # local clock
fudge   127.127.1.0 stratum 10

# Enable public key cryptography.
#crypto

includefile /etc/ntp/crypto/pw

# Key file containing the keys and key identifiers used when operating
# with symmetric key cryptography. 
keys /etc/ntp/keys

# Specify the key identifiers which are trusted.
#trustedkey 4 8 42

# Specify the key identifier to use with the ntpdc utility.
#requestkey 8

# Specify the key identifier to use with the ntpq utility.
#controlkey 8

# Enable writing of statistics records.
#statistics clockstats cryptostats loopstats peerstats

```

### 启动NTP
```
/usr/local/ntp/bin/ntpd -c /etc/ntp.conf
```
### 增加启动脚本
```
#!/bin/sh
# ntpd          This shell script takes care of starting and stopping
#               ntpd (NTPv4 daemon).
#
# chkconfig: - 58 74
# description: ntpd is the NTPv4 daemon. \
# The Network Time Protocol (NTP) is used to synchronize the time of \
# a computer client or server to another server or reference time source, \
# such as a radio or satellite receiver or modem.

NTPD=/usr/local/bin/ntpd
PIDFILE=/var/run/ntpd.pid
USER=ntp
GROUP=ntp
NTPD_OPTS="-g -u ntp:ntp -p $PIDFILE"

ntpd_start() {
    if [ -r $PIDFILE ]; then
        echo "ntpd seems to be already running under pid `cat $PIDFILE`."
        echo "Delete $PIDFILE if this is not the case.";
        return 1;
    fi
    echo -n "Starting NTP daemon... "

    $NTPD $NTPD_OPTS

    # You can't always rely on the ntpd exit code, see Bug #2420
    # case "$?" in
    #     0) echo "OK!"
    #         return 0;;
    #     *) echo "FAILED!"
    #         return 1;;
    # esac

    sleep 1

    if ps -Ao args|grep -q "^$NTPD $NTPD_OPTS"; then
        echo "OK!"
        return 0
    else
        echo "FAILED!"
        [ -e $PIDFILE ] && rm $PIDFILE
        return 1
    fi
}

ntpd_stop() {
    if [ ! -r $PIDFILE ]; then
        echo "ntpd doesn't seem to be running, cannot read the pid file."
        return 1;
    fi
    echo -n "Stopping NTP daemon...";
    PID=`cat $PIDFILE`

    if kill -TERM $PID 2> /dev/null;then
        # Give ntp 15 seconds to exit
        for i in `seq 1 15`; do
            if [ -n "`ps -p $PID|grep -v PID`" ]; then
                echo -n .
                sleep 1
            else
                echo " OK!"
                rm $PIDFILE
                return 0
            fi
        done
    fi

    echo " FAILED! ntpd is still running";
    return 1
}

ntpd_status() {
    if [ -r $PIDFILE ]; then
        echo "NTP daemon is running as `cat $PIDFILE`"
    else
        echo "NTP daemon is not running"
    fi
}

case "$1" in
    'start')
        ntpd_start
        ;;
    'stop')
        ntpd_stop
        ;;
    'restart')
        ntpd_stop && ntpd_start
        ;;
    'status')
        ntpd_status
        ;;
    *)
        echo "Usage: $0 (start|stop|restart|status)"
esac
```
