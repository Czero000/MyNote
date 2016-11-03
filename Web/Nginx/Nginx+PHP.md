## Nginx + PHP-FPM(FastCGI Process Manager) ##

### 简介 ###
Apache的效率和承载能力受到大多人的诟病，nginx藉由Nob-blocking与epool这些特性，大幅提高了并发数和处理速度，愈发收到人们的喜爱，但由于Nginx本身只是单纯的HTTP Server，如果执行php，需要配合CGI来完成，nginx把请求转发给fastcig管理进程，处理之后在将结果返回给Nginx。

### 什么是PHP-FPM ###
相对于Spawn-FCGI，PHP-FPM在内存和CPU方面的控制更胜一筹，PHP-FPM提供了更好的PHP进程管理方式。PHP-FPM对于PHP5.3之前来说就是一个补丁，将FastCGI进程管理整合到PHP中，在PHP 5.4之后，PHP-FPM已经集成到PHP的软件包中，在编译PHP过程中，增加`--enable-fpm`参数即可开启PHP-FPM


## 环境介绍 ##

### 系统环境 ###

本文的安装环境采用：`CentOS Linux release 7.1.1503 (Core)`


### 软件获取 ###

* Nginx

官方网站：http://nginx.org
最新稳定版本：[nginx-1.8.1.tar.gz](http://nginx.org/download/nginx-1.8.1.tar.gz)
帮助文档：http://nginx.org/en/docs
编译参数说明：http://nginx.org/en/docs/configure.html

* PHP

官方网站：http://www.php.net
稳定版：[php-5.6.17.tar.gz](http://cn2.php.net/distributions/php-5.6.17.tar.gz)


* 软件仓库

yum仓库包含centos官方和epel两个安装源
```
rpm -ivh http://mirrors.yun-idc.com/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
```

## 安装Nginx ##

### 安装模块依赖包 ###
Nginx的gzip、rewrite、ssl模块分别需要zlib、pcre、openssl的支持，可以通过源码或yum工具来安装

* 安装zlib

```
\\ 使用gzip压缩
yum install zlib zlib-devel -y
```


* 安装pcre

```
\\ 使用rewrite功能
yum install pcre pcre-devel
```

* 安装openssl

```
\\ 如果需要ssl支持,不需要可以不安装
yum install openssl openssl-devel
```

### 安装Nginx ###
```
wget http://nginx.org/download/nginx-1.8.1.tar.gz
tar zxf nginx-1.8.1.tar.gz
./configure --prefix=/usr/local/nginx --with-http_ssl_module  --with-http_stub_status_module --with-pcre
make && make install 
```

### 启动Nginx，测试安装 ###
nginx的默认端口是80，启动之前要确保80端口没有被占用，如果想保留80端口，只需要在nginx配置文件中，`listen 80；`中80换成其他端口。
```
//启动nginx
/usr/local/nginx/sbin/nginx

// 检查80端口是否启动
netstat -ntpl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      28608/nginx: master 
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      917/sshd            
tcp6       0      0 :::22                   :::*                    LISTEN      917/sshd            
```
通过浏览器访问Nginx Server 会出现欢迎页面，说明nginx安装正常

## 安装PHP及PHP-FPM ##

* 安装依赖软件包

确保安装之前有安装gd、png、curl、xml等lib开发库
```
yum install gd-devel libjpeg-devel libpng-devel libxml2-devel bzip2-devel libcurl-devel -y
```

* 下载软件包

```
wget http://cn2.php.net/distributions/php-5.6.17.tar.gz
tar zxf php-5.6.17.tar.gz 
cd php-5.6.17/
```

* 编译安装php5.6

以下参数支持，ftp、图片函数、pdo等，因为使用了php自带的mysqlnd，所以不需要额外安装mysql的lib库，如果是64位系统，参数后面需要添加--wtih-libdir=lib64
```
./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --with-bz2 --with-curl --enable-ftp --enable-sockets --disable-ipv6 --with-gd --with-jpeg-dir=/usr/local --with-png-dir=/usr/local --with-freetype-dir=/usr/local --enable-gd-native-ttf --with-iconv-dir=/usr/local --enable-mbstring --enable-calendar --with-gettext --with-libxml-dir=/usr/local --with-zlib --with-pdo-mysql=mysqlnd --with-mysqli=mysqlnd --with-mysql=mysqlnd --enable-dom --enable-xml --enable-fpm --with-libdir=lib64
make && make install 
```
注： 编译参数可以根据实际需求，增加或者删减

* 配置php-fpm

```
cp php.ini-production /usr/local/php/etc/php.ini
cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf
```

* 启动PHP-FPM

```
systemctl start php-fpm

// init方式
cp /usr/local/src/php-5.6.17/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
chmod +x /etc/init.d/php-fpm
/etc/init.d/php-fpm start

//执行没有报错，说明启动成功，还可以通过端口检查服务是否启动,9000端口是fpm的服务端口
netstat -ntpl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name   
tcp        0      0 127.0.0.1:9000              0.0.0.0:*                   LISTEN      23723/php-fpm       
tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      1423/sshd           
tcp        0      0 :::22                       :::*                        LISTEN      1423/sshd
```


## 配置Nginx ##

### nginx主配置文件 ###
```
cat nginx.conf
user  nobody;
worker_processes  8;  
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 1000000;
worker_rlimit_nofile 65535;

error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

pid        logs/nginx.pid;

events {
    use epoll;
    worker_connections  10240;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    server_names_hash_bucket_size 128;
    client_header_buffer_size 32k;
    client_body_buffer_size 32k;
    client_max_body_size 8m; 
    large_client_header_buffers 4 32k;
    
    log_format access  '$http_host $remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent"';

    index index.php index.html;
    autoindex off;
    fastcgi_intercept_errors on;
    #access_log  logs/access.log  main;

    sendfile        on;
    tcp_nopush     on;
    tcp_nodelay    off;

    keepalive_timeout  65;

    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;

    gzip  on;
    gzip_min_length 1k;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_buffers  4 16k;
    gzip_proxied any;
    gzip_disable "MSIE [1-6]\.";
    gzip_types  text/plain text/css application/x-javascript application/xml application/xml+rss text/javascript;
    gzip_vary on;
    server_name_in_redirect off;
    include /usr/local/nginx/conf/vhost/*.conf;
}
```

### 虚拟主机配置文件 ###

增加测试站点www.zerounix.com

```
server {
    listen 80;
    server_name www.zerounix.com;
    root /data/website/www.zerounix.com;
    charset utf-8;
    index index.php index.html index.htm ;
    access_log  logs/www.zerounix.com_access.log access;
    error_log   logs/www.zerounix.com_error.log;

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    location ~ .*\.(php|php5)$ {
        fastcgi_pass 127.0.0.1:9000;
        include        fastcgi.conf;
        try_files $uri =404;
    }
}

```
Nginx将会连接回环地址9000端口执行php文件，需要使用tcp/ip协议，速度较慢，建议设置为socket方式连接。将`fastcgi_pass 127.0.0.1:9000`变更为`fastcgi_pass unix:/dev/shm/php-fpm.socket`; 同时变更php-fpm配置文件，在`listen = 127.0.0.1:9000`添加`listen = /dev/shm/php5-fpm.socket`;分别重启`nginx`和`php-fpm` 服务

### 启动Nginx ###
```
/usr/local/nginx/sbin/nginx
```

### 创建PHP测试文件 ###
在`/data/website/www.zerounix.com/phpinfo.php` 添加
```
<?php 
var_export($_SERVER)
?>
```

### 测试访问 ###

```
curl -x 172.16.11.210:80 www.zerounix.com/phpinfo.php
array (
  'USER' => 'nobody',
  'HOME' => '/',
  'FCGI_ROLE' => 'RESPONDER',
  'SCRIPT_FILENAME' => '/data/website/www.zerounix.com/phpinfo.php',
  'QUERY_STRING' => '',
  'REQUEST_METHOD' => 'GET',
  'CONTENT_TYPE' => '',
  'CONTENT_LENGTH' => '',
  'SCRIPT_NAME' => '/phpinfo.php',
  'REQUEST_URI' => '/phpinfo.php',
  'DOCUMENT_URI' => '/phpinfo.php',
  'DOCUMENT_ROOT' => '/data/website/www.zerounix.com',
  'SERVER_PROTOCOL' => 'HTTP/1.1',
  'GATEWAY_INTERFACE' => 'CGI/1.1',
  'SERVER_SOFTWARE' => 'nginx/1.8.1',
  'REMOTE_ADDR' => '172.16.11.210',
  'REMOTE_PORT' => '55060',
  'SERVER_ADDR' => '172.16.11.210',
  'SERVER_PORT' => '80',
  'SERVER_NAME' => 'www.zerounix.com',
  'REDIRECT_STATUS' => '200',
  'HTTP_USER_AGENT' => 'curl/7.29.0',
  'HTTP_HOST' => 'www.zerounix.com',
  'HTTP_ACCEPT' => '*/*',
  'HTTP_PROXY_CONNECTION' => 'Keep-Alive',
  'PHP_SELF' => '/phpinfo.php',
  'REQUEST_TIME_FLOAT' => 1454568561.60866,
  'REQUEST_TIME' => 1454568561,
  )
```
说明php解析正常

## 总结 ##
Nginx安装配置相对容易，但是要调优就是另外一件事了，如果设定的不恰当，在高并发的时候，经常会出现502 Bad Gateway。之后会研究下调优的为问题。
