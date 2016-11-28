#!/bin/sh

ssh_exec () {

for i in `grep "^[1-9]" $1|awk -F: '{print $1}'`
        do
        expect -c "
        set timeout 600;
        spawn /usr/bin/ssh $i $2;
        expect {
                  \"*yes/no*\" {send \"yes\r\"; exp_continue}
                  \"*password*\" {send \"$passwd\r\";}
                }
        expect eof;"|grep -v 'spawn'
        done
}

[ "$#" -ne 2 ] && echo $"Usage: $0 IPLIST CMDS" && exit 1
[ -f "$1" ] || { echo "No such iplist file..." && exit 2;}
read -p "Password:" -s passwd ;echo -e "\n"
passwd=$(echo ${passwd}|sed 's/[^[:alnum:]]/\\&/g')

CLIENT=${SSH_CLIENT##*:}

ssh_exec $1 "$2"
