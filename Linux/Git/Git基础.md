# 关于版本控制
什么是版本控制
>版本控制是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。 在本书所展示的例子中，我们对保存着软件源代码的文件作版本控制，但实际上，你可以对任何类型的文件进行版本控制。

## 版本控制系统的变迁
想要做好版本控制，少不了相应的系统，版本控制系统也经历了不少变迁

### 原始
本地版本控制系统: 用复制整个项目目录的方式来保存不同的版本，或许还会改名加上备份时间以示区别。本地版本控制系统，大多都是采用某种简单的数据库来记录文件的历次更新差异。
![本地版本控制](http://ofc9x1ccn.bkt.clouddn.com/git/local.png)

### 进化
集中化版本控制: 为了让不同开发者协同工作，`Centralized Version Control Systems`应运而生，诸如 `CVS、Subversion` 以及 `Perforce` 等，都有一个单一的集中管理的服务器，保存所有文件的修订版本，而协同工作的人们都通过客户端连到这台服务器，取出最新的文件或者提交更新。

![集中版本控制](http://ofc9x1ccn.bkt.clouddn.com/git/centralized.png)

缺点是服务器单点故障。 如果宕机一小时，那么在这一小时内，谁都无法提交更新，也就无法协同工作。 如果磁盘发生损坏，又没有做恰当备份，毫无疑问你将丢失所有数据。

### 究极进化
分布式版本控制系统：为了解决本地版本控制的单点故障问题，`Distributed Version Control System` 便横空出世，像 Git、Mercurial、Bazaar 以及 Darcs 等，客户端并不只提取最新版本的文件快照，而是把代码仓库完整地镜像下来。 这么一来，任何一处协同工作用的服务器发生故障，事后都可以用任何一个镜像出来的本地仓库恢复。 因为每一次的克隆操作，实际上都是一次对代码仓库的完整备份。

![分布式版本控制](http://ofc9x1ccn.bkt.clouddn.com/git/distributed.png)

`Git` 不仅可以解决单点故障，还有离线提交、快速切换分支、方便合并、更少的仓库污染等特性。 在技术层面上，Git 绝对是一个无中心的分布式版本控制系统，但在管理层面上，我建议你保持一个中心版本库（Origin）
![Git仓库](http://ofc9x1ccn.bkt.clouddn.com/git/git-repo.jpg)

## Git 简史
生活中的许多伟大事物一样，`Git` 诞生于一个极富纷争大举创新的年代。`Linux` 内核开源项目有着为数众广的参与者。 绝大多数的 `Linux` 内核维护工作都花在了提交补丁和保存归档的繁琐事务上（1991－2002年间）。 到 2002 年，整个项目组开始启用一个专有的分布式版本控制系统 `BitKeeper` 来管理和维护代码。到了 2005 年，开发 BitKeeper 的商业公司同 Linux 内核开源社区的合作关系结束，他们收回了 `Linux` 内核社区免费使用 `BitKeeper` 的权力。 这就迫使 `Linux` 开源社区（特别是 `Linux` 的缔造者 `Linux Torvalds`）基于使用 `BitKcheper` 时的经验教训，开发出自己的版本系统。

他们对新的系统制订了若干目标
- 速度
- 简单的设计
- 对非线性开发模式的强力支持（允许成千上万个并行开发的分支）
- 完全分布式
- 有能力高效管理类似 Linux 内核一样的超大规模项目（速度和数据量）

自诞生于 2005 年以来，Git 日臻成熟完善，在高度易用的同时，仍然保留着初期设定的目标。 它的速度飞快，极其适合管理大项目，有着令人难以置信的非线性分支管理系统

## Git 基础

### 直接记录快照，而非差异比较
与其他版本控制系统不同在于 `Git` 对待数据的方法。概念上来区分，其它大部分系统以文件变更列表的方式存储信息
![CVS](http://ofc9x1ccn.bkt.clouddn.com/git/deltas.png "存储每个文件与初始版本的差异")
`Git` 则不同于上面，`Git` 更像是把数据看做对小型文件系统的快照，每次你提交更新，或在 `Git` 中保存项目状态时，它主要对当时的全部文件制作一个快照并保存这个快照的索引。 如果文件没有修改，`Git` 不再重新存储该文件，而是只保留一个链接指向之前存储的文件。 `Git` 对待数据更像是`快照流`。
![Git](http://ofc9x1ccn.bkt.clouddn.com/git/snapshots.png "存储项目随时间改变的快照")

### 近乎所有操作都是本地操作
在 `Git` 中的绝大多数操作都只需要访问本地文件和资源，因为你在本地磁盘上就有项目的完整历史，所以大部分操作看起来瞬间完成。

### Git 保持完整性
`Git` 中所有数据在存储前都计算校验和，然后以校验和来引用。 这意味着不可能在 `Git` 不知情时更改任何文件内容或目录内容。

### Git 一般只添加数据
在执行的 Git 操作时，几乎只往 Git 数据库中增加数据。 很难让 Git 执行任何不可逆操作，或者让它以任何方式清除数据。

### 三种状态
`Git` 有三种状态，已提交（`committed`）、已修改（`modified`）和已暂存（`staged`）。- 工作区(`Workspace`)是计算机中项目的根目录
- 工作区(Workspace)是计算机中项目的根目录
- 暂存区(Index)像个缓存区域，临时保存你的改动
- 版本库(Repository)分为本地仓库（Local)和远程仓库(Remote)
几乎所有常用命令就是围绕这几个概念来操作的，一图胜千言，下面是一张比较简单的图，包括了最基本的命令

![git-simple](http://ofc9x1ccn.bkt.clouddn.com/git/git-simple.png)

但只会使用以上命令是不够的，在这个复杂纷繁的程序世界，事情没你想的那么简单，不过有些事情想想就够了，不一定要去做，真要去做你也做不来，比如自己写个git来，但是，更多地的了解git是我们每个程序员都可以做得到的事。再看下图：
![git-advance](http://ofc9x1ccn.bkt.clouddn.com/git/git-advance.jpg)

下面的命令结合上面两张图来理解、练习、记忆效果更加。暂时用不着的命令记不住，不理解也没关系，哪天遇到问题，再来找找有没有合适的方法也不迟。

## Git 常用命令

### 新建/克隆代码库
```
git init                                            # 当前目录新建一个Git代码库
git init [project-name]                             # 新建一个目录，将其初始化为Git代码库
git init --bare [project-name]                      # 创建远程仓库
git clone /path/to/repository                       # 克隆本地仓库和它的整个代码历史
git clone username@host:/path/to/repository         # 克隆远端仓库
git fetch [url]                                     # 下载/同步项目到
```

### 添加/删除文件
```
git add [file1] [file2] ...                         # 添加指定文件到暂存区
git add [dir]                                       # 添加指定目录到暂存区，包括子目录
git add .                                           # 添加当前目录的所有文件到暂存区
git rm [file1] [file2] ...                          # 删除工作区文件，并且将这次删除放入暂存区
git rm --cached [file]                              # 停止追踪指定文件，但该文件会保留在工作区
git mv [file-original] [file-renamed]               # 改名文件，并且将这个改名放入暂存区
```

### 代码提交
```
git commit -m [message]                             # 提交暂存区所有文件到仓库区，并指定提交说明
git commit [file1] [file2] ... -m [message]         # 提交暂存区的指定文件到仓库区，并指定提交说明
git commit -a                                       # 提交工作区自上次commit之后的变化，直接到仓库区。是git add 和 git commit的组合操作
git commit -v                                       # 提交时显示所有diff信息
git commit --amend -m [message]                     # 使用一次新的commit，替代上一次提交
```

### 分支操作
```
git branch                                          # 列出所有本地分支
git branch -r                                       # 列出所有远程分支
git branch -a                                       # 列出所有本地分支和远程分支
git branch [branch-name]                            # 新建一个分支，但依然停留在当前分支
git checkout -b [branch]                            # 新建一个分支，并切换到该分支
git branch [branch] [commit]                        # 新建一个分支，指向指定commit
git checkout [branch-name]                          # 切换到指定分支
git merge [branch]                                  # 合并指定分支到当前分支
git branch -d [branch-name]                         # 删除本地分支
git push origin --delete [branch-name]              # 方法一：删除远程分支
git branch -dr [remote/branch]                      # 方法二：删除远程分支
```

### 撤销
```
git checkout [file]                                 # 恢复暂存区的指定文件到工作区（注意区别分支操作中得checkout命令）
git checkout [commit] [file]                        # 恢复某个commit的指定文件到暂存区和工作区
git checkout .                                      # 恢复暂存区的所有文件到工作区
git reset [file]                                    # 重置暂存区的指定文件，与最新的commit保持一致，但工作区不变
git reset --hard                                    # 重置暂存区与工作区，与最新的commit保持一致
git reset [commit]                                  # 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
git reset --hard [commit]                           # 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
git reset --keep [commit]                           # 重置当前HEAD为指定commit，但保持暂存区和工作区不变
git revert [commit]                                 # 新建一个commit，用来撤销指定commit
```

### 标签
```
git tag                                             # 列出所有tag
git tag [tag]                                       # 在当前commit新建一个tag
git tag [tag] [commit]                              # 在指定commit新建一个tag
git tag -d [tag]                                    # 删除本地tag
git push origin :refs/tags/[tagName]                # 删除远程tag
git show [tag]                                      # 查看tag信息
git push [remote] [tag]                             # 提交指定tag
git push [remote] --tags                            # 提交所有tag
git checkout -b [branch] [tag]                      # 新建一个分支，指向某个tag
```

### 查看日志
```
git status                                          # 显示所有变更文件
git log                                             # 显示当前分支的版本历史
git log --stat                                      # 显示当前分支的版本历史，以及发生变更的文件
git blame [file]                                    # 显示指定文件是什么人在什么时间修改过
git log -p [file]                                   # 显示指定文件相关的每一次diff
git diff                                            # 显示暂存区和工作区的差异
git diff --cached [commit]                          # 显示暂存区和某个commit的差异
git diff HEAD                                       # 显示工作区与当前分支最新commit之间的差异
git show [commit]                                   # 显示某次提交的元数据和内容变化
git show --name-only [commit]                       # 显示某次提交发生变化的文件
git show [commit]:[filename]                        # 显示某次提交时，某个文件的内容
git reflog                                          # 显示当前分支的最近几次提交
```

### 远程同步
```
git fetch [remote]                                  # 下载远程仓库的所有变动到暂存区
git remote -v                                       # 显示所有远程仓库
git remote show [remote]                            # 显示某个远程仓库的信息
git remote add [shortname] [url]                    # 增加一个新的远程仓库，并命名
git pull [remote] [branch]                          # 取回远程仓库的变化，并与本地分支合并
git push [remote] [branch]                          # 上传本地指定分支到远程仓库
git push [remote] --force                           # 即使有冲突，强行推送当前分支到远程仓库
git push [remote] --all                             # 推送所有分支到远程仓库
```

### 设置
`git` 的配置文件是`.gitconfig`，支持全局配置和项目配置，全部配置对所有项目有效，用 `--global`选择指定。
```
git config --list                                   # 显示配置
git config -e [--global]                            # 编辑(全局)配置文件
git config [--global] user.name "xx"                # 设置 commit 的用户
git config [--global] user.email "xx@xx.com"        # 设置 commit 的邮箱
gitk                                                # 内建的图形化 git
git config color.ui true                            # 彩色的 git 输出
git config format.pretty oneline                    # 显示历史记录时，只显示一行注释信息
git add -i                                          # 交互的添加文件至缓存区
```
参考资料:

[git-简易指南](http://www.bootcss.com/p/git-guide/)
