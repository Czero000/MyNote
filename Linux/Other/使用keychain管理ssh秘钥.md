## 配置 SSH 免密码登陆

### 生成 SSH 密码
```
// 生成的秘钥是有密码加密的
ssh-keygen -q
Enter file in which to save the key (/home/charlie/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

### 将 ssh 公钥传到要登陆的机器上
```
ssh-copy-id 172.16.11.211
```

### 直接登陆
```
// 直接登陆会提示输出秘钥的密码
ssh 172.16.11.211
Enter passphrase for key '/root/.ssh/id_rsa':
```

### 使用 ssh-agent，实现免密码登陆
```
// 每次要登陆都需要重复下面两个命令
ssh-agent bash
ssh-add
```

### 使用 ssh-keychain
```
// 安装
apt install keychain

// 编辑脚本
vim run_keychain.sh
#!/bin/sh
#
keychain ~/.ssh/id_rsa

// 执行脚本后回生成 keychain 配置并加入环境变量中
source .keychain/MY-45-24-sh  
echo "source .keychain/MY-45-24-sh " >> /root/.bashrc
```
这样每次登陆之后就可以直接免密码登陆机器了。
