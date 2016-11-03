Gitlab 是一个基于 `Ruby on Rails` 开发的开源项目管理程序，可以通过 WEB 界面进行访问公开的或者私人项目，实现一个自托管的 Git 项目仓库。它拥有与 GitHub 类似的功能，可以浏览代码，管理缺陷和注释。

## 安装依赖软件

```
apt-get install curl openssh-server ca-certificates postfix
```

## 添加　GitLab仓库 ,安装软件包
```
curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
apt-get install gitlab-ce
```

如果不习惯使用命令行管道的安装方式，官方提供了[安装脚本](http://packages.gitlab.cc/install/gitlab-ce/) 或者 [手动下载相应平台及版本的软件包](https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/)
```
curl -LJO https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/xenial/gitlab-ce-XXX.deb/download
dpkg -i gitlab-ce-XXX.deb
```

如果访问速度慢，可以使用国内的镜像站如：`https://mirror.tuna.tsinghua.edu.cn/help/gitlab-ce/`

## 启动 GitLab
```
gitlab-cli reconfigure
```

可以通过 `gitlab-clt status` 查看 GitLab 安装是否成功
```
gitlab-ctl status
run: gitlab-workhorse: (pid 17111) 276s; run: log: (pid 17010) 298s
run: logrotate: (pid 17034) 294s; run: log: (pid 17033) 294s
run: nginx: (pid 17019) 296s; run: log: (pid 17018) 296s
run: postgresql: (pid 16863) 383s; run: log: (pid 16862) 383s
run: redis: (pid 16776) 389s; run: log: (pid 16775) 389s
run: sidekiq: (pid 17001) 300s; run: log: (pid 17000) 300s
run: unicorn: (pid 16970) 302s; run: log: (pid 16969) 302s
```

## 访问 GitLab
访问 `http:gitlab_serverip`，即可访问 GitLab 的　Web 界面

- 首次使用要设置密码
