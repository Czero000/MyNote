# 镜像

## 什么是镜像
* 镜像是 Docker 的三大组件之一
* Docker 镜像就是一个只读模版，一个镜像可以包含一个完整的ubuntu 操作系统，系统安装了 apache 和用户自定义应用软件。
* 镜像可以用来创建容器，Docker 提供了一个简单的机制来创建镜像或者更新现有镜像，用户甚至可以直接从其他人哪里下载已经做好的镜像来使用
* Docker 运行容器之前需要本地存在对应镜像，如果不存在，Docker 就会从镜像仓库下载(默认是 Docker Hub 公共注册服务器的仓库)

## 获取镜像
通过 `docker pull` 命令从仓库下载所需的镜像，镜像可以通过 `Docker Hub` 获取已有镜像并更新，也可以利用本地文件系统创建一个
```
\\下载一个ubuntu16.04操作系统镜像
 docker pull ubuntu:16.04
```
该命令实际上是`docker pull registry.hub.docker.com/ubuntu:16.04`命令，即从注册服务器`registry.hub.docker.com`中的`ubuntu`仓库下载标记为16.04的镜像
有的时候官方注册服务器下载较慢，可以从其他仓库下载，如：
```
docker pull somedomain:5000/ubuntu:16.04
```

## 列出当前镜像
```
docker images           
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               c73a085dc378        2 weeks ago         127.1 MB
```
在列出的信息中，可以看到几个字段的信息

* 来自那个仓库 -> ubuntu
* 镜像的标记   -> latest、16.04
* ID         -> 唯一
* 创建时间
* 镜像大小
`TAG`信息标记来自同一个仓库的不同镜像，例如`ubuntu`仓库有多个镜像，通过TAG信息区分放行版本，例如，10.04、12.04、12.10等。通过下面命令指定镜像

```
\\ 通过ubuntu:16.04 启动一个容器
docker run -t -i ubuntu:16.04 /bin/bash
```
如果不执行 `TAG`，则默认使用 `latest` 标记信息


## 修改已有镜像

* 利用镜像启动一个容器
```
docker run --name docker_test -i -t -d ubuntu:16.04 /bin/bash
```
在容器中添加vim软件
```
apt install -y vim 
```
当结束后，使用`exit`退出，现在容器被改变了，使用docker commit命令提交更新后的副本
```
docker commit -m "Added Vim" -a "charlie.cui" 50eabeaf73f6 ubuntu:16.04v2
325a4e26e96fdefb70a9941db1c19ead801cf3ac5d9228bca6fc6c1a13c0ab92
```

* `-m` 来指定提交的说明信息,与使用版本控制工具一样
* `-a` 可以指定更新的用户信息
* 容器ID
* 指定目标镜像仓库名和tag信息
成功创建之后便会返回镜像的ID信息

使用 `docker images` 来查看新创建的镜像

之后便可以使用新的镜像启动容器
```
docker run -t -i ubuntu:16.04v2 /bin/bash
```

### 利用 Dockerfile 来创建镜像 

使用 `docker commit` 来扩展一个镜像相对简单，但是不方便在一个团队中分享。可以使用 `docker build` 来创建一个新的镜像，首先需要创建一个 Dockerfile ，包含一些如何创建镜像的指令

* 新建一个目录和一个 Dockerfile

```
mkdir docker
cd docker/
touch Dockerfile
```

* Dockerfile 中每一条指令都创建镜像的一层
```
cat Dockerfile
#This is a comment
FROM ubuntu:16.04
MAINTAINER Charlie.Cui < charlie.cui127@gmail.com > 
RUN apt-get -qq update
RUN apt-get -qqy install vim 
```
Dockerfile 的基本语法

* 使用#来注释
* `FROM`指令告诉Docker使用哪个镜像作为基础镜像
* 接着为维护者信息
* `RUN`开头的指令会在创建中运行，比如安装一个软件包，在这里使用`apt-get`安装vim

编写 Dockerfile 之后，可以使用 `docker build` 来生成镜像
```
docker build -t "ubuntu16.04:v1" . 
Sending build context to Docker daemon 3.072 kB
Step 1 : FROM ubuntu:16.04
 ---> e9ae3c220b23
Step 2 : MAINTAINER Charlie.Cui 
 ---> Using cache
 ---> 16d77dc9a444
Step 3 : RUN apt-get -y -qq update
 ---> Running in b8407b9d75c4
 ---> 8721117f7c1f
...
Processing triggers for libc-bin (2.19-0ubuntu6.6) ...
 ---> 5a4b35abd4c4
Removing intermediate container bb09f1a73b30
Successfully built 5a4b35abd4c4
```
其中 `-t` 标记添加 tag，指定新的镜像用户信息。 `.`是 Dockerfile 所在的路径(当前目录)，也可以使用一个具体的 Dockerfile 路径

上面的过程可以看到 build 进程在执行操作。它所做的第一件事就是上传 Dockerfile 内容，应为所有的操作都是根据 Dockerfile 内容来执行。
然后，Dockfile 中的指令被一条一条的执行，每一步都创建了一个新的容器，在容器中执行指令并提交修改(跟 docker commit 命令一样)。当所有的指令执行之后，返回最终的镜像 ID，所有的中间步骤产生的容器都被清理掉。

**注： Dockerfile 中执行命令不能超过127**

此外，还可以利用 ADD 命令赋值本地文件到镜像；用 `EXPOSE` 命令向外部开放端口；用 `CMD` 命令来描述容器启动后运行的程序
```
ADD myApp /var/www
EXPOSE 80
CMD ["/usr/sbin/apachectl", "-d", "FOREGROUND"]
```
现在可以利用新创建的镜像启动一个容器
```
docker]# docker run -t -i ubuntu16.04:v1 /bin/bash
```
还可以用 `docker tag`命令修改镜像标签
```
docker tag 5a4b35abd4c4 ubuntu16.04:devel
```

### 本地文件系统导入
要从本地文件系统导入一个镜像，可以使用openvz的模版来创建：openvz的模版下载地址：[http://openvz.org/Download/templates/precreated](http://openvz.org/Download/templates/precreated)

下载一个centos-7-x86_64的镜像，使用下面命令导入
```
wget http://download.openvz.org/template/precreated/centos-7-x86_64.tar.gz
cat centos-7-x86_64.tar.gz | docker import - centos:7
45a9c0d13bd2d94a69f8a70501541f5329dbbc4760e610013a801d8e11d8cb46
```

查看导入的新镜像
```
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos              7                   45a9c0d13bd2        7 minutes ago       564.3 MB
```

### 存出镜像
如果想要导出镜像到本地文件，可以使用`docker save`命令
```
\\ 保存镜像到本地文件
docker save -o ubuntu_16.04.tar ubuntu:16.04
```

### 载入镜像

可以使用`docker load`从导出的本地文件在导入到本地镜像库,命令会导入镜像以及其他的元数据信息(标签等)
```
docker load --input ubuntu_16.04.tar
或者
docker load < ubuntu_16.04.tar
```

#### 移除本地镜像
如果要移除本地镜像，使用`docker rmi`命令
```
dock rmi ubuntu:16.04
```
*** 在删除镜像之前要先`docker rm`删除掉依赖于这个镜像的容器 ***


### 清理所有为打过标签的本地镜像
`docker images` 可以列出本地的所有镜像，其中有很多中间状态的未打过标签的镜像，大量占用磁盘空间，使用下面命令清理本地镜像

```
docker rmi $(docker images -q -f "dangling=true")

\\ 完整写法
docker rmi $(docker images --quiet --filter "dangling=true")
```

### 镜像的实现原理

>Docker 镜像是怎么实现增量的修改和维护的？ 每个镜像都由很多层次构成，Docker 使用 Union FS 将这
些不同的层结合到一个镜像中去。
通常 Union FS 有两个用途, 一方面可以实现不借助 LVM、RAID 将多个 disk 挂到同一个目录下,另一个更
常用的就是将一个只读的分支和一个可写的分支联合在一起，Live CD 正是基于此方法可以允许在镜像不
变的基础上允许用户在其上进行一些写操作。 Docker 在 AUFS 上构建的容器也是利用了类似的原理。
