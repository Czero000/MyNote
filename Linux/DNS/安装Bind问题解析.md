安装Bind过程中发现的问题，本文是解决过程
### 问题

1. ipv6问题
报错信息如下：

```
"0-Nov-2015 16:40:55.395 lame-servers: info: error (network unreachable) resolving './NS/IN': 2001:500:2f::f#53"
```

### 解决

1. ipv6问题
  * 方法一： 直接编辑配置文件`/etc/sysconfig/named`，去掉IPv6的解析，只解析IPv4 `OPTIONS="whatever"变更为OPTIONS="-4"`
  * 方法二： 禁掉IPv6功能，编辑`/etc/sysconfig/network`,将`NETWORKING_IPV6=YES`变更为`NETWORKING_IPV6=no`
