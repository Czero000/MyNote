title: expect实现scp或ssh登录
date: 2016/12/09 10:45:50
updated: 2016/12/09 10:45:50
categories:
- 运维自动化
- expect
---
expect 是一种交互语言，可以为 shell 脚本提供交互方式

- scp 

```
#!/bin/bash

read -p "`whoami`@server Password:" -s -r passwd ;echo -e "\n"
passwd=$(echo ${passwd}|sed 's/[^[:alnum:]]/\\&/g')

expect -c "
    set timeout 600
    spawn /usr/bin/scp `whoami`@$1:/root/test.txt /root/
    expect {
        \"*yes/*no\" {send \"yes\r\"; exp_continue}
        \"*assword\" {set timeout 300;send \"$passwd\r\";}
    }
    expect eof"|grep -v 'spawn'
```


- SSH

```
#!/bin/bash

read -p "`whoami`@$1 Password:" -s -r passwd ;echo -e "\n"
passwd=$(echo ${passwd}|sed 's/[^[:alnum:]]/\\&/g')

expect -c "
    set timeout 600
    spawn /usr/bin/ssh `whoami`@$1 $2;
    expect {
        \"*yes/*no\" {send \"yes\r\"; exp_continue}
        \"*assword\" {set timeout 300;send \"$passwd\r\";}
    }
    expect eof"|grep -v 'spawn'
```
