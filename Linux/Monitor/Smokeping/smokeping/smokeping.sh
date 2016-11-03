#!/bin/bash
###########################################
#Write: By Charlie.cui                    #
#DATE: 2015-06-05			  #	
#Description: Auto Install Smokeping      #
###########################################
. /etc/rc.d/init.d/functions
PATH_root="$PWD"
soft_dir='/usr/local/smokeping'
IP=`ifconfig|grep "inet addr"|awk '{print $2}'|awk -F ":" '{print $2}'|egrep  -v "^127"|head -1`

#install pkg
pkg() {
echo "Yum Install Dependencies"
rpm -Uvh  http://mirrors.sohu.com/fedora-epel/epel-release-latest-6.noarch.rpm
yum install gcc gcc-c++ cairo-devel libxml2-devel pango-devel pango libpng-devel freetype freetype-devel libart_lgpl-devel libidn libidn-devel httpd httpd-devel apr-util-devel apr-devel facter  perl-ExtUtils-MakeMaker -y
yum groupinstall "chinese support" -y
}

#install rrdtool
rrdtool() {
cd $PATH_root
wget http://oss.oetiker.ch/rrdtool/pub/rrdtool-1.4.7.tar.gz
[ -f rrdtool-1.4.7.tar.gz ] &&  tar -zxf rrdtool-1.4.7.tar.gz
[ -d rrdtool-1.4.7 ] && cd rrdtool-1.4.7 && ./configure --prefix=/usr/local/rrdtool && make && make install 
}

#install fping
fping() {
cd $PATH_root
wget http://oss.oetiker.ch/smokeping/pub/fping-2.4b2_to3-ipv6.tar.gz
[ -f fping-2.4b2_to3-ipv6.tar.gz ] &&  tar -zxf fping-2.4b2_to3-ipv6.tar.gz
[ -d fping-2.4b2_to3-ipv6 ] && cd fping-2.4b2_to3-ipv6 && ./configure && make && make install 
}

#install fcgi
fcgi() {
cd $PATH_root
wget  http://cpan.communilink.net/authors/id/F/FL/FLORA/FCGI-0.74.tar.gz
[ -f FCGI-0.74.tar.gz ] &&  tar -zxf FCGI-0.74.tar.gz
[ -d FCGI-0.74 ] && cd FCGI-0.74 && perl Makefile.PL && make && make install                            
}

#install mod_fastcgi
mod_fastcgi() {
cd $PATH_root
wget  http://www.fastcgi.com/dist/mod_fastcgi-2.4.6.tar.gz
[ -f mod_fastcgi-2.4.6.tar.gz ] &&  tar -zxf mod_fastcgi-2.4.6.tar.gz
[ -d  mod_fastcgi-2.4.6 ] && cd mod_fastcgi-2.4.6 && apxs -o mod_fastcgi.so -c *.c && apxs -i -a -n fastcgi .libs/mod_fastcgi.so
}

#install smokeping
smokeping(){
architecture=`facter architecture`
cd $PATH_root
wget http://oss.oetiker.ch/smokeping/pub/smokeping-2.6.9.tar.gz
[ -f smokeping-2.6.9.tar.gz ] && tar -zxf smokeping-2.6.9.tar.gz
[ -d smokeping-2.6.9 ] && cd smokeping-2.6.9  
if [ $architecture == x86_64 ];then
	./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib64/perl5/
	if [ $? -ne 0 ];then
	./setup/build-perl-modules.sh /usr/local/smokeping/thirdparty
	ln -s `find /usr/local/rrdtool/ -name RRDs.so` /usr/lib64/perl5/
	ln -s `find /usr/local/rrdtool/ -name RRDs.pm` /usr/lib64/perl5/
	./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib64/perl5/ && make && make install 
	else
	make && make install
	fi
else
	./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib/perl5/
	if [ $? -ne 0 ];then
	./setup/build-perl-modules.sh /usr/local/smokeping/thirdparty
        ln -s `find /usr/local/rrdtool/ -name RRDs.pm` /usr/lib/perl5/
        ln -s `find /usr/local/rrdtool/ -name RRDs.so` /usr/lib/perl5/
	./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib/perl5/ && make && make install
	else 
	make && make install 
	fi
fi
}
config() {
cd $soft_dir/etc
mv config.dist config
mv basepage.html.dist basepage.html
mv smokemail.dist smokemail
mv tmail.dist tmail
mv smokeping_secrets.dist smokeping_secrets
mv $soft_dir/htdocs/smokeping.fcgi.dist $soft_dir/htdocs/smokeping.fcgi
chmod 400 smokeping_secrets
mkdir /usr/local/smokeping/{htdocs/cache,var,data}
chown nobody:nobody /usr/local/smokeping/{htdocs/cache,var,data} 
cd $PATH_root
rsync -azvh config /usr/local/smokeping/etc/
rsync -azvh config.d /usr/local/smokeping/etc/
rsync -azvh smokeping.conf /etc/httpd/conf.d/
rsync -azvh Graphs.pm /usr/local/smokeping/lib/Smokeping
rsync -azvh Graphs.pm /usr/local/smokeping/lib/Smokeping
chmod +s /usr/local/sbin/fping
chown nobody:nobody /var/log/httpd/fastcgi/dynamic
rsync -azvh httpd.conf /etc/httpd/conf/httpd.conf   
/etc/init.d/httpd restart
sudo -u nobody /usr/local/smokeping/bin/smokeping --logfile=/var/log/smokeping.log 
}
pkg
rrdtool
fping
fcgi
mod_fastcgi
smokeping
config
