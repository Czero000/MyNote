# Docker 常用命令

根据 docker 命令的应用场景，大体可以分为下面几类：

- docker 镜像管理 `docker [ build|commit|history|images|import|load|rmi|save|tag ]`
- docker 镜像仓库 `docker [login|logout|pull|push|search]`
- docker 容器生命周期 `docker [ create|run|start|stop|restart|kill|rm|pause|unpause]`
- docker 容器操作 `docker [cp|diff|exec|attach|ps|rename|top|logs|events|export|port|wait|update|stats]`

![](http://ofc9x1ccn.bkt.clouddn.com/docker/docker_cli_stage.png)

## 列出服务器上的镜像 (images)
```
docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
registry                  latest              c9bd19d022f6        5 days ago          33.3 MB
nginx                     latest              a5311a310510        11 days ago         181.5 MB
ubuntu                    16.04               c73a085dc378        3 weeks ago         127.1 MB
```
可以根据 `REPOSITORY` 来判断镜像来自那个仓库。如果没有`/`表示从官方仓库，类似于`username/repos_name`则表示个人仓库。`IMAGE ID` 其实是缩写，想看完整需要使用`--no-trunc`选项。

## 搜索镜像 (search)
```
docker search nginx
NAME                      DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
nginx                     Official build of Nginx.                        4406      [OK]       
```

## 从注册服务器拉取 images (pull)
```
// 下载最新版本的images
docker pull ubuntu
docker pull ubuntu:latest
// 指定拉取版本
docker pull ubuntu:16.04
// 从私有注册服务器拉取镜像
docker pull 172.16.11.211:5000/ubuntu:16.04
```

## 推送一个 image 到 registry (push)
```
docker push czero/mariadb
```

## 从 image 启动一个 container
`docker run`命令首先会从特定的 image 创之上 create 一层可写的 container，然后通过 start 命令来启动它。停止的 container 可以重新启动并保留原来的修改。run 命令启动参数有很多，以下是一些常规使用说明，更多部分请参考http://www.cnphp6.com/archives/24899
当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定的镜像，不存在就从公有仓库下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
- 从地址池配置一个 ip 地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器被终止
```
Usage: docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

- 运行一个 简单的容器

```
docker run ubuntu echo "Hello World"
```

- 创建一个交互模式的容器

```
docker run -i -t --name=czero ubuntu /bin/bash
```
通过`--name`来指定容器名称，`run` 命令创建容器,`-i` 保证容器中 STDIN 开启，`-t` 分配一个伪终端

- 创建一个后台运行的容器

```

docker run -d ubuntu /bin/sh -c "while true; do echo hello world; sleep 2;done"
```
大多数情况是把启动的容器运行在后台，比如 apache、nginx等，使用 `docker ps` 可以看到运行容器的信息，通过 ` docker logs container_name` 可以看到容器输出，`docker attach container_name` 可以连接到运行的容器。

- 映射端口到容器

在容器中运行的程序，可以将容器中的端口映射到宿主机的端口上，便可提供服务
```
-p 80:80 这个即是默认情况下，绑定主机所有网卡（0.0.0.0）的80端口到容器的80端口上
-p 127.0.0.1:80:80 只绑定localhost这个接口的80端口
-p 127.0.0.1::5000
-p 127.0.0.1:80:8080
```

- 映射容器目录

目录映射其实就是绑定挂载宿主机的目录到容器中，适用于数据库文件，代码等
```
-v <host_path:container_path>
-v /tmp/docker:/tmp/docker
```

两个容器之间还可以通过`--link`建立连接。下面的列子便是将`/tmp/docker` 下的 index.html，映射到容器内，这样便可以通过访问容器中的nginx 访问页面。
```
docker run --name  nginx_test -v /tmp/docker:/usr/share/nginx/html:ro -p 80:80 -d nginx:1.7.6
```

- 将容器 container 固化为一个新的镜像 images (commit)

在制作镜像之后，例如安装某些软件包，更改配置，如果不固化容器，在容器停止后，这些变动便消失了，这就需要使用 commit 将容器保存起来。
```
// docker commit <container> 【repo:tag]
```
`repo:tag` 可选选项，固化容器只对运行状态的容器有效。

```
// 查看运行中的容器
docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
8f99b43b0400        docker_test:v1      "nginx -g 'daemon off"   7 days ago          Up 13 seconds       0.0.0.0:80->80/tcp       website

// 固化容器
docker commit -m 'test' 8f99b43b0400 website:v2
```

当反复去 commit 一个容器的时候，每次都会得到一个新的 `IMAGE ID`，假如后面的 repository:tag 没有变，通过 docker images 可以看到，之前提交的那份镜像的 `repository:tag` 就会变成`<none>:<none>`，所以尽量避免反复提交。
另外，观察以下几点

- commit container只会pause住容器，这是为了保证容器文件系统的一致性，但不会stop。如果你要对这个容器继续做其他修改：
- 你可以重新提交得到新image2，删除次新的image1
- 也可以关闭容器用新image1启动，继续修改，提交image2后删除image1
- 当然这样会很痛苦，所以一般是采用Dockerfile来build得到最终image，参考[]
- 虽然产生了一个新的image，并且你可以看到大小有100MB，但从commit过程很快就可以知道实际上它并没有独立占用100MB的硬盘空间，而只是在旧镜像的基础上修改，它们共享大部分公共的“片”。
