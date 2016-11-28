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
    expect eof|grep -v 'spawn'
"
