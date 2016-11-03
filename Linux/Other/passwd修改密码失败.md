### 问题
今天增加一用户时，出现以下情况
```
[root@ssq-54-104 ~]# passwd root
Changing password for user root.
New UNIX password:
/usr/share/cracklib/pw_dict: error reading header
PWOpen: Success
```
### 解决方法
```
yum reinstall -y cracklib-dicts
```
>CrackLib是一个可用于类UNIX系统下的函数库,   一般来说,   通常只使用其中的一个函数.它可以用于编写和passwd有关的程序中,   其基本思想是很简单的,   就是防止用户使用过于简单,   容易被猜测出来或容易被一些工具搜索到的密码.CrackLib并不是一个可以直接运行使用的程序,   它是一个函数库,   你可以利用其中的函数写自己的程序,   或是加入其它程序中,   用来提高安全性.   比如,   你可以重写passwd,使用户在选择密码时受到限制CrackLib使用一个字典,   它查找字典以判断所选用密码是否是不安全的密码,   所以你也可以加入其它信息,   使用自己的字典.比如,   加入公司的名称,   实验室墙上的单词等等潜在的不安全密码.
