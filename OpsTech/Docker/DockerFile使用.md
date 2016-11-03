# Dockerfile

## 书写 Dockerfile 准则和建议

- 要会利用 .dockerignore 文件。
- 避免安装不必要的包。
- 一个容器只运行一个进程。
- 排序使得方便更新，检查利用符号。
- 使层的数量尽可能少。
- 利用 Cache (在 Docker 建立镜像的过程中，Dockerfile 会按层编译执行，每个指令的编译会寻找缓存，如果有则不会创建新的镜像，可以使用 `--no-cache=true` 禁止使用缓存)

## Dockerfile 命令

### 基本语句

- FROM

指定一个基本的镜像源，FROM 语句必须是第一行
```
FROM <image>
FROM <image>:<tag>
FROM <image>@<digest>
```

- MAINTAINER

设置作者信息
```
MAINTAINER <name> <mail>
```

- LABEL

设置标签，采用键值对的形式
```
LABEL <key>=<value> <key>=<value> <key>=<value>
```

- RUN

运行命令
```
RUN <command>
RUN ["executable", "param1", "param2"]
```

- EXPOSE

用来指定监听端口
```
EXPOSE <port> [<port>...]
```

- ENV

设置环境变量
```
ENV <key> <value>
```

- WORKDIR

设置命令 COPY 、 ADD 和 ENV 路径

- ADD 、 COPY

从指定目录复制文件到容器
```
COPY <src> <dest>
ADD <src> <dest>
```
ADD 命令在 COPY 基础上增加
1. ADD 允许 <src> 是一个 URL
2. ADD 的 <src> 如果是一个压缩的文件，将会被解压缩复制

虽然　ADD 比 COPY 强大，但是还是推荐使用 COPY 来复制文件



- CMD 与 Entrypoint

  1. CMD 和 Entrypoint一般用于制作具备后台服务的镜像, 如启动nginx，php-fpm, mysql 等
  2. DockerFile应至少指定一个CMD命令或Entrypoint
  3. 都可以指定shell或exec函数调用的方式执行命令。
  4. DockerFile run 启动镜像之后便会退出容器，需要一个长时间运行的命令，使得容器一直执行

```
CMD ["executable","param1","param2"] （运行一个可执行的文件并提供参数）
CMD ["param1","param2"] （为ENTRYPOINT指定参数）
CMD command param1 param2 (以”/bin/sh -c”的方法执行的命令)

ENTRYPOINT ["executable", "param1", "param2"] (首选执行形式)
ENTRYPOINT command param1 param2 (以”/bin/sh -c”的方法执行的命令)
```
区别:
  1. 一个 Dockerfile 只能有一个 CMD/ENTRYPOINT 指令，如果有超过一个 CMD 将只启动并有效最后一个。
  2. CMD 在运行时会被 command 覆盖, ENTRYPOINT 不会被运行时的 command 覆盖
  3. 如果在 Dockerfile 中同时写了 entrypoint 和 cmd 则，docker 在 build 过程中会将 cmd 中指定的内容作为 entrypoint 的参数

需要初始化运行多个命令，彼此之间可以使用 && 隔开，但最后一个须要为无限运行的命令
