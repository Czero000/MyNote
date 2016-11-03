#前言
类似Dropbox形式的同步型网盘 (云存储服务) 已经成为越来越多人生活和工作中都离不开的工具了。可惜 Dropbox 在国内多次遭屏蔽，而国产的百度云、金山快盘等产品也有人不太喜欢使用。如果你有动手能力，并且希望数据能掌握在自己手中，那么给自己或团队搭建私有的文件同步云存储平台是个不错的选择。Seafile 是一个免费开源且专业可靠的云存储平台软件，能让你自建一个类似 Dropbox 功能的私有云存储服务！可以实现文件同步、共享、跨平台访问、团队协作等功能

#什么是seafile
Seafile 是由国内团队开发的一个国际化的开源云存储软件项目，目前据说已有10万左右的用户，典型的机构用户包括比利时的皇家自然科学博物馆、德国的 Wuppertal 气候、能源研究所等等。Seafile 同时提供了客户端和服务器端软件免费下载，任何个人或公司都能搭建属于自己的私有文件同步服务。

Seafile 的服务器端支持 Linux 、Windows 以及树莓派平台，客户端除了网页版之外，还支持 Mac、Linux、Windows 三个桌面平台以及 Android 和 iOS 两个移动平台。你可以利用局域网里的一台电脑作为服务器，搭建一个仅局域网内部能访问的专有云存储服务，也能将 Seafile 部署到互联网上的诸如阿里云、Linode 或任何 VPS、独立服务器上，实现一个私人的在线云存储服务。

同时，Seafile 支持用户同时使用多个同步服务器，而且能够在不同服务器之间切换。比如，用户可以用公司服务器来同步工作文件，用个人服务器与朋友共享私人文件，两者互不干扰，私密性也可保证。而且，由于 Seafile 是开源的项目，因此相对来说数据的私密性还是有保障的，起码不必担心有什么看不见的后门。

# 安装seafile
## 安装环境介绍
- 系统版本: `CentOS Linux release 7.1.1503 (Core)`
- 软件依赖:
  - python2.7(从Seafile5.1开始，python版本最低要求2.7)
  - python-setuptools
  - python-imaging
  - python-mysqldb
  - python-ldap
  - python-memcache(或者python-memcached)
- 软件版本: seafile-server_5.1.1_x86-64.tar.gz

## 安装Seafile
- 安装软件依赖包

```
yum install python-setuptools python-imaging python-ldap MySQL-python python-memcache python -y
```

- 安装seafile

```shell
mkdir -p /data/seafile/
cd /data/seafile
wget http://download-cn.seafile.com/seafile-server_5.1.1_x86-64
tar -zxf seafile-server_5.1.1_x86-64.tar.gz
mkdir installed
mv seafile-server_5.1.1_x86-64.tar.gz installed/
mv seafile-server-5.1.1 seafile-server
cd seafile-server
./setup-seafile-mysql.sh \\该脚本会检查安装环境，不满足安装要求会有提示你安装相应软件包，并会问你一些创建seafile一些问题，配置你seafile各项参数
[ server name ]   // 服务器名字
[ This server's ip or domain ] //服务器ip或者域名
[ default "/data/seafile/seafile-data" ] //seafile数据存放目录
[ default "8082" ] //默认TCP端口
[1] Create new ccnet/seafile/seahub databases  //创建新的数据库
[2] Use existing ccnet/seafile/seahub databases //使用已有的数据库
What is the host of mysql server?                  //数据库信息
[ default "localhost" ]
[ default "3306" ]
[ root password ]
[ default "root" ]
[ default "ccnet-db" ]
[ default "seafile-db" ]
[ default "seahub-db" ]
```
# 启动Seafile服务

## 启动Seafile

```
./seafile.sh start    // 启动seafile服务
```

## 启动Seahub

```shell
./seahub.sh start  // 启动seahub 默认端口8000
```
第一次启动Seahub，会提示你创建Seafile管理员账号

## 关闭重启Seafile和Seahub

```
//关闭Seafile、Seahub
./seahub.sh stop
./seafile.sh stop

// 重启Seafile、Seahub
./seafile.sh restart
./seahub.sh restart

// 如果停止、重启失败
1. 使用pgrep命令检查,seafile/seahub进程是否运行
pgrep -f seafile-controller                //查看Seafile进程
pgrep -f "manage.py run_gunicorn"          //查看Seahub进程

2. 使用pkill命令杀掉进程
pkill -f seafile-controller
pkill -f "manage.py run_gunicorn"
```
## 自定义端口启动

```
//更改`conf/ccnet.conf`文件中`SERVICE_URL`的值
SERVICE_URL = http://172.16.11.211:8001

// 正常启动Seafile进程
./seafile.sh start    
./seahub.sh start
```

## 配置Seahub
Seahub是Seafile服务器的网站界面，SeafServer用来处理浏览器端文件的上传与下载，默认监听8082端口。

通过fastcgi部署Seahub，通过反向代理部署SeafServer，域名绑定`pan.zerounix.com`
- 创建虚拟主机配置文件

```shell
  server {
        listen       80;
        server_name  pan.zerounix.com;

        access_log  logs/pan.zerounix.com_access.log access;
        error_log  logs/pan.zerounix.com_error.log ;

        location / {
            include /usr/local/nginx/conf/fastcgi.conf
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Referer http://$host;
            proxy_pass http://172.16.11.211:8000;
        }

        location /seafhttp {
            rewrite ^/seafhttp(.*)$ $1 break;
            proxy_pass http://127.0.0.1:8082;
            client_max_body_size 0;
            proxy_connect_timeout 36000s;
            proxy_read_timeout 36000s;
        }

        location /media {
            root /data/seafile/seafile-server/seahub;

        }

}
```
- 修改seafile配置文件

```sehll
  // 修改SERVICE_URL和FILE_SERVER_ROOT
  SERVICE_URL: http://pan.zerounix.com
  FILE_SERVER_ROOT: http://pan.zerounix.com/seafhttp
```