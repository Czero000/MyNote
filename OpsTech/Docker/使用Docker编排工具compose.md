# 什么是编排
编排（Orchestration）这个概念包含了自动配置、协作和管理服务的过程，在`Docker`中是指同时管理多个容器的行为。当使用多个容器运行在多个主机上时，`Docker`原生的编排工具便捉襟见肘，这样便开发了很多`Docker`构建和集成工具，提供让多个`Docker`宿主机具有协同的功能，

# Fig 简介
`Fig` 是`Orchard`团队开发的开源工具，使用`Python`编写，遵循`Apache 2.0`许可。在使用`Fig`时，可以用一个`YAML`文件定义一组要启动的容器，以及容器运行时的属性。

# 安装 Fig
`Fig` 可以在`Linux`发行版和`OS X`使用。可以直接安装可执行文件来安装或者通过`python pip`来安装。
```
pip install -U fig
```
