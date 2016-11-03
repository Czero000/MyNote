Docker 是一个有趣的技术，在过去的两年已经从一个想法变成了全世界的机构都在采用来部署应用的技术。下面会通过 docker 来创建一个blog。

# 什么是 Docker
Docker 是一个操作系统容器管理工具，通过将应用打包到操作系统容器里面，从而让你能轻松管理和部署应用。

# 容器 vs 虚拟机
容器可能不如虚拟机一样为人所熟知，但是它们是另外的一种提供操作系统虚拟化的方法。然而，他们与标准的虚拟机有很大的差异。

标准的虚拟机通常包含一个完整的操作系统，OS 软件包，最后包含一两个应用。它是通过一个向虚拟机提供了硬件虚拟化的 Hypervisor 来实现的，允许单个服务器运行很多独立的被当做虚拟游客（virtual guest）的操作系统。

而容器与虚拟机的类似之处在于它们允许单个服务器运行多个操作环境（operating environment），然而这些环境不却是完整的操作系统。容器通常只包含必要的 OS 软件包和应用。他们通常不包含一个完整的操作系统或者硬件虚拟化。这也意味着比之虚拟机，容器的额外开销（overhead）更小。

容器和虚拟机通常被视为不能共生的技术，然而这通常是一个误解。虚拟机面向物理服务器，提供可以能与其他虚拟机一起共享这些物理资源的，功能完善的操作环境。容器通常是用来通过对单一主机的一个进程进行隔离，来保证被隔离的进程无法与处于同一个系统的其他进程进行互动。实际上，比起完全的虚拟机，容器与 BSD 的 Jail，chroot 的进程更加类似。

# Docker 提供了什么

Docker自身并不是一个容器的运行时环境；实际上 Docker 实际上是对容器技术不可知的（container technology agnostic），并且为了支持Solaris Zones和 BSD Jails 花了不少功夫。Docker 提供的是一种容器管理，打包和部署的方法。尽管这种类型的功能已经某一种程度地存在于虚拟机中，但在传统上，它们并不是为了绝大多数的容器方案而生的，而那些已经存在的，却又不如 Docker 一样容易使用且功能完善。

# 通过 Dockerfile 方式部署一个 blog (转载)

- 获取 blog 源码

```
git clone https://github.com/madflojo/blog.git
cd blog
```

- 使用 FROM 继承一个 docker 镜像
Dockerfile的第一条命令是 `FROM` 指令。这用来将存在的 Docker 镜像指定为基础镜像，这会让docker 使用 nginx 镜像。如果想使用最原始的空白状态。可以制定 `ubuntu:latest`使用 ubuntu 镜像。

```
FROM nginx:latest
MAINTAINER Charlie.Cui <charlie.cui127@mail.com>
```
除了使用 `FROM` 指令，还使用了 `MAINTAINER` 指令，用来显示 Dockerfile 的作者。Docker支持使用 `#` 用来当做注释的标示。

- 使用 `RUN` 来执行 `apt-get`

如果需要在 `docker` 中执行 `apt update` 和 `apt install python-dev`，可以通过 `RUN` 指令来实现。
```
FROM nginx:latest
MAINTAINER Charlie.Cui <charlie.cui127@mail.com>

RUN apt -qq update
RUN apt -qqy install python-dev python-pip
```

- 安装 python 模块

如果需要安装 python 模块，在 docker 之外，可以使用 pip 命令完成并且引用在仓库中的一个名叫`requirements.txt`文件。Dockerfile 使用 `COPY` 指令
```
FROM nginx:latest
MAINTAINER Charlie.Cui <charlie.cui127@mail.com>

RUN apt -qq update
RUN apt -qqy install python-dev python-pip

RUN mkdir -p /build/
COPY requirements.txt /build/
RUN pip install -r /build/requirements.txt
```

- 构建容器

```
docker build -t blog:v1 .
```
使用 `-t` 表示来讲这个镜像打上 blog 标签

- Docker 构建缓存

当docker 构建一个镜像的时候，不仅仅构建一个单一的镜像，它实际上在整个构建过程中构建多个镜像。每进行一步会构建一个镜像，当构建相同的容器时，会使用已经缓存的镜像，而不是重新构建一个镜像。凡是都会有两面，好的一面是当应用场景是 copy 文件，当源文件被更改，再次运行时 docker 会检测到文件不同，会从新 copy 新的文件，但是如果是安装 python-dev 这个软件包，当仓库更新了软件包版本，docker 是没法检测到这个变化，会傻傻的使用缓存，这样就会安装了一个老版本的软件。解决这个需要在 docker 构建时制定 `--no-cache=True` 来禁用缓存


- 部署 blog 其余部分

```
FROM nginx:latest
MAINTAINER Charlie.Cui <charlie.cui127@mail.com>

RUN apt -qq update
RUN apt -qqy install python-dev python-pip

RUN mkdir -p /build/
COPY requirements.txt /build/
RUN pip install -r /build/requirements.txt

COPY static /build/static
COPY templates /build/templates
COPY hamerkop /build/
COPY config.yml /build/
COPY articles /build/articles

RUN /build/hamerkop -c /build/config.yml
```
当再次运行 `docker build -t blog:v1 .`来构建 docker 镜像

- 运行一个定制化的容器

```
docker run -d -p 80:80 --name=blog blog:v1
```
使用`-p`参数，可以标志让用户将一个端口从主机映射到容器的一个端口，
