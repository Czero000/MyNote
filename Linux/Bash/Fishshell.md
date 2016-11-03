### 什么是Fish Shell
FISH（friendly interactive shell）是一个用户友好的命令行 shell，主要是用来进行交互式使用。shell 就是一个用来执行其他程序的程序。

![Fish-Shell](http://ofc9x1ccn.bkt.clouddn.com/bash/fish-shell.png)

### Fish Shell特性
#### 自动建议
fish 会根据你的历史输入和补完来提供命令建议，就像一个网络浏览器一样。注意了，就是Netscape Navigator 4.0!
![Fish-Shell](http://ofc9x1ccn.bkt.clouddn.com/bash/fish-shell.gif))

#### 漂亮的VGA 色彩
fish 原生支持 term256， 它就是一个终端技术的艺术国度。 你将可以拥有一个难以置信的、256 色的shell 来使用。

#### 理智的脚本
fish 是完全可以通过脚本控制的，而且它的语法又是那么的简单、干净，而且一致。你甚至不需要去重写。

#### 基于 web 的配置
对于少数能使用图形计算机的幸运儿， 你们可以在网页上配置你们自己的色彩方案，以及查看函数、变量和历史记录。

#### 帮助手册补全
其它的 shell 支持可配置的补全， 但是只有 fish 可以通过自动转换你安装好的 man 手册来实现补全功能。

#### 开箱即用
fish 将会通过 tab 补全和语法高亮使你非常愉快的使用shell， 同时不需要太多的学习或者配置。

### 安装Fish Shell
```
对于 CentOS 7，请以 根用户 root 运行下面命令：
cd /etc/yum.repos.d/
wget http://download.opensuse.org/repositories/shells:fish:release:2/CentOS_7/shells:fish:release:2.repo
yum install fish

对于 CentOS 6，请以 根用户 root 运行下面命令：
cd /etc/yum.repos.d/
wget http://download.opensuse.org/repositories/shells:fish:release:2/CentOS_6/shells:fish:release:2.repo
yum install fish

对于 CentOS 5，请以 根用户 root 运行下面命令：
cd /etc/yum.repos.d/
wget http://download.opensuse.org/repositories/shells:fish:release:2/CentOS_5/shells:fish:release:2.repo
yum install fish
```
附: [主流类UNIX系统安装方法介绍](http://software.opensuse.org/download.html?project=shells%3Afish%3Arelease%3A2&package=fish)
