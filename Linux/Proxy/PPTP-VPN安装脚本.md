```
#!/bin/bash
########################################################
## Description: pptpd Install PPTP VPN For rhel5.x_x64##
## Version: 1.0                                       ##
## Date: 2015-08-05                                   ##
## Author: Charlie.Cui                                ##
## Mail: Charlie.cui127@gmail.com                      ##  
## License: General Public License (GPL)              ##
## Copyright© 2015, Charlie.Cui All Rights Reserved   ##
########################################################
yum remove -y pptpd ppp
iptables --flush POSTROUTING --table nat
iptables --flush FORWARD
rm -rf /etc/pptpd.conf
rm -rf /etc/ppp
wget http://poptop.sourceforge.net/yum/stable/packages/kernel_ppp_mppe-1.0.2-3dkms.noarch.rpm
wget http://poptop.sourceforge.net/yum/stable/packages/dkms-2.0.17.5-1.noarch.rpm
wget http://poptop.sourceforge.net/yum/stable/packages/ppp-2.4.4-14.1.rhel5.x86_64.rpm
wget http://poptop.sourceforge.net/yum/stable/packages/pptpd-1.4.0-1.rhel5.x86_64.rpm
yum -y install make libpcap iptables gcc-c++ logrotate tar cpio perl pam tcp_wrappers
rpm -ivh dkms-2.0.17.5-1.noarch.rpm
rpm -ivh kernel_ppp_mppe-1.0.2-3dkms.noarch.rpm
rpm -ivh ppp-2.4.4-14.1.rhel5.x86_64.rpm
rpm -ivh pptpd-1.4.0-1.rhel5.x86_64.rpm
mknod /dev/ppp c 108 0
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "mknod /dev/ppp c 108 0" >> /etc/rc.local
echo "echo 1 > /proc/sys/net/ipv4/ip_forward" >> /etc/rc.local
echo "localip 172.16.6.1" >> /etc/pptpd.conf
echo "remoteip 172.16.6.2-254" >> /etc/pptpd.conf
echo "ms-dns 8.8.8.8" >> /etc/ppp/options.pptpd
echo "ms-dns 8.8.4.4" >> /etc/ppp/options.pptpd
vpnpass=`openssl rand 6 -base64`
if [ "$1" != "" ]
then vpnpass=$1
fi
echo "vpnuser pptpd ${vpnpass} *" >> /etc/ppp/chap-secrets
iptables -t nat -A POSTROUTING -s 172.16.6.0/24 -j SNAT --to-source `ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -
f2 | awk 'NR==1 { print $1}'`
iptables -t nat -A POSTROUTING -s 192.38.38.0/255.255.255.0 -d 192.168.48.116 -o eth1 -j SNAT --to-source 192.168.39.250 
chkconfig pptpd on
service pptpd start
echo "VPN service is installed, your VPN username is vpn, VPN password is ${pass}"
```
