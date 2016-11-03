下面的nginx.conf简单的实现nginx在前端做反向代理服务器的例子，处理js、png等静态文件，jsp等动态请求转发到其它服务器tomcat


```
user  daemon;
worker_processes  8;
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 1000000;
worker_rlimit_nofile 65535;

error_log  logs/error.log;
#error_log  logs/error.log  notice;
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

    autoindex off;
    fastcgi_intercept_errors on;
    access_log  logs/access.log  access;
    sendfile        on;
    tcp_nopush     on;
    tcp_nodelay    off;
    keepalive_timeout  65;

  # gzip压缩功能设置
    gzip on;
    gzip_min_length 1k;
    gzip_buffers    4 16k;
    gzip_http_version 1.0;
    gzip_comp_level 6;
    gzip_types text/html text/plain text/css text/javascript application/json application/javascript application/x-javascript application/xml;
    gzip_vary on;

   ##http_proxy 设置
  server_name_in_redirect off;

    proxy_connect_timeout 5;
    proxy_send_timeout 60;
    proxy_read_timeout 5;
    proxy_buffer_size 32k;
    proxy_buffers 4 64k;
    proxy_busy_buffers_size 128k;
    proxy_temp_file_write_size 128k;
    proxy_ignore_client_abort on;
    proxy_headers_hash_max_size 51200;
    proxy_headers_hash_bucket_size 6400;
    proxy_temp_path   /cache/proxy_temp 1 2;
    proxy_cache_path  /cache/proxy_cache levels=1:2 keys_zone=cache_one:200m inactive=1d max_size=10g;

  # 设定负载均衡后台服务器列表
    upstream  backend  {
          #ip_hash;
          server   192.168.10.100:8080 max_fails=2 fail_timeout=30s ;  
          server   192.168.10.101:8080 max_fails=2 fail_timeout=30s ;  
    }

  # 很重要的虚拟主机配置
    server {
        listen       80;
        server_name    api.zerounix.com;
        root   /data/website/www;

        charset utf-8;
        access_log  logs/api.zerounix.com_access.log combined;
        error_log   logs/api.zerounix.com_error.log;

        #对 / 所有做负载均衡+反向代理
        location / {
            root   /apps/oaapp;
            index  index.jsp index.html index.htm;

            proxy_pass        http://backend;  
            proxy_redirect off;
            # 后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
            proxy_set_header  Host  $host;
            proxy_set_header  X-Real-IP  $remote_addr;  
            proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;

        }

        #静态文件，nginx自己处理，不去backend请求tomcat
        location  ~* /download/ {  
            root /apps/oa/fs;  

        }
        location ~ .*\.(gif|jpg|jpeg|bmp|png|ico|txt|js|css)$   
        {   
            root /apps/oaapp;   
            expires      7d;
        }
           location /nginx_status {
            stub_status on;
            access_log off;
            allow 192.168.10.0/24;
            deny all;
        }

        location ~ ^/(WEB-INF)/ {
            deny all;
        }
        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
  ## 其它虚拟主机，server 指令开始
}
```
