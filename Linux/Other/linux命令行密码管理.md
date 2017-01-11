title: linux命令行密码管理
date: 2016/12/09 11:02:45
updated: 2016/12/09 11:02:45
categories:
- Linux系统
- Other
---
# 软件：pass

## 安装软件包
```
apt install pass
```

## 初始化仓库
```
gpg --gen-key
pass init <gpg-id>
```
*该命令会在`~/.password-store`目录中创建一个密码仓库*

## 添加新的密码信息
```
pass insert <password-name> -m
```

## 查看密码名称列表
```
pass
```

## 复制密码到剪切板
```
pass -c <password-name>
```

## 粘帖剪切板中密码
```
Ctrl + Shift + v
```

## 移除密码记录
```
pass rm <password-name>
```
