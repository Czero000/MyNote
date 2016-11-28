#!/bin/bash
#Uage: expect_hosts iplist Command

Usage () {         
        echo "Usage: $0 [iplist] [Command]"
} 

ssh_exec() {
for i in `egrep "^[1-9]{1,3}.[1-9]{1,3}.[1-9]{1,3}.[1-9]{1,3}" $1`
do 
    expect -c "
        set timeout 600
        spawn /usr/bin/ssh `whoami`@$i $2;
        expect {
            \"*yes/*no\" {send \"yes\r\"; exp_continue}
            \"*assword\" {set timeout 300;send \"$passwd\r\";}
        }
        expect eof"|egrep -v "^spawn"
        echo -e "\n"
done
}

[ "$#" -ne 2 ] && { Usage && exit 1; }
[ -f "$1" ] || { echo "No such iplist file..." && exit 2;}

read -p "Enter Host Password: " -s -r passwd ;echo -e "\n"
passwd=$(echo ${passwd}|sed 's/[^[:alnum:]]/\\&/g')

ssh_exec $1 "$2"

