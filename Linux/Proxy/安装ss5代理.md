
### socks5代理服务 ###
官网：http://ss5.sourceforge.net/
 
### 安装gcc编译环境和相关依赖包 ###  
```
yum -y install pam-devel openldap-devel cyrus-sasl-devel gcc gcc-c++ automake make openssl openssl-devel
```

### 下载ss5 ###  
```
wget http://cznic.dl.sourceforge.net/project/ss5/ss5/3.8.9-8/ss5-3.8.9-8.tar.gz
```

### 编译安装ss5 ###
```
tar -zxf ss5-3.8.9-8.tar.gz
cd ss5-3.8.9
./configure      
make && make install
```

### 配置ss5 ###
编译安装后的配置文件在/etc/opt/ss5下面
```
ss5.conf  ss5.ha  ss5.passwd
```

添加用户和密码
ss5.passwd的用法是：
***用户 密码***
 
配置代理权限
ss5.conf 用法
```
auth    0.0.0.0/0               -               -
#      Auth     SHost           SPort   DHost           DPort   Fixup   Group   Band    ExpDate
permit -       0.0.0.0/0       -       0.0.0.0/0       -       -       test       -       -
```

修改/etc/init.d/ss5文件自定义端口，默认为1080
```
daemon /usr/sbin/ss5 -t $SS5_OPTS -b 0.0.0.0:1081
```

在`/etc/sysconfig/ss5`中，取消注释
```
SS5_OPTS=" -u root"
``` 

### 启动ss5 ###

```
/etc/init.d/ss5 start
doneting ss5...                                            [  OK  ]
```
