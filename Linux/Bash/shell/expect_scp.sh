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
    expect eof|grep -v 'spawn'
"
