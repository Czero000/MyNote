# 使用 docker 创建一个静态网站
将 docker 作为本地 web 开发环境是使用 docker 的最简单情况，可以完全实现生产环境，保证开发环境和部署环境一致，下面讲创建一个简单的网站 sample。

## 通过 Dockerfile 创建 sample website

- 创建工作目录

```
mkdir sample
cd sample
touch Dockerfile
```


- 创建 nginx 配置文件

```
mkdir nginx ; cd nginx
wget https://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/nginx/global.conf
wget https://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/nginx/nginx.conf
```

- 编写 Dockerfile

```
# For a simple website
# V0.1
FROM ubuntu:16.04
MAINTAINER Charlie.Cui <charlie.cui127@gmail.com>
ENV REFRESHED_AT 2016-11-01
RUN apt-get update
RUN apt-get -qqy install nginx
RUN mkdir -p /var/www/html
ADD nginx/global.conf /etc/nginx/conf.d/
ADD nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

Dockerfile 内容主要包含下面几项
1. 安装 nginx
2. 在容器中创建一个目录 `/var/www/html`
3. 将下载的本地 nginx 配置文件添加到镜像中
4. 开放镜像的 80 端口

```
//设置nginx 监听 80 端口，root目录为 /var/www/html/website
::::::::::::::
nginx/global.conf
::::::::::::::
server {
        listen          0.0.0.0:80;
        server_name     _;

        root            /var/www/html/website;
        index           index.html index.htm;

        access_log      /var/log/nginx/default_access.log;
        error_log       /var/log/nginx/default_error.log;
}


// 配置 nginx 为非守护进程模式， daemon off选项会阻止 nginx 进入后台，强制 nginx 在前台运行，这样是为了保持 docker 容器的活跃状态，默认情况下， nginx 会以守护进行方式启动，这会使容器短暂运行，在守护进程 fork 启动后，发起守护进程的源进程便会退出，容器也随之停止
::::::::::::::
nginx/nginx.conf
::::::::::::::
user www-data;
worker_processes 4;
pid /run/nginx.pid;
daemon off;

events {  }

http {
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  include /etc/nginx/mime.types;
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;
  gzip on;
  gzip_disable "msie6";
  include /etc/nginx/conf.d/*.conf;
}
```

## 构建 sample 网站和 nginx 镜像
利用之前的  Dockerfile，可以利用 `docker build` 命令构建出新的镜像，并将该镜像命名为 czero/nginx:v1
```
docker build -t Czero/nginx:v1 .
```

通过 `docker history`可以看到构建过程

```
docker history czero/nginx:v1
IMAGE               CREATED                  CREATED BY                                      SIZE                COMMENT
32901d5b7262        19 hours ago             /bin/sh -c #(nop)  EXPOSE 80/tcp                0 B                 
774362201d8f        19 hours ago             /bin/sh -c #(nop) ADD file:d6698a182fafaf3cb0   415 B               
5e9f2a24c991        19 hours ago             /bin/sh -c #(nop) ADD file:9778ae1b43896011cc   286 B               
5d9dd8c94af9        19 hours ago             /bin/sh -c mkdir -p /var/www/html               0 B                 
4f866ff78749        19 hours ago             /bin/sh -c apt-get -qqy install nginx           56.81 MB            
887048645d36        19 hours ago             /bin/sh -c apt-get update                       39.19 MB            
6bc9139d50a3        20 hours ago             /bin/sh -c #(nop)  ENV REFRESHED_AT=2016-11-0   0 B                 
0ce2ec18f130        20 hours ago             /bin/sh -c #(nop)  MAINTAINER Charlie.Cui <ch   0 B                 
c73a085dc378        Less than a second ago   /bin/sh -c #(nop)  CMD ["/bin/bash"]            0 B                 
<missing>           Less than a second ago   /bin/sh -c mkdir -p /run/systemd && echo 'doc   7 B                 
<missing>           Less than a second ago   /bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/   1.895 kB            
<missing>           Less than a second ago   /bin/sh -c rm -rf /var/lib/apt/lists/*          0 B                 
<missing>           Less than a second ago   /bin/sh -c set -xe   && echo '#!/bin/sh' > /u   745 B               
<missing>           Less than a second ago   /bin/sh -c #(nop) ADD file:cd937b840fff16e04e   127.1 MB
```

## 从 sample 网站和 nginx 镜像构建容器
使用 czero/nginx:v1 镜像，构建容器

- 生成网站首页

```
// 创建 website 目录，创建首页文件 index.html
cd sample
mkdir website
cd website
wget https://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/website/index.html
```

- 创建容器

```
docker run -d -p 80:80 --name blog -v $PWD/website:/var/www/html/website:ro czero/nginx:v1 nginx
```
在执行`docker run`命令时，会创建一个 blog 容器，`-v`选项允许将宿主机的目录挂载到容器中，然后会传入 `nginx`启动命令，让 ningx 启动后已交互模式在前台运行。
卷在 docker 中非常有用，卷是一个或者多个容器内被选定的目录，可以绕过分层的联合文件系统，为 docker 提供持久数据或者共享数据，对卷的修改会直接生效，并会绕过镜像，当提交或者创建镜像时，卷不会被包含在镜像中。利用卷可以实现不想把代码或者应用等构建到镜像中，或者是希望同时对代码做开发和测试、代码频繁改动，不想在开发过程中重新构建镜像、希望在多个容器中共享代码。

`-v`参数指定了卷的源目录和容器里的目的目录，这两个目录通过`:`分隔，如果目的目录不存在，docker 会自动创建。也可以在目的目录后面添加`rw、ro`来指定目录的读写状态
`-p`参数指定了将容器内部的端口映射到本地的指定端口，`本地端口:容器端口`，可以不指定本地端口。

- 查看容器

通过`docker ps`命令可以查看正在运行的容器，可以看到 blog 容器正在活跃状态，并将 80 端口映射到本地的 80端口。
```
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                NAMES
e479aa5da8ae        czero/nginx:v1      "nginx"             16 minutes ago      Up 16 minutes       0.0.0.0:80->80/tcp   blog
```

## 使用 docker 构建一个 web 应用
现在构建一个更大的 web 应用，一个基于 sinatra 的 web 应用。

### 构建 sinatra 应用程序

- 创建 Dockerfile 文件

```
# a sinatra website
FROM ubuntu:16.04
MAINTAINER Charlie.Cui <charlie.cui127@gmail.com>
ENV REFRESHED_AT 2016-11-03
RUN apt-get -qq update
RUN apt-get -qqy install ruby ruby-dev build-essential redis-tools
RUN gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
RUN gem install --no-rdoc --no-ri sinatra json redis

RUN mkdir -p /opt/webapp
EXPOSE 4567

CMD ["/opt/webapp/bin/webapp"]
```
- 构建 docker 镜像

```
docker build -t czero/sinatra:v1 .
```

### 创建 sinatra 容器

- 下载 sinatra web 应用代码

```
wget  --cut-dirs=3 -nH -r --no-parent --no-check-certificate http://dockerbook.com/code/5/sinatra/webapp/
// 增加执行权限
chmod +x $PWD/webapp/bin/webapp
```

-  创建 docker 容器

```
docker run -d -p 4567:4567 --name sinatra -v $PWD/webapp:/opt/webapp czero/sinatra:v1  
```
Dockerfile 中的 `CMD` 指令，会让镜像启动容器时，执行该命令

- 查看容器执行命令的输出

```
docker logs sinatra
[2016-03-17 05:10:39] INFO  WEBrick 1.3.1
[2016-03-17 05:10:39] INFO  ruby 2.3.1 (2016-04-26) [x86_64-linux-gnu]
== Sinatra (v1.4.7) has taken the stage on 4567 for development with backup from WEBrick
[2016-03-17 05:10:39] INFO  WEBrick::HTTPServer#start: pid=1 port=4567
172.16.3.139 - - [17/Mar/2016:05:11:01 +0000] "GET / HTTP/1.1" 200 36 0.0064
```
在运行 `docker logs` 命令时，加上`-f` 参数，会持续食醋胡容器的 `stderr` 和 `stdout`

- 查看 docker 容器中正在运行的程序

```
docker top sinatra
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                14395               14378               0                   13:10               ?                   00:00:00            /usr/bin/ruby /opt/webapp/bin/webapp
```

- 查看 docekr 容器端口映射

```
docker port sinatra
4567/tcp -> 0.0.0.0:4567
```

- 访问 sinatra

sinatra 应用只接受输入参数，并将输入转成 JSON 输出
```
curl -i -H 'Accept: application/json' -d 'name=Foo&status=Bar' http://localhost:4567/json
HTTP/1.1 200 OK
Content-Type: text/html;charset=utf-8
Content-Length: 29
X-Xss-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Server: WEBrick/1.3.1 (Ruby/2.3.1/2016-04-26)
Date: Thu, 17 Mar 2016 07:47:18 GMT
Connection: Keep-Alive

{"name":"Foo","status":"Bar"}#   
```


## 构建 Redis 镜像和容器
扩展 sinatra 应用程序，在后端加入 redis 数据库，并在数据库中存入输入参数。构建全新的镜像和容器运行 redis 数据库，通过 docker 管理两个容器。

- 创建Dockerfile

```
cat Dockerfile
# contarner for sinatra redis
FROM ubuntu:16.04
MAINTAINER Charlie.Cui <charlie.cui127@gmail.com>
ENV REFRESHED_AT 2016-11-03
RUN apt-get -qq update
RUN apt-get -qqy install redis-server redis-tools
EXPOSE 6379
ENTRYPOINT ["/usr/bin/redis-server"]
CMD []
```

- 生成镜像
```
docker build -t czero/redis:v1 .
```
dockerfile 指定安装 redis 服务，开放 6379 端口，并启动 redis 服务

- 创建容器

```
docker run -d -p 6379:6379 --name sinatra_redis czero/redis:v1
```

- 测试连接 redis

```
// 本地安装 redis-tools
apt install -f redis-tools

// 连接 redis
redis-cli -h 127.0.0.1
```

## 连接到 redis 容器

连接到 docker 容器有两种方式，

- ip地址方式
- docker link功能

### ip 方式连接

查看 容器 IP 信息
```
docker inspect sinatra_redis

// 上面命令输出信息较多，可以利用-f 标志那个，过滤关键字
docker inspect -f '{{ .NetworkSettings.IPAddress }}' sinatra_redis
172.17.0.3
```
安装docker时，会创建一个名为 `docker0` 的网卡，主机上的容器都会在这个网卡上分配到一个地址，docker0 网卡，拥有一个私有IP段，`172.16～172.30`，网卡是一个虚拟的以太网桥，用于连接本地忘了和容器网络，在容器中，会以`veth`开头来命令网卡，并随机分配到一个 ip 地址，当知道了容器的ip，两个容器便可以通过 IP及端口相互访问，但是这种方式有个缺点。由于容器的 ip 地址是由 `docker0` 网卡分配的 ip 地址，当容器被重启，容器本身的 ip 地址会改变，这样当两个容量使用固定 ip 地址方式访问，这样便会连接不上。

### 通过 link 连接 容器

- 删除掉之前的容器

```
docker stop $(docker ps -q)
doker rm $(docker ps -aq)
```

- 创建新的 redis 容器

```
docker run -d --name sinatra_redis czero/redis:v1
```

- 创建 web 应用连接 redis

```
docker run -p 4567 --name sinatra_web --link  sinatra_redis:db -t -i -v $PWD/sinatra_web/webapp:/opt/webapp czero/sinatra:v1 /bin/bash
// 如果想要多个 web 应用同时连接 redis
docker run -p 4567 --name sinatra_web1 --link  sinatra_redis:db -v $PWD/sinatra_web/webapp:/opt/webapp czero/sinatra:v1
docker run -p 4567 --name sinatra_web2 --link  sinatra_redis:db -v $PWD/sinatra_web/webapp:/opt/webapp czero/sinatra:v1
```

`--link` 标志创建两连个容器间父子连接，这个标志需要两个参数: **一个是要连接的容器名称，另外一个便是连接后容器的别名** ,上面列子便是连接到 `sinatra_redis` 容器，并使用 `db` 作为别名。别名可以访问公开的信息，而无需关注底层容器的名字。连接让父容器可以访问子容器，并且把子容器的一些连接细节分给父容器。
这样会在安全性上得到提高，在启动 redis 时，并没有使用 `-p` 开放容器端口，当使用`--link` 时，可以让父容器直接访问子容器的开放端口。在启动容器守护进程时，如果加上 `--ice=false` 便会关闭所有没有连接的容器通信。**被连接的容器要求必须是同一主机上的容器，不同主机上的容器不能连接**

在创建两个容器连接后，会在两个地方写入连接信息
1. /etc/hosts 文件

```
more /etc/hosts
172.17.0.2      db 9e0071f714c4 sinatra_redis
172.17.0.3      744d452651ca
```
2. 包含连接信息的环境变量中

```
env   
HOSTNAME=744d452651ca
DB_NAME=/sinatra_web/db
DB_PORT_6379_TCP_PORT=6379
TERM=xterm
DB_PORT=tcp://172.17.0.2:6379
DB_PORT_6379_TCP=tcp://172.17.0.2:6379
```

- 容器应用通信

使用 host 或者 ENV 给应用加入连接信息，例如
```
// web应用代码
uri=URI.parse(env['DB_PORT'])
redis = redis.net(:host => uri.host, :port => uri.port )
```

**在docker run 命令中加入 --dns 或者 --dns-search 标志可以为容器定义dns**

再次使用`curl`命令测试 sinatra 程序
```
curl -i -H 'Accept: application/json' -d 'name=Foo&status=Bar' http://localhost:4567/json                                       
HTTP/1.1 200 OK
Content-Type: text/html;charset=utf-8
Content-Length: 29
X-Xss-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Server: WEBrick/1.3.1 (Ruby/2.3.1/2016-04-26)
Date: Fri, 18 Mar 2016 09:08:31 GMT
Connection: Keep-Alive

{"name":"Foo","status":"Bar"}
```

再次确认 redis 是否收到更新
