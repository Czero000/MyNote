# 什么是编排
编排（Orchestration）这个概念包含了自动配置、协作和管理服务的过程，在 `Docker` 中是指同时管理多个容器的行为。当使用多个容器运行在多个主机上时，`Docker` 原生的编排工具便捉襟见肘，这样便开发了很多 `Docker` 构建和集成工具，提供让多个 `Docker` 宿主机具有协同的功能，

# Fig 简介
![fig](http://ofc9x1ccn.bkt.clouddn.com/docker/docker_fig.png)

`Fig` 是 `Orchard` 团队开发的开源工具，使用 `Python` 编写，遵循 `Apache 2.0` 许可。在使用 `Fig` 时，可以用一个 `YAML` 文件定义一组要启动的容器，以及容器运行时的属性。

# docker Compose
> Fig has been replaced by Docker Compose, and is now deprecated. The new documentation is on the Docker website.

`compose` 前身是 `Fig`，是基于 `Fig` 开发的，并兼容使用 `Fig` 的的应用程序。`Dockerfile` 可以让用户管理一个单独的应用容器；而 `Compose` 则可以允许用户在一个模板文件（YAML格式）中定义一组相关联的应用容器。
![fig](http://ofc9x1ccn.bkt.clouddn.com/docker/docker-compose.png)
# 安装 Compose
`Compose` 可以在 `Linux` 发行版和 `OS X` 使用。可以直接安装可执行文件来安装或者通过 `python pip` 来安装。

```
//
curl -L https://github.com/docker/compose/releases/download/1.9.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

// python pip
pip install -U docker-compose
```

# 使用 docker compose

## compose 文件
`compose` 文件使用`YAML`格式，`docker` 规定了一些指令，使用他们可以去设置对应东西，主要分为下面几项：

- Service: 应用容器，可以定义应用需要的服务，每个服务的命名，使用的镜像、挂载的数据卷、所属的网络、依赖那些其他服务等
- Networks: 应用网络，可以定义应用使用的网络类型
- Volumes： 容器数据卷，
