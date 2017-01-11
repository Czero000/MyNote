![](http://ofc9x1ccn.bkt.clouddn.com/docker/docker-images.png)
图注：一张图掌握 Docker 命令 - 简化版

![](http://ofc9x1ccn.bkt.clouddn.com/docker/docker-commands.png)
图注：一张图掌握 Docker 命令 - 完整版

在 docker 镜像的制作过程中，有不少方式可以减少容器的空间占用，甚至镜像可以精简 98%，精简 docker 镜像，既节省了存储空间，又能节省带宽，加快传输。

# 镜像层
在开始制作镜像前，首先了解镜像的原理，而这其中最重要的概念就是镜像层(Layers)
![](http://ofc9x1ccn.bkt.clouddn.com/docker/docker-image-layers.png)
在 `Dockerfile` 中的每条指令都会创建一个镜像层，继而会增加整体镜像的大小。

```
FROM busybox  
RUN mkdir /tmp/foo  
RUN dd if=/dev/zero of=/tmp/foo/bar bs=1048576 count=100  
RUN rm /tmp/foo/bar  
```
在上面例子中，最终容器没有变回，但是新生成的镜像会比原生镜像大。

# 精简方法

```
// 原始 Dockerfile　文件
FROM ubuntu:trusty  
ENV VER     3.0.0  
ENV TARBALL http://download.redis.io/releases/redis-$VER.tar.gz  
# ==> Install curl and helper tools...
RUN apt-get update  
RUN apt-get install -y  curl make gcc  
# ==> Download, compile, and install...
RUN curl -L $TARBALL | tar zxv  
WORKDIR  redis-$VER  
RUN make  
RUN make install  
#...
# ==> Clean up...
WORKDIR /  
RUN apt-get remove -y --auto-remove curl make gcc  
RUN apt-get clean  
RUN rm -rf /var/lib/apt/lists/*  /redis-$VER  
#...
CMD ["redis-server"]  
```
通过这个例子，演示如何精简 docker 镜像大小。

## 1. 优化基础镜像
选用更小的基础镜像，在常用的 Linux 系统镜像中，Ubuntu、Centos、Debian中，debian 更为轻量。

## 2. 减少构建步骤
串联 Dockerfile 指令（一般为 RUN 命令）
```
// 优化后的 Dockerfile
FROM debian:jessie

ENV VER     3.0.0  
ENV TARBALL http://download.redis.io/releases/redis-$VER.tar.gz

RUN echo "==> Install curl and helper tools..."  && \  
    apt-get update                      && \
    apt-get install -y  curl make gcc   && \
    \
    echo "==> Download, compile, and install..."  && \
    curl -L $TARBALL | tar zxv  && \
    cd redis-$VER               && \
    make                        && \
    make install                && \
    ...
    echo "==> Clean up..."  && \
    apt-get remove -y --auto-remove curl make gcc  && \
    apt-get clean                                  && \
    rm -rf /var/lib/apt/lists/*  /redis-$VER
#...
CMD ["redis-server"]  
```

## 3. 压缩镜像

- 使用命令或者工具压缩镜像

docker 自带的一些命令还能协助压缩镜像，比如 export 和 import
```
docker run -d redis:lab-3
$ docker export 71b1c0ad0a2b | docker import - redis:lab-4
```
麻烦的是需要先将容器运行起来，而且这个过程中你会丢失镜像原有的一些信息，比如：导出端口，环境变量，默认指令。

- 使用 [docker-squash](https://github.com/jwilder/docker-squash)

[下载安装](https://github.com/jwilder/docker-squash#installation)
```
docker save redis:lab-3 \
 | sudo docker-squash -verbose -t redis:lab-4  \
 | docker load
```

## 4. 使用最精简的基础镜像
使用 scratch 或者 busybox 作为基础镜像。

关于 scratch
- 一个空镜像，只能用于构建镜像，通过 FROM scratch
- 在构建一些基础镜像，比如 debian 、 busybox，非常有用
- 用于构建超少镜像，比如构建一个包含所有库的二进制文件

关于 busybox + 只有 1~5M 的大小 + 包含了常用的 UNIX 工具 + 非常方便构建小镜像这些超小的基础镜像，结合能生成静态原生 ELF 文件的编译语言，比如C/C++，比如 Go，特别方便构建超小的镜像。


## 5. 提取动态链接的 .so 文件
- 查看系统信息

```
cat /etc/os-release

NAME="Ubuntu"  
VERSION="14.04.2 LTS, Trusty Tahr"  

uname -a
Linux localhost 3.13.0-46-generic #77-Ubuntu SMP  
Mon Mar 2 18:23:39 UTC 2015  
x86_64 x86_64 x86_64 GNU/Linux  
```
- 打印共享的依赖库

```
ldd  redis-3.0.0/src/redis-server
    linux-vdso.so.1 =>  (0x00007fffde365000)
    libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f307d5aa000)
    libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f307d38c000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f307cfc6000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f307d8b9000)
```

- 打包需要的库文件

```
tar ztvf rootfs.tar.gz
4485167  2015-04-21 22:54  usr/local/bin/redis-server  
1071552  2015-02-25 16:56  lib/x86_64-linux-gnu/libm.so.6  
 141574  2015-02-25 16:56  lib/x86_64-linux-gnu/libpthread.so.0
1840928  2015-02-25 16:56  lib/x86_64-linux-gnu/libc.so.6  
 149120  2015-02-25 16:56  lib64/ld-linux-x86-64.so.2
```

- 制作 Dockerfile

```
FROM scratch  
ADD  rootfs.tar.gz  /  
COPY redis.conf     /etc/redis/redis.conf  
EXPOSE 6379  
CMD ["redis-server"]  
```
