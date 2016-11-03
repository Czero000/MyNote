Git 是通过 ssh方式访问，例如 GitHub，当用户访问 Github 上的仓库时，用户会将本地的 `~/.ssh/id_rsa` 与上传到 GitHub 的公钥进行验证。但是在实际情况，很多会有自己的内部 git 仓库，或者是私人创建的仓库，当要求每个 git 仓库要使用不同 ssh-key 时，应该如何配置呢。

- 生成 ssh-key

```
ssh-keygen -t rsa -C 'user@mail.com' -f id_rsa_github1
ssh-keygen -t rsa -C 'user@mail.com' -f id_rsa_github2   
```

- 创建 config 配置文件

该文件可以定义不同 ssh-key 访问不同 git仓库
```
cat ~/.ssh/config
Host github1.com                         \\ 别名
    hostname github.com                 \\ 仓库地址
    IdentityFile ~/.ssh/id_rsa.github   \\ ssh-key
    user github1                         \\ 登录用户

Host github2.com
    hostname github.com
    IdentityFile ~/.ssh/id_rsa.github2
    user github2
```

- 连接远程仓库
```
git clone git@github1.com:github1/test.git

git clone git@github2.com:github2/test.git
```

这样就可以使用不同 ssh-key 来访问不同 GitHub 仓库。
