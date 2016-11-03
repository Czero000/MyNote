
# 反向代理 

## 初识反向代理 
反向代理(Reverse Proxy)是指以代理服务器来接受Internet的连接请求，然后将请求转发给内部服务器，并将从服务器得到的结构返回给Internet请求客户端，喜事的代理服务器对外表现为一个反向代理服务器。

![Reverse_Proxy](http://ofc9x1ccn.bkt.clouddn.com/nginx/Reverse_Proxy.png "反向代理示意图")

## 反向代理作用 ###

* 保护网站安全 -- 任何来自Internet的请求都必须先经过代理服务器
* 通过配置缓存功能加速Web请求 -- 可以缓存后端Web服务器的某些静态资源，减轻Web服务器的负载
* 实现负载均衡 -- 充当负载均衡服务器均衡的分发请求，平衡集群中各个服务器的负载压力

# 安装 Nginx 
安装过程参考nginx源码安装

## 配置反向代理 
简单的反向代理就是http，不需要缓存控制等高级功能，仅仅一个简单的代理，比如nginx+php-fpm也是一种反向代理

```
location ~ .*\.(php|php5)$ {
   fastcgi_pass 127.0.0.1:9000;
   include        fastcgi.conf;
   try_files $uri =404;
}
```

而相对复杂一些的就是反向代理一些网站，会应用到缓存控制机制。

## 简单反向代理  ###

* 在nginx.conf配置文件中的http块中添加下面内容

```
// 反向代理参数
proxy_connect_timeout 5;                        // nginx跟后端服务器连接超时时间(代理连接超时)                       
proxy_send_timeout 60;
proxy_read_timeout 5;                           // 连接成功后，后端服务器响应时间(代理接收超时)
proxy_buffer_size 32k;                          // 设置代理服务器（nginx）保存用户头信息的缓冲区大小
proxy_buffers 4 64k;                            // proxy_buffers缓冲区
proxy_busy_buffers_size 128k;                   // 高负荷下缓冲大小（proxy_buffers*2）
proxy_temp_file_write_size 128k;                  
proxy_ignore_client_abort on;                   // 不允许代理端主动关闭连接
proxy_headers_hash_max_size 51200;
proxy_headers_hash_bucket_size 6400;

// 配置临时目录、缓存路径(同一个硬盘分区，注意权限)
proxy_temp_path   /cache/proxy_temp 1 2;
proxy_cache_path  /cache/proxy_cache levels=1:2 keys_zone=cache_one:200m inactive=1d max_size=10g;

// keys_zone=cache_one:200m 表示这个 zone 名称为 cache_one，分配的内存大小为 200MB
// levels=1:2 表示缓存目录的第一级目录是 1 个字符，第二级目录是 2 个字符
// inactive=1d 表示这个zone中的缓存文件如果在 1 天内都没有被访问，那么文件会被cache manager 进程删除
// max_size=10G 表示这个zone的硬盘容量为 10G

```

* 在虚拟主机配置文件proxy.zerounix.com.conf文件中添加下面内容

```
server {
        listen       80;
        server_name  proxy.zerounix.com;
        index index.html index.htm index.php;
        access_log  logs/proxy.zerounix.com_access.log access;

        location / {
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_pass http://172.16.11.211;
        }


// 只对图片、js、css等静态文件进行缓存

        location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|js|css)$ {
            proxy_next_upstream http_502 http_504 error timeout invalid_header;
            proxy_cache cache_one;
            proxy_cache_valid  200 304 12h;
            proxy_cache_valid 301 302 1m;
            proxy_cache_valid any 1m;
            proxy_cache_key $host$uri$is_args$args;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Accept-Encoding "none";
            proxy_ignore_headers "Cache-Control" "Expires";
            proxy_pass http://172.16.11.211;
            expires      1h;
        }

        location ~ .*\.(php|jsp|cgi)?$ {
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For  $remote_addr;
            proxy_pass http://172.16.11.211;
        }

        error_page  500 502 503 504  /50x.html;

        location = /50x.html {
            root   html;
        }

}

```

## 使用SSL的反向代理  ###

* 安装nginx

需要将将 --with-http_sub_module、ngx_cache_purge-2.3编译到nginx中
下载链接[http://labs.frickle.com/files/](http://labs.frickle.com/files/)

```
// 编译参数
./configure --prefix=/usr/local/nginx --add-module=../ngx_cache_purge-2.3 \
--with-http_sub_module --with-http_stub_status_module --with-http_ssl_module --with-http_flv_module \
--with-http_gzip_static_module --with-ld-opt=-ljemalloc
```

* 签发证书

自己签发免费ssl证书，为nginx生成自签名ssl证书(访问时需添加信任。也可以使用第三方签名后的证书，如免费的startssl)
```
cd /usr/local/nginx/conf
openssl genrsa -out server.key 1024
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

* 配置反向代理

```
proxy_temp_path   /cache/proxy_temp 1 2;
proxy_cache_path  /cache/proxy_cache levels=1:2 keys_zone=cache_one:200m inactive=1d max_size=10g;
proxy_cache_key "$host$request_uri";

server {
listen 80;
server_name proxy.zerounix.com;
rewrite ^(.*) https://proxy.zerounix.com$1 permanent;
}

server
    {
        listen 443;
        server_name proxy.zerounix.com;

        upstream google {
            server 173.194.127.144:80 max_fails=3;
            server 173.194.127.147:80 max_fails=3;
            server 173.194.127.148:80 max_fails=3;
            server 173.194.127.145:80 max_fails=3;
            server 173.194.127.146:80 max_fails=3;  
        }
        
        ssl on;
        ssl_certificate      /usr/local/nginx/ssl/nginx.crt;      
        ssl_certificate_key  /usr/local/nginx/ssl/nginx.key;   
        ssl_protocols   TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-RC4-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:RC4-SHA:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!DSS:!PKS;
        ssl_prefer_server_ciphers  on;
        ssl_session_cache       shared:SSL:10m;
        ssl_session_timeout     5m;

        location / {
            proxy_cache one;
            proxy_cache_valid  200 302  1h;
            proxy_cache_valid  404      1m;
            proxy_redirect https://www.google.com/ /;
            proxy_cookie_domain google.com proxy.zerounix.com;
            proxy_pass              http://google;
            proxy_set_header Host "www.google.com";
            proxy_set_header Accept-Encoding "";
            proxy_set_header User-Agent $http_user_agent;
            proxy_set_header Accept-Language "zh-CN";
            proxy_set_header Cookie "PREF=ID=047808f19f6de346:U=0f62f33dd8549d11:FF=2:LD=zh-CN:NW=1:TM=1325338577:LM=1332142444:GM=1:SG=2:S=rE0SyJh2w1IQ-Maw";            
            sub_filter www.google.com proxy.zerounix.com;
            sub_filter_once off
        }
    }
    
```

1 监听了80和443端口，可以在Linux自己生成证书。
2 定义了个upstream google，放了5个谷歌的ip（通过nslookup www.google.com命令获取（yum -y install bind-utils）），如果不这样做，就等着被谷歌的验证码搞崩溃吧。
3 也设置了反向代理缓存，某些资源不用重复去请求谷歌获取，加快搜索速度
4 proxy_redirect https://www.google.com/ /; 这行的作用是把谷歌服务器返回的302响应头里的域名替换成我们的，不然浏览器还是会直接请求www.google.com，那样反向代理就失效了。
5 proxy_cookie_domain google.com proxy.zerounix.com; 把cookie的作用域替换成我们的域名
6 proxy_pass http://google; 反向代理到upstream google
7 proxy_set_header Accept-Encoding ""; 防止谷歌返回压缩的内容，因为压缩的内容我们无法作域名替换
8 proxy_set_header Accept-Language "zh-CN";设置语言为中文
9 proxy_set_header Cookie "PREF=ID=047808f19f6de346:U=0f62f33dd8549d11:FF=2:LD=zh-CN:NW=1:TM=1325338577:LM=1332142444:GM=1:SG=2:S=rE0SyJh2w1IQ-Maw"; 这行很关键，传固定的cookie给谷歌，是为了禁止即时搜索，因为开启即时搜索无法替换内容。还有设置为新窗口打开网站，这个符合我们打开链接的习惯
10 sub_filter www.google.com proxy.zerounix.com当然是把谷歌的域名替换成我们的了，注意需要安装nginx的sub_filter模块(编译加上--with-http_sub_module参数)

## 反向代理配置范例
```
cat nginx.conf
user  daemon;
worker_processes  8;  
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 1000000;
worker_rlimit_nofile 65535;

error_log  logs/error.log  notice;
pid        logs/nginx.pid;

events {
    use epoll;
    worker_connections  10240;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    server_names_hash_bucket_size 128;
    client_header_buffer_size 32k;
    client_body_buffer_size 32k;
    client_max_body_size 8m;
    large_client_header_buffers 4 32k;
    log_format access  '$http_host $remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent"';

    autoindex off;
    fastcgi_intercept_errors on;
    access_log  logs/access.log  access;
    sendfile        on;
    tcp_nopush     on;
    tcp_nodelay    off;
    keepalive_timeout  65;

    gzip  on;
    gzip_min_length 1k;
    gzip_http_version 1.0;
    gzip_comp_level 2;
    gzip_buffers  4 16k;
    gzip_proxied any;
    gzip_disable "MSIE [1-6]\.";
    gzip_types  text/plain text/css application/x-javascript application/xml application/xml+rss text/javascript;
    gzip_vary on;
    server_name_in_redirect off;

    proxy_connect_timeout 5;                       
    proxy_send_timeout 60;
    proxy_read_timeout 5;                         
    proxy_buffer_size 32k;                       
    proxy_buffers 4 64k;                        
    proxy_busy_buffers_size 128k;                   
    proxy_temp_file_write_size 128k;                  
    proxy_ignore_client_abort on;              
    proxy_headers_hash_max_size 51200;
    proxy_headers_hash_bucket_size 6400;
    proxy_temp_path   /cache/proxy_temp 1 2;
    proxy_cache_path  /cache/proxy_cache levels=1:2 keys_zone=cache_one:200m inactive=1d max_size=10g;

    proxy_set_header  Host		$host;
    proxy_set_header  X-Real-IP 	$remote_addr;
    proxy_set_header  x-forwarded-for	$proxy_add_x_forwarded_for;

    server {
        listen	80;
	      server_name	api.zerounix.com;
	      charset utf-8;
	      index index.html;
	      root /usr/local/nginx/html;
	      access_log  logs/api.zerounix.com_access.log combined;
        error_log   logs/api.zerounix.com_error.log;
	      location / {
		        proxy_pass	http://118.2.154.72:6080;
	      }
     }
}

```
