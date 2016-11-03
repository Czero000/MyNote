## 什么是ShadowSocks  ##
>Shadowsocks 是一个安全的socks5代理，用于保护网络流量，是一个开源项目。通过客户端以指定的密码、加密方式和端口连接服务器，成功连接到服务器后，客户端在用户的电脑上构建一个本地socks5代理。使用时将流量分到本地socks5代理，客户端将自动加密并转发流量到服务器，服务器以同样的加密方式将流量回传给客户端，以此实现代理上网。其流行起来的一大原因，多亏了国内不科学的防火长城和某些地区的SSH Tunnel连接被禁用。

## Shadowsocks优势 ##

* 如前面所说，使用SSH来创建本地socks5代理的方法容易被发现，某些地区干脆进行了封锁，而Shadowsocks的代理方式更为隐蔽和安全。
* 无需保持实时连接，不用考虑断线问题。在使用SSH时，总会发生断开连接的情况，如网络不稳定、电脑休眠、切换wifi等，此时SSH连接将断开，浏览网页什么的会提示无法连接到代理服务器。虽然客户端大都支持断线重连，但是反应经常不太灵敏，平均需要30秒左右的时间（而且这个时间是从你点开网页开始算的）。如果你用的是手机的话，鉴于手机网络的多变性，人一旦动起来就几乎不可用了。
* 更丰富的客户端支持。目前Shadowsocks官网（是shadowsocks.org，不是.com那个，.com那个是售卖账号的，并非官网，有假冒官网的嫌疑）提供几乎全平台支持，包括linux和非越狱iPhone在内。尤其是OS X版的自动代理模式（PAC）非常稳定，胜过GoAgentX，完美支持safari。同时，各个平台上的客户端使用都十分简单，基本上就是填写一下地址端口密码什么的，就能开始使用了，连点击连接都不用。另外，大部分客户端支持扫描屏幕二维码完成配置，这个指导新手不要太爽。
[shadowsocks软件覆盖](https://shadowsocks.org/en/download/clients.html)
![shadowsocks](http://ofc9x1ccn.bkt.clouddn.com/system/proxy/shadowsocks-software.png "shadowsocks软件覆盖")

## 服务端 ##

### 安装ShadowSocks  ###

* shadowsocks开发语言有Node.JS、go、pthon、c
* shadowsocks python语言版 https://github.com/clowwindy/shadowsocks
* shadowsocks go语言版 https://github.com/hugozhu/shadowsocks-go
* shadowsocks nodejs语言版 https://github.com/clowwindy/shadowsocks-nodejs
* shadowsocks libev版（使用C语言+libev库+openssl开发） https://github.com/madeye/shadowsocks-libev
* shadowsocks libuv版（很久没更新了） https://github.com/dndx/shadowsocks-libuv

网上推荐安装python版和Shadowsocks-libev版，这里安装标准python版，系统为CentOS7。

#### 检查服务器python，确保python 版本高于2.6

```
python --version

Python 2.7.5
```

#### 安装依赖库 ####
```
yum -y install m2crypto python-setuptools
```

#### 安装PIP ####
```
yum -y install python-pip
或者
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

```

#### 安装Shadowsocks ####
```
pip install shadowsocks
```

### 配置ShadowSocks ###
安装ShadowSocks之后可以在后天直接启动``ssserver -p 8000 -k password -m rc4-md5 -d start
``
当然也可以使用配置文件进行配置，创建``/etc/shadowsocks/shadowsocks.json``文件，如下：
```
{
    "server":"my_server_ip",
    "server_port":8388,
    "local_port":1080,
    "password":"barfoo!",
    "timeout":600,
    "method":"table"
}

```

字段解释：
* server:         服务器ip地址(IPV4/IPV6)，即为端口监听ip        
* server_port：   Shadowsocks服务监听端口
* local_port：    本地端口
* password：      密码
* timeout         超时时间
* method          加密方法("bf-cfb", "aes-256-cfb", "des-cfb", "rc4")、默认为table，但是它并不安全，官方建议"aes-256-cfb"

shadowsockv 支持多端口多用户模式
```
{
  "server":"my_server_ip",
  "local_port":1080,
  "timeout":600,
  "method": "aes-256-cfb",
  "port_password":
  {
    "9123":"passwd1",
    "9124":"passwd2"
  }
  "_comment":
  {
    "9123":"hanmeimei",
    "9124":"lilei"
  }
}
```

### 启动Shadowsocks ###
```
 ssserver -c /etc/shadowsocks/shadowsocks.json -d start
INFO: loading config from /etc/shadowsocks/shadowsocks.json
2015-10-10 04:40:30 INFO     loading libcrypto from libcrypto.so.10
started
```
如果要停止Shadowsocks，将命令中``start``变更为``stop``即可

TIPS: 加密方式推荐使用``rc4-md5``，因为 RC4 比 AES 速度快好几倍，如果用在路由器上会带来显著性能提升。旧的 RC4 加密之所以不安全是因为 Shadowsocks 在每个连接上重复使用 key，没有使用 IV。现在已经重新正确实现，可以放心使用。更多可以看[issue](https://github.com/clowwindy/shadowsocks/issues/178)。


## 客户端安装 ##

### 下载客户端 ###
Shadowsocks官网下载链接：http://shadowsocks.org/en/download/clients.html
如果打不开官方下载地址，可以在这里下载（不能保证为最新版本）
* **Windows** [Windows 7 or above: 2.5.8.zip](https://czero000.github.io/upload/proxy/Shadowsocks-2.5.8.zip)
* **Mac OS**  [ShadowsocksX: 2.6.3.dmg](https://czero000.github.io/upload/proxy/ShadowsocksX-2.6.3.dmg)


### 运行客户端 ###
客户端都是免安装，打开就可以使用，可以参考这篇文章[Shadowsocks快速安装与配置指南](http://www.jianshu.com/p/08ba65d1f91a)


## ShadowSocks优化 ##
首先将内核升级到3.5或者以上

### 增加系统文件描述符的最大数量 ###
编辑``/etc/secritylimits.conf``文件增加以下两行
```
* soft nofile 51200
* hard nofile 51200
```
在启动Shadowsocks服务前，设置
```
ulimit -n 51200
```
### 调整内核参数 ###
编辑``/etc/sysctl.conf``，修改以下内容
```
fs.file-max = 51200

net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.netdev_max_backlog = 250000
net.core.somaxconn = 4096

net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_mem = 25600 51200 102400
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_congestion_control = hybla
```
最后执行``sysctl -p``使配置生效
