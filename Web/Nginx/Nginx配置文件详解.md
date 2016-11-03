## nginx 主配置文件详解 ##
安装nginx后，会在安装目录下生成conf目录，目录中`nginx.conf`便是nginx的主配置文件，nginx是基于模块化的构建方式，在ningx配置文件中也有体现，可以分为核心模块、事件模块、邮件模块、HTTP模块。

### 核心模块 ###

```
user  nobody;                                // 指定nginx运行的用户和组，默认为nobody
worker_processes  8;                         // 开启nginx的进程数，与cpu核数一致
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 1000000; // 将每个nginx进程绑定到一个CPU上
worker_rlimit_nofile 65535;                  // 指定nginx进程打开的最多文件描述符数量，受系统的最大文件打开数限制

error_log  logs/error.log;  notice;          // 设定全局错误日志文件，以什么级别显示，有[debug、info、warn、error、crit]模式可选，按照实际情况设定
#error_log  logs/error.log  info;            

pid        logs/nginx.pid;                   // 指定进程id的存储文件位置
```

### 事件模块 ###

```
events {
    use epoll;	                             // 工作模式设定为epoll，还有select、poll、kqueue、rtsig和/dev/poll模式可选
    worker_connections  65535;                // 定义每个进程的最大连接数，受系统的最大文件打开数限制
}
```


### http模块 ###
```
http {
    include       mime.types;                             // 文件拓展名与文件类型映射表 
    default_type  application/octet-stream;               // 默认文件类型 
    charset utf-8;                                        // 默认编码
   #autoindex on ;                                        // 关闭目录别表访问，默认关闭
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '    // 设置日志格式
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
  
    access_log  logs/access.log  main;                                 
   
    sendfile        on;                                   //开启高效文件传输模式，如果进行下载等磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。注意：如果图片显示不正常把这个改成off。
    #tcp_nopush     on;                                   // 开启防止网络阻塞

    #keepalive_timeout  0;
    keepalive_timeout  65;                                // 设置客户端连接报错活动的超时时间
    tcp_nodelay         on;
    
    
    // 反向代理设置
    proxy_connect_timeout 30;                           
    proxy_send_timeout 30;
    proxy_read_timeout 30;
    proxy_buffer_size 32k;
    proxy_buffers 4 64k;
    proxy_busy_buffers_size 128k;
    proxy_temp_file_write_size 128k;
    proxy_ignore_client_abort on;
    proxy_headers_hash_max_size 51200;
    proxy_headers_hash_bucket_size 6400;
    proxy_set_header  Host              $host;
    proxy_set_header  X-Real-IP         $remote_addr;     
    proxy_set_header  x-forwarded-for   $proxy_add_x_forwarded_for; //后端的Web服务器可以通过X-Forwarded-For获取用户真实IP

    server_names_hash_bucket_size 128;                  // 服务器名字的hash表大小
    client_header_buffer_size 32k;                      // 指定client请求头的hearder buffers大小
    large_client_header_buffers 4 32k;                  // 大请求缓冲区数量和大小
    client_max_body_size 8m;                            // 设置client请求的最大单个文件字节数
    client_body_temp_path /dev/shm/client_body_temp;    // 指定连接请求试图写入缓存文件的目录路径
 
 
 // FastCGI相关参数设定
    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;
    
// Gzip相关参数设定    
    gzip  on;                                             // 开启gzip压缩
    gzip_min_length 1k;                                   // 设置允许压缩的页面最小字节
    gzip_http_version 1.0;                                // 设置识别http协议的版本，默认是1.1
    gzip_comp_level 2;                                    // 设置压缩比，1-9
    gzip_buffers  4 16k;                                  // 设置4个单位16k的内存作为压缩结果流缓存 
    gzip_proxied any;                                     // nginx 做前端代理时启用该选项，表示无论后端服务器的headers头返回什么信息，都无条件启用压缩
    gzip_disable "MSIE [1-6]\.";                          // 禁用IE1-6的gzip压缩
    gzip_types  text/plain text/css application/x-javascript application/xml application/xml+rss text/javascript;  // 什么类型的页面或文档启用压缩
    gzip_vary on;
    server_name_in_redirect off;                          // nginx 在处理自己内部重定向时不默认使用  server_name 设置中的第一个域名
    
    include vhost/*.conf;
}

```


### 虚拟主机文件###

```
server {
        listen 80;                                              // 监听端口
        server_name  www.zerounix.com                           // 域名，可以多个，用空格分隔
        root /data/htdocs/www.zerounix.com;                  // 虚拟主机根目录
        charset uft-8;                                         // 访问编码
        access_log  logs/www.zerounix.com_access.log access;   //设置虚拟主机访问日志的存放路径和格式main
        error_log   logs/www.zerounix.com_error.log;            // 错误日志

        location / {
          index index.php index.htm                          // 甚至首页索引文件类型
        }
        
        error_page  404              /404.html;              // 定义404页面

        error_page   500 502 503 504  /50x.html;             // 定义50x页面
        location = /50x.html {
            root   html;
        }
        
        
        
        // php请求转发到本地9000，交给fastcig处理
        location ~.*\.(php|php5)?$ {
          fastcgi_pass   127.0.0.1:9000;
          fastcgi_index  index.php;
          fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
          include        fastcgi_params;
        }
        
        // 设置nginx status页面
        location /status {                                     
           stub_status on; 
           access_log logs/www.zerounix.com_status.log;
           auth_basic "NginxStatus"
           auth_baaic_user_file conf/htpasswd;                // apache提供的htpasswd工具
        }
        
        // 图片缓存时间
        location ~ .*\.(gif|jpg|jpeg|png|bmp|sfw)$ {             
          expires 10d;
        }
        
        // JS和CSS缓存时间
        location ~ .*\.{js|css}$ {
          expires 1h;
        }
        
        //所有静态文件由nginx直接读取不经过tomcat或resin
        location ~ .*.(htm|html|gif|jpg|jpeg|png|bmp|swf|ioc|rar|zip|txt|flv|mid|doc|ppt|pdf|xls|mp3|wma)$ { 
          expires 15d; 
        }
        
       
        // 本地动静分离反向代理配置，所有jsp的页面均交由tomcat或resin处理
        location ~ .(jsp|jspx|do)?$ {
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_pass http://127.0.0.1:8080;
        }
        
        #对 "/" 启用反向代理
     	  location / {
          proxy_pass	http://18.26.154.72:8090;
          proxy_redirect off;
        }
}
```
