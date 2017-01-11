# 安装 GitLab
Gitlab 是一个基于 `Ruby on Rails` 开发的开源项目管理程序，可以通过 WEB 界面进行访问公开的或者私人项目，实现一个自托管的 Git 项目仓库。它拥有与 GitHub 类似的功能，可以浏览代码，管理缺陷和注释。

## 安装依赖软件

```
apt-get install curl openssh-server ca-certificates postfix -y
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

**注意：首次使用要设置密码**


# 使用 GitLab
基本的 GitLab 就安装好了，通过访问 ip 就可以正常使用 GitLab。GitLab 还有很多可以自定义的配置，下面来看如何配置。
GitLab 的配置文件是`/etc/gitlab/gitlab.rb`

## GitLab 自定义域名

```
// edit /etc/gitlab/gitlab.rb
external_url 'http://gitlab.example.com'

//重新生成配置
gitlab-ctl reconfigure
```

## 更改 GitLab 默认仓库目录
默认 GitLab 仓库存储目录是 `/var/opt/gitlab/git-data`，如果要定义其他路径，变更下面配置
```
// edit `/etc/gitlab/gitlab.rb`
git_data_dirs({"default" => "/var/opt/gitlab/git-data"})
git_data_dirs({"default" => "/mnt/nas/git-data"})

// 或者添加另外一个存储路径
git_data_dirs({
  "default" => "/var/opt/gitlab/git-data",
  "alternative" => "/mnt/nas/git-data"
})
//重新生成配置
gitlab-ctl reconfigure

// 如果移动仓库路径
gitlab-ctl stop
rsync -av /var/opt/gitlab/git-data/repositories /mnt/nas/git-data/
sudo gitlab-ctl upgrade
ls /mnt/nas/git-data/
sudo gitlab-ctl start
```

## GitLab 启用 HTTPS

### 变更 URL

```
external_url 'https://gitlab.example.com'
// 或者开启 HTTP 转 HTTPS
external_url "https://gitlab.example.com"
nginx['redirect_http_to_https'] = true
```

### 生成 SSL 证书

-  生产 SSL 证书 脚本

```
#!/bin/bash
# create self-signed server certificate:
read -p "Enter your domain [www.example.com]: " DOMAIN
echo "Create server key..."
openssl genrsa -des3 -out $DOMAIN.key 1024

echo "Create server certificate signing request..."
SUBJECT="/C=US/ST=Mars/L=iTranswarp/O=iTranswarp/OU=iTranswarp/CN=$DOMAIN"
openssl req -new -subj $SUBJECT -key $DOMAIN.key -out $DOMAIN.csr
echo "Remove password..."

mv $DOMAIN.key $DOMAIN.origin.key
openssl rsa -in $DOMAIN.origin.key -out $DOMAIN.key

echo "Sign SSL certificate..."
openssl x509 -req -days 3650 -in $DOMAIN.csr -signkey $DOMAIN.key -out $DOMAIN.crt

echo "TODO:"
echo "Copy $DOMAIN.crt to /etc/nginx/ssl/$DOMAIN.crt"
echo "Copy $DOMAIN.key to /etc/nginx/ssl/$DOMAIN.key"
echo "Add configuration in nginx:"
echo "server {"
echo "    ..."
echo "    listen 443 ssl;"
echo "    ssl_certificate     /etc/nginx/ssl/$DOMAIN.crt;"
echo "    ssl_certificate_key /etc/nginx/ssl/$DOMAIN.key;"
echo "}"
```

- 生成 SSL 证书

```
sh create_ssl.sh
subject=/C=US/ST=Mars/L=iTranswarp/O=iTranswarp/OU=iTranswarp/CN=gitlab.example.com
Getting Private key
TODO:
Copy gitlab.example.com.crt to /etc/nginx/ssl/gitlab.example.com.crt
Copy gitlab.example.com.key to /etc/nginx/ssl/gitlab.example.com.key
Add configuration in nginx:
server {
    ...
    listen 443 ssl;
    ssl_certificate     /etc/nginx/ssl/gitlab.example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/gitlab.example.com.key;
}
```

- 拷贝 SSL 证书

```
mkdir -p /etc/gitlab/ssl
chmod 700 /etc/gitlab/ssl
cp gitlab.8864.com.key gitlab.8864.com.crt /etc/gitlab/ssl/
```

- 更改 GitLab 配置

```
nginx['enable'] = true
nginx['redirect_http_to_https'] = true
nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.example.crt"
nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.example.com.key"

// 配置生效
gitlab-ctl reconfigure
```

## 配置邮件提醒

- 开启邮件

```
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = 'gitlab@example.com'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'
gitlab_rails['gitlab_email_reply_to'] = 'noreply@example.com'、

gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "mail.example.com"
gitlab_rails['smtp_port'] = 25
gitlab_rails['smtp_user_name'] = "gitlab@example.com"
gitlab_rails['smtp_password'] = "password"
gitlab_rails['smtp_domain'] = "example.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
```
