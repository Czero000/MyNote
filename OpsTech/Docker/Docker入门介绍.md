# Docker 简介

##  Docker 是什么
>Docker is an open-source engine that automates the deployment of any application as a lightweight, portable, self-sufficient container that will run virtually anywhere.

Docker[https://www.docker.com/] 是 PaaS 提供商 [dotCloud](https://www.dotcloud.com/) 开源的一个基于 LXC 的高级容器引擎， []源代码](https://github.com/docker/docker)托管在 [Github](https://www.github.com) 上, 基于go语言并遵从Apache2.0协议开源。Docker近期非常火热，无论是从 GitHub 上的代码活跃度，还是Redhat宣布在 [RHEL7中正式支持Docker](http://server.cnw.com.cn/server-os/htm2014/20140616_303249.shtml)，都给业界一个信号，这是一项创新型的技术解决方案。就连 Google 公司的 Compute Engine 也支持 docker 在其之上运行，国内 “BAT” 先锋企业百度 Baidu App Engine(BAE) 平台也是[以Docker作为其PaaS云基础](http://blog.docker.com/2013/12/baidu-using-docker-for-its-paas/)。

Docker产生的目的就是为了解决以下问题：

1. 环境管理复杂：从各种 OS 到各种中间件再到各种 App，一款产品能够成功发布，作为开发者需要关心的东西太多，且难于管理，这个问题在软件行业中普遍存在并需要直接面对。Docker可以简化部署多种应用实例工作，比如 Web 应用、后台应用、数据库应用、大数据应用比如 Hadoop 集群、消息队列等等都可以打包成一个 Image 部署。

2. 云计算时代的到来：AWS 的成功，引导开发者将应用转移到云上, 解决了硬件管理的问题，然而软件配置和管理相关的问题依然存在 (AWS cloudformation是这个方向的业界标准, 样例模板可参考这里)。Docker 的出现正好能帮助软件开发者开阔思路，尝试新的软件管理方法来解决这个问题。

3. 虚拟化手段的变化：云时代采用标配硬件来降低成本，采用虚拟化手段来满足用户按需分配的资源需求以及保证可用性和隔离性。然而无论是 KVM 还是 Xen，在 Docker 看来都在浪费资源，因为用户需要的是高效运行环境而非OS，GuestOS 既浪费资源又难于管理，更加轻量级的 LXC 更加灵活和快速。
![vm](http://ofc9x1ccn.bkt.clouddn.com//docker/vm.png)
![docker](http://ofc9x1ccn.bkt.clouddn.com/docker/docker.png)

4. LXC 的便携性：LXC 在 Linux 2.6 的 Kernel 里就已经存在了，但是其设计之初并非为云计算考虑的，缺少标准化的描述手段和容器的可便携性，决定其构建出的环境难于分发和标准化管理(相对于 KVM 之类 image 和 snapshot 的概念)。Docker 就在这个问题上做出了实质性的创新方法。

## Docker的主要特性

- 文件系统隔离： 每个进程容器运行在完全独立的根文件系统里。
- 资源隔离： 可以使用 cgroup 为每个进程容器分配不同的系统资源，例如 CPU 和内存。
- 网络隔离： 每个进程容器运行在自己的网络命名空间里，拥有自己的虚拟接口和 IP 地址。
- 写时复制： 采用写时复制方式创建根文件系统，这让部署变得极其快捷，并且节省内存和硬盘空间。
- 日志记录： Docker 将会收集和记录每个进程容器的标准流（stdout/stderr/stdin），用于实时检索或批量检索。
- 变更管理： 容器文件系统的变更可以提交到新的映像中，并可重复使用以创建更多的容器。无需使用模板或手动配置。
- 交互式 Shell： Docker 可以分配一个虚拟终端并关联到任何容器的标准输入上，例如运行一个一次性交互 shell。


## Docker vs 传统虚拟化技术
作为一种新兴的虚拟化方式，Docker 跟传统的虚拟化方式（xen、kvm、vmware）相比具有众多的优势。

首先，Docker 容器的启动可以在秒级实现，这相比传统的虚拟机方式要快得多。 其次，Docker 对系统资源的利用率很高，一台主机上可以同时运行数千个 Docker 容器。容器除了运行其中应用外，基本不消耗额外的系统资源，使得应用的性能很高，同时系统的开销尽量小。传统虚拟机方式运行 10 个不同的应用就要起 10 个虚拟机，而 Docker 只需要启动 10 个隔离的应用即可。

具体说来，Docker 在如下几个方面具有较大的优势。

- 更快速的交付和部署
对开发和运维（devop）人员来说，最希望的就是一次创建或配置，可以在任意地方正常运行。
开发者可以使用一个标准的镜像来构建一套开发容器，开发完成之后，运维人员可以直接使用这个容器来部署代码。 Docker 可以快速创建容器，快速迭代应用程序，并让整个过程全程可见，使团队中的其他成员更容易理解应用程序是如何创建和工作的。 Docker 容器很轻很快！容器的启动时间是秒级的，大量地节约开发、测试、部署的时间。

- 更高效的虚拟化
Docker 容器的运行不需要额外的 hypervisor 支持，它是内核级的虚拟化，因此可以实现更高的性能和效率。

- 更轻松的迁移和扩展
Docker 容器几乎可以在任意的平台上运行，包括物理机、虚拟机、公有云、私有云、个人电脑、服务器等。 这种兼容性可以让用户把一个应用程序从一个平台直接迁移到另外一个。

- 更简单的管理
使用 Docker，只需要小小的修改，就可以替代以往大量的更新工作。所有的修改都以增量的方式被分发和更新，从而实现自动化并且高效的管理。

对比传统虚拟机总结：

|特性|容器|虚拟机|
|--|--|--|
|启动|秒级|分钟级|
|硬盘使用|一般为 MB|一般为 GB|
|性能|接近原生|弱于|
|系统支持量|单机支持上千个容器|一般几十个|

## Docker vs lxc
Docker 以 Linux 容器 LXC 为基础，实现轻量级的操作系统虚拟化解决方案。在 LXC 的基础上 Docker 进行了进一步的封装，让用户不需要去关心容器的管理，使得操作更为简便，具体改进有

- Portable deployment across machines

Docker 提供了一种可移植的配置标准化机制，允许你一致性地在不同的机器上运行同一个 Container；而 LXC 本身可能因为不同机器的不同配置而无法方便地移植运行；

- Application-centric

Docker 以 App 为中心，为应用的部署做了很多优化，而 LXC 的帮助脚本主要是聚焦于如何机器启动地更快和耗更少的内存；

- Automatic build
Docker 为 App 提供了一种自动化构建机制（Dockerfile），包括打包，基础设施依赖管理和安装等等；

- Versioning

Docker 提供了一种类似 git 的 Container 版本化的机制，允许你对你创建过的容器进行版本管理，依靠这种机制，你还可以下载别人创建的 Container，甚至像 git 那样进行合并；

- Component reuse

Docker Container 是可重用的，依赖于版本化机制，你很容易重用别人的 Container，作为基础版本进行扩展；

- Sharing

Docker Container 是可共享的，有点类似 github 一样，Docker 有自己的 INDEX，你可以创建自己的 Docker 用户并上传和下载 Docker Image；

- Tool ecosystem

Docker 提供了很多的工具链，形成了一个生态系统；这些工具的目标是自动化、个性化和集成化，包括对 PAAS 平台的支持等。

## docker 应用场景
Docker 作为一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。Docker 可以自动化打包和部署任何应用、创建一个轻量级私有 PaaS 云、搭建开发测试环境、部署可扩展的 Web 应用等。这决定了它在企业中的应用场景是有限的，Docker 将自己定位为“分发应用的开放平台”，其网站上也明确地提到了 Docker的典型应用场景
> - Automating the packaging and deployment of applications
> - Creation of lightweight, private PAAS environments
> - Automated testing and continuous integration/deployment
> - Deploying and scaling web apps, databases and backend services

对应用进行自动打包和部署，创建轻量、私有的 PAAS 环境，自动化测试和持续整合与部署，部署和扩展Web应用、数据库和后端服务。

平台即服务一般与大数据量系统同在，反观当前我司各 IT 系统，可以在以下情形下使用 docker 替代方案：

1. 结合 vagrant 或 supervisor，搭建统一的开发、测试环境
多个开发人员共同进行一个项目，就必须保持开发环境完全一致，部署到测试环境、正式环境后，最好都是同一套环境，通过容器来保存状态，分发给开发人员或部署，可以让“代码在我机子上运行没有问题”这种说辞将成为历史。

2. 对 memcached、mysql 甚至 tomcat，打包成一个个容器，避免重复配置
比如将一个稳定版本的、已配置完善的 mysql，固化在一个镜像中，假如有新的环境要用到 mysql 数据库，便不需要重新安装、配置，而只需要启动一个容器瞬间完成。tomcat 应用场景更多，可以将不同版本的 jvm 和 tomcat 打包分发，应用于多 tomcat 集群，或在测试服务器上隔离多个不同运行环境要求的测试应用（例如旧系统采用的是 jdk6，新系统在jdk7上开发，但共用同一套测试环境）。

**docker不足**

- LXC 是基于 cgroup 等 linux kernel 功能的，因此 container 的 guest 系统只能是 linux base 的

- 隔离性相比 KVM之类的虚拟化方案还是有些欠缺，所有 container公用一部分的运行库

- 网络管理相对简单，主要是基于 namespace 隔离

- cgroup 的 cpu 和 cpuset 提供的 cpu 功能相比 KVM 的等虚拟化方案相比难以度量(所以 dotcloud 主要是安内存收费)

- container 随着用户进程的停止而销毁，container 中的 log 等用户数据不便收集

另外，Docker 是面向应用的，其终极目标是构建 PAAS 平台，而现有虚拟机主要目的是提供一个灵活的计算资源池，是面向架构的，其终极目标是构建一个 IAAS 平台，所以它不能替代传统虚拟化解决方案。目前在容器可管理性方面，对于方便运维，提供 UI 来管理监控各个 containers的功能还不足，还都是第三方实现如 DockerUI、Dockland、Shipyard 等。

## docker 组成部分
![make_docker](http://ofc9x1ccn.bkt.clouddn.com/docker/make_docker.png)
Docker 使用客户端-服务器 (client-server) 架构模式。Docker 客户端会与 Docker 守护进程进行通信。Docker 守护进程会处理复杂繁重的任务，例如建立、运行、发布你的Docker 容器。Docker 客户端和守护进程可以运行在同一个系统上，当然你也可以使用 Docker 客户端去连接一个远程的 Docker 守护进程。Docker 客户端和守护进程之间通过socket或者 RESTful API 进行通信。

### images 镜像
Docker 镜像就是一个只读的模板。例如，一个镜像可以包含一个完整的 ubuntu 操作系统环境，里面仅安装了 Apache 或用户需要的其它应用程序。
镜像可以用来创建 Docker 容器。
Docker 提供了一个很简单的机制来创建镜像或者更新现有的镜像，用户甚至可以直接从其他人那里下载一个已经做好的镜像来直接使用。


### container 容器
Docker 利用容器来运行应用。容器是从镜像创建的运行实例。它可以被启动、开始、停止、删除。每个容器都是相互隔离的、保证安全的平台。可以把容器看做是一个简易版的 Linux 环境（包括root用户权限、进程空间、用户空间和网络空间等）和运行在其中的应用程序。 镜像是只读的，容器在启动的时候创建一层可写层作为最上层。

### repository 仓库
仓库是集中存放镜像文件的场所。有时候会把仓库和仓库注册服务器（Registry）混为一谈，并不严格区分。实际上，仓库注册服务器上往往存放着多个仓库，每个仓库中又包含了多个镜像，每个镜像有不同的标签（tag）。

- 公开仓库

docker团队控制的top-level的顶级repository，即[Docker Hub](https://registry.hub.docker.com/)，存放了数量庞大的镜像供用户下载，任何人都能读取，里面包含了许多常用的镜像，如ubuntu, mysql ,redis, python等。

- 个人仓库

个人公共库也是被托管在Docker Hub上，网络上的其它用户也可以pull你的仓库（如docker pull seanloook/centos6）你可以在修改完自己的container之后，通过commit命令把它变成本地的一个image，push到自己的个人公共库。（在此之前你需要docker login登录，或者vi ~/.dockercfg。）

- 私有仓库

首先与另外一种仓库区分——Docker Hub Private Repository，它简单理解为公网上的个人私有库，与上面的个人公共库相对应，在Docker Hub上Create Repository时选择Private便是，只有你自己才可以读写。
这里所说的私有仓库是指自己在本地服务器上搭建的专属自己的内部仓库docker-registry，俗称“私服”，供无法访问互联网的内部网络使用，或者镜像到本地一份以加快pull、push的速度。
它与公共仓库最明显的区分就是repository的命名，如必须使用带.的主机名或域名，后面必须接:port，如sean.tp-link.net:5000/centos6:your_tag_name，而公共仓库第一个斜杠前表示的是登录用户名。命名关系到推送到哪个服务器的哪个位置，

## 运行一个容器的内部过程
docker client告诉docker daemon运行一个容器，例如：docker run -i -t ubuntu /bin/bash
让我们分解一下这个命令，docker client启动使用一个二进制的docker命令，最小的docker client需要你告诉docker daemon你的容器是从哪个docker镜像构建的，你希望在容器内部运行哪个命令。所以启动过程如下：

- Pulling the ubuntu image

docker检查是否存在ubuntu镜像，如果本地不存在ubuntu镜像，则docker会到docker index下载。
- Creates a new container

利用镜像创建容器
- Allocates a filesystem and mounts a read-write layer

为镜像创建文件系统层和read-write层
- Allocates a network / bridge interface

为容器创建网络接口，使容器和本地机器可以通讯
- Sets up an IP address

在地址池中为容器分配一个可用的IP地址
- Executes a process that you specify

运行你的应用
- Captures and provides application output

连接log的标准输入、输出、错误，以使你直到你的应用是否正常运行

# 安装 Docker

Docker可以运行在Ubuntu16.04 LTS 和 CentOS7.x上，可能会和其他的二进制 EL7 兼容工作，但是 Docker 官方并没有去做测试。

## 准备
先决条件：

* 运行64为CPU架构（x86_64和amd64），不支持32位
* 运行Linux3.8 或更高版本，老版本的2.6.x及之后版本也可以运行，但是运行结果大不相同
* 内核必须支持合适的存储驱动（storagedriver）
  * Device Manager
  * AUFS
  * vfs
  * btrfs
* 内核必须支持并开启cgroup和命名空间功能


## 安装

- 更新系统

```
apt-get update
apt install linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get install apt-transport-https ca-certificates
```

- 添加 GPG Key

```
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

- 增加安装源

```
vim /etc/apt/sources.list.d/docker.list
// On Ubuntu Precise 12.04 (LTS)
deb https://apt.dockerproject.org/repo ubuntu-precise main
// On Ubuntu Trusty 14.04 (LTS)
deb https://apt.dockerproject.org/repo ubuntu-trusty main
// Ubuntu Wily 15.10
deb https://apt.dockerproject.org/repo ubuntu-wily main
// Ubuntu Xenial 16.04 (LTS)
deb https://apt.dockerproject.org/repo ubuntu-xenial main
```

- 安装docker

```
apt update
apt install docker
```

- 启动docker

```
systemctl start docker
```

- 验证启动

```
docker info
Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 0
Server Version: 1.12.2
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 0
 Dirperm1 Supported: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
```

# 使用 Docker及 docker 命令汇总

## 查看 docker 信息

- 查看 docker 版本

```
docker Version
```

- 显示 docker 系统的信息

```
docker info
```

## 镜像相关

- 检索 image

```
// docker search image_name
docker search ubuntu:16.04
```

- 下载一个预建立的镜像

```
// docker pull image_name
docker pull ubuntu:16.04
Digest: sha256:28d4c5234db8d5a634d5e621c363d900f8f241240ee0a6a978784c978fe9c737
Status: Downloaded newer image for ubuntu:16.04
```
这个将从索引仓库中通过名字找到ubuntu镜像，并从索引仓库中心下载到本地镜像存储
当镜像下载成功后，你可以看到12位的hash值，如c73a085dc378，这是下载完整的镜像的精简ID，这些短的镜像ID是完整镜像ID前12个字符—可以使用docker inspect或者docker images -no-trunc=true来获取完整镜像ID

- 列出镜像列表

```
docker images
```

- 删除一个或者多个镜像

```
//docker rmi image_name
docker rmi ubuntu:16.04
```

- 显示一个镜像的历史

```
// docker history image_name
docker history ubuntu:16.04
```

##  容器操作

- 创建容器

```
//使用 docker run 命令创建容器,-i 保证容器中 STDIN 开启，-t 分配一个伪终端
docker run -i -t ubuntu /bin/bash
```
使用 ubuntu:16.04 运行一个交互性的 shell,分配一个伪终端，附带 stdin 和 stout ,如果想要退出伪终端，使用 CTRL -p + CTRL -q,容器只有在指定的 /bin/bash 命令处于运行状态，容器才会运行，一旦退出 `/bin/bash`，容器随之停止。

如果容器因为某种错误导致停止，可以通过`--restart`标志，让docker自动重启容器。--restart会检查容器的退出状态，并据此来判断是否要重启容器
```
docker run --restart=always --name=docker_test -i -t -d ubuntu:16,04 /bin/bash
```

- 容器命名

容器命名可以是使用小写字母a-z、大写字母A-Z、数字0-9、下划线、圆点、横线。容器的命名必须是唯一
```
docker run --name docker_test -i -t ubuntu:16.04 /bin/bash
```
可以通过增加 `-d` 参数，创建一个长时间运行的容器
```
docker run --name docker_test -i -t -d ubuntu:16.04 /bin/bash
```

- 查看容器状态

通过 `docker ps -a `可以列出所有停止、运行的容器
```
docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
fd74d17e54f1        ubuntu:16.04        "/bin/bash"         2 minutes ago       Up 2 minutes                            docker_test
```

- 查看容器进程

```
docker top docker_test
```

- 深入容器

```
// 获取更加详细的 docker 信息
docker inspect docker_test
```

- 启动、重启、连接容器

```
//启动
docker start docker_test

//停止
docker stop docker_test

// 杀死
docker stop docker_test

// 连接
docker sttach docker_test
```

- 在容器内部运行进程

```
// -d 表明在后台运行一个进程
docker exec -d docker_test touch /etc/new_config_file

// 打开一个交互性的shell
docker exec -i -t docker_test /bin/bash
```

- 查看容器输出

```
//到目前为止收集的输出
docker logs docker_test
//使用-f 可以监控docker输出
docker logs -f docker_test
//加上tail 命令可以查看某段输出，如最后10行
docker log --tail 10 docker_tet
//使用 -t 可以在每条日志加上时间戳
docker log -ft docker_test
```

- 保存容器

```
// docker commit id new_image_name
docker commit 2194cf55f5ea docker_test
```

- 删除容器

```
// 所有容器
docker rm `docker ps -a -q`
// 指定容器
docker rm name/id
```

- 查看容器被修改的文件或目录

```
docker diff docker_test
```

- 拷贝文件

```
docker cp [name|id]:container_path  local_path
```

## 保存和加载镜像

- 保存镜像

```
docker save image_name -o file_path
```

- 加载本地镜像

```
docker load -i file_path
```
