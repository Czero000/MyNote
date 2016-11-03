Github 就是一个提供免费托管开源代码的远程仓库，但对于一些敏感代码或者不想开源的源代码，有不舍得付费，那么就需要自己搭建一台 Git 服务器作为私有仓库来使用。下面是搭建 Git 服务器过程。

## 安装配置

- 安装 git

```
yum install git -y
```

- 创建一个 `git` 用户，用来运行 `git` 服务

```
useradd git -s /usr/bin/git-shell
```

- 创建证书登录
所有需要登录的用户，将他们自己的 `id_rsa.pub` 文件及公钥，导入到 `/home/git/.ssh/authorized_keys` 文件里，一行一个。

- 初始化git仓库
选当一个目录作为Git仓库，比如 `/opt/GitWork`，在 `/opt/GitWork` 目录下创建 git 仓库

```
git init --bare  sample.git
Initialized empty Git repository in /opt/GitWork/sample.git/
```
Git会创建一个裸仓库，仓库没有工作区。

- 克隆远程仓库

```
git clone git@172.16.11.211:/opt/GitWork/sample.git
Cloning into 'sample'...
warning: You appear to have cloned an empty repository.
```

- 代码提交到远程仓库

```
// 第一次推送远程版本库，会提示不知道推送的那个分支
git push origin master
// 确定分支之后，就不需要指定分支了
git push
```

## 公钥管理
如果团队很小，把每个人的公钥收集起来放到服务器的`/home/git/.ssh/authorized_keys`文件里就是可行的。如果团队有几百号人，就没法这么玩了，这时，可以用[Gitosis](https://github.com/res0nat0r/gitosis)来管理公钥。

## 权限管理
有很多不但视源代码如生命，而且视员工为窃贼的公司，会在版本控制系统里设置一套完善的权限控制，每个人是否有读写权限会精确到每个分支甚至每个目录下。因为 Git 是为 Linux 源代码托管而开发的，所以 Git 也继承了开源社区的精神，不支持权限控制。不过，因为 Git 支持钩子 （hook），所以，可以在服务器端编写一系列脚本来控制提交等操作，达到权限控制的目的。[Gitolite](https://github.com/sitaramc/gitolite)就是这个工具。
