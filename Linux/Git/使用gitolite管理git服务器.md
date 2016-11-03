# 使用 gitolite 管理 git 服务器
由于Git的设计初衷，在使用 Git 在面向团队服务时，如果需要对权限控制，就需要第三方的工具来帮助 Git。在 Git 管理工具中，有三个解决方案。
- [Gitosis](https://github.com/res0nat0r/gitosis) 轻量级、开源项目，使用 SSH 公钥认证，只能做到库级别的权限控制。现在项目已经停止开发，不在维护；
- [Gitolite](https://github.com/sitaramc/gitolite) 轻量级、开源项目，使用 SSH 公钥认证，可以做到对分支级的权限控制；
- [[Git](http://git-scm.com/) + [Repo](http://source.android.com/source/downloading.html) + [Gerrit](http://code.google.com/p/gerrit/)] 重量级，集版本控制、库管理和代码审核。可以用来管理大型项目

由于 gitosis 不在提供更新，新建项目使用 gitolite 配置 git 的访问控制。

# 安装 Gitolite
Gitolite 的安装步骤如下如：
![gitolite](http://ofc9x1ccn.bkt.clouddn.com/git/gitolite.png "Gitolite")

## 系统环境
系统采用最新的 `Ubuntu-16-04 LTS`

|角色|ip|
|--|--|
|gitolite_gitServer |172.16.11.210|
|git_client|172.16.11.211|
|git_client|172.16.8.247|


## 创建管理用户
```
adduser --system --shell /bin/bash --group --gecos 'Git SCM User'--disabled-password --home /home/gitolite gitolite
su - gitolite
ssh-keygen -t rsa -q
cp ~/.ssh/id_rsa.pub /tmp/gitolite.pub
```


## 软件安装
```
// apt 安装
sudo apt install git-core gitolite3

// git clone
git clone git://github.com/sitaramc/gitolite
mkdir ~/bin
gitolite/install  -ln ~/bin
~/bin/gitolite setup -pk /tmp/gitolite.pub
```


## 配置授权

### 配置管理库

```
// 执行命令之后，会在家目录中创建 `gitolite-admin` 的 git 仓库，可以通过修改这个仓库来管理 Gitolite
git clone gitolite@172.16.11.210:gitolite-admin.git  

// 配置 git
git config --global push.default simple
git config --global user.email "charlie.cui127@gmail.com"
git config --global user.name "Cc"
```

在 gitolite 仓库中有两个目录 `conf` 和 `keydir`,前者是配置权限的配置文件，后者是用来存放 Client 的 key/

### 配置新用户

添加新用户很简单。添加一个名为 client1 的用户，获取她的公钥，命名为 client1.pub，然后放到在 `gitolite-admin`克隆的 keydir 目录。添加，提交，然后推送更改。这样用户就被添加了
```
ssh-keygen -t rsa -q
scp id_rsa.pub 172.16.11.210:/tmp/client1.pub
// ssh-key 都采用这样的命名方式 <yourname>.pub
cp /tmp/client1.pub /home/gitolite/gitolite-admin/keydir/client1.pub
```

### 定制配置

**官方示例**

```
cat conf/gitolite.conf
repo gitolite-admin
    RW+     =   gitolite

repo testing
    RW+     =   @all
```

**用户管理可以给用户或者仓库分组 `@`代表组，成员之间空格分隔**

```
@oss_repos = linux perl gitolite
@admin     = Cc
@devops    = alice bob charlie
```

**权限分类**
```
C: 代表创建，仅用在通配符版本库授权时可以使用，用于指定那个用户可以创建和通配符匹配版本库
R: 只读
RW: 读写
RW+: 除了读写权限，还可以对 rewind 的提交强制 push
RWC、RW+C: 只有当授权指令中定义了正则引用（正则表达式定义的分支、里程碑等），才可以使用该授权指令。其中 C 的含义是允许创建和正则引用匹配的引用（分支或里程碑等）。
RWD, RW+D: 只有当授权指令中定义了正则引用（正则表达式定义的分支、里程碑等），才可以使用该授权指令。其中 D 的含义是允许删除和正则引用匹配的引用（分支或里程碑等）。
RWCD, RW+CD: 只有当授权指令中定义了正则引用（正则表达式定义的分支、里程碑等），才可以使用该授权指令。其中 C 的含义是允许创建和正则引用匹配的引用（分支或里程碑等），D 的含义是允许删除和正则引用匹配的引用（分支或里程碑等）。
```

**拒绝访问**
```
还有一种权限是 `-`表示拒绝， 拒绝
RW  master integ    = @engineers
-   master integ    = @engineers
RW+                 = @engineers
```

**限制文件**
```
repo foo
  RW    = @devops
  - VERF/Makefile    = @devops

```

### 提交变更
```
// 使用 gitlite 用户
git add .
git commit -m 'xxx'
git push
```

### 新增项目
```
git init mytest
cd mytest/
echo "is test." > m.txt
git add .
git commit -am 'abc'
git remote add origin ssh://gitolite@localhost/mytest.git
git push origin master
git remote show origin
git push --set-upstream origin master
```
