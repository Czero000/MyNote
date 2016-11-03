I am using Centos7 + smokeping-2.6.9 lets start up by install needed package before that, we will need to enable Epel repo You can install EPEL by running yum install epel-release. The package is included in the CentOS Extras repository, enabled by default.
### install epel
```
yum install epel-release
```
Then follow up by the package for:

* mod_fcgid
* httpd
* httpd-devel
* rrdtool
* perl-CGI-SpeedyCGI
* fping
* rrdtool-perl
* perl
* perl-Sys-Syslog

```
yum install mod_fcgid httpd httpd-devel rrdtool perl-CGI-SpeedyCGI fping rrdtool-perl perl perl-Sys-Syslog
```

### install perl modules
Then we will needed some package for Cpan to install perl stuff
```
yum install perl-CPAN perl-local-lib perl-Time-HiRes
```
The last one is the package to create installation for smokeping
```
# yum groupinstall "Development tools"
```


### install smokeping
```
\\ Now lets download the latest smokeping at http://oss.oetiker.ch/smokeping/pub currently the latest i saw is 2.6.9, so i just download that
wget http://oss.oetiker.ch/smokeping/pub/smokeping-2.6.9.tar.gz

\\ then extract it
tar -zxvf smokeping-2.6.9.tar.gz

\\ Install the smokeping perl stuff
cd smokeping-2.6.9/setup
./build-perl-modules.sh

\\ it will auto install needed perl
\\ Once done, back to smokeping-2.6.9 folder and you will notice a folder name thirdparty is created
\\ we will need to move it to /usr/local/smokeping folder, but before that, lets create smokeping folder at /usr/local/smokeping first
\\ then copy the thirdparty folder into it
mkdir /urs/local/smokeping
cp -r thirdparty /usr/lcoal/smokeping/

./configure --prefix=/usr/local/smokeping PERL5LIB=/usr/lib64/perl5/
make
make install
```

**Note:  if you encounter problem, please try make install again
this is because for my situation when i first make install, it pop some error but when i try make install again, the error gone**

Now you can go to /usr/local/smokeping/etc and prepare the config file

### install httpd
Now is time to prepare for the interface make sure you had install apache else please install it using yum install httpd
```
yum install httpd -y
```

### smokeping config
```
cd /usr/local/smokeping/etc
for foo in *.dist; do cp $foo `basename $foo .dist`; done
mv /usr/local/smokeping/htdocs/smokeping.fcgi.dist /usr/local/smokeping/htdocs/smokeping.fcgi

\\edit smokeping.conf
vim /etc/httpd/conf.d/smokeping.conf

Alias /ping /usr/local/smokeping/htdocs/

       DirectoryIndex index.html smokeping.fcgi
       Options +ExecCGI
       #AllowOverride None
       AddHandler cgi-script .cgi .fcgi
       Order allow,deny
       Allow from all
       AuthName "Smokeping Access"
       AuthType Basic
       AuthUserFile /usr/local/smokeping/htdocs/htpasswd.user
       Require valid-user


chmod 600 /usr/local/smokeping/etc/smokeping_secrets
mkdir -p /usr/local/smokeping/htdocs/cache
mkdir /usr/local/smokeping/data
mkdir /usr/local/smokeping/var


chown nobody:nobody /usr/local/smokeping/var
chown nobody:nobody /usr/local/smokeping/data
chown nobody:nobody /usr/local/smokeping/htdocs/cache

\\Before we start smokeping, please edit your configuration first edit the smokeping config to your need (change the part in Red color word

vim /usr/local/smokeping/etc/config
*** General ***

owner    = Charlie.cui
contact  = some@address.nowhere
mailhost = my.mail.host (Ignore if you do not have smtp server)
sendmail = /usr/sbin/sendmail
# NOTE: do not put the Image Cache below cgi-bin
# since all files under cgi-bin will be executed ... this is not
# good for images.
imgcache = /usr/local/smokeping/cache
imgurl   = cache
datadir  = /usr/local/smokeping/data
piddir  = /usr/lcoal/smokeping/var
cgiurl   = http://some.url/smokeping.cgi
smokemail = /usr/local/smokeping/etc/smokemail.dist
tmail = /usr/local/smokeping/etc/tmail.dist
# specify this to get syslog logging
syslogfacility = local0
# each probe is now run in its own process
# disable this to revert to the old behaviour
# concurrentprobes = no

*** Alerts ***
to = alertee@address.somewhere
from = smokealert@company.xy

+someloss
type = loss
# in percent
pattern = >0%,*12*,>0%,*12*,>0%
comment = loss 3 times  in a row

*** Database ***

step     = 300
pings    = 20

# consfn mrhb steps total

AVERAGE  0.5   1  1008
AVERAGE  0.5  12  4320
    MIN  0.5  12  4320
    MAX  0.5  12  4320
AVERAGE  0.5 144   720
    MAX  0.5 144   720
    MIN  0.5 144   720

*** Presentation ***

template = /usr/local/smokeping/etc/basepage.html.dist

+ charts

menu = Charts
title = The most interesting destinations

++ stddev
sorter = StdDev(entries=>4)
title = Top Standard Deviation
menu = Std Deviation
format = Standard Deviation %f

++ max
sorter = Max(entries=>5)
title = Top Max Roundtrip Time
menu = by Max
format = Max Roundtrip Time %f seconds

++ loss
sorter = Loss(entries=>5)
title = Top Packet Loss
menu = Loss
format = Packets Lost %f

++ median
sorter = Median(entries=>5)
title = Top Median Roundtrip Time
menu = by Median
format = Median RTT %f seconds

+ overview

width = 600
height = 50
range = 10h

+ detail

width = 600
height = 200
unison_tolerance = 2

"Last 3 Hours"    3h
"Last 30 Hours"   30h
"Last 10 Days"    10d
"Last 400 Days"   400d

#+ hierarchies
#++ owner
#title = Host Owner
#++ location
#title = Location

*** Probes ***

+ FPing

binary = /usr/sbin/fping

*** Slaves ***
secrets=/usr/local/smokeping/etc/smokeping_secrets.dist
+boomer
display_name=boomer
color=0000ff

+slave2
display_name=another
color=00ff00

*** Targets ***

probe = FPing

menu = Top
title = Network Latency Grapher
remark = Welcome to the SmokePing website of xxx Company. \
         Here you will learn all about the latency of our network.

+ Server
menu= Targets

++ google

menu = google.com
title = google.com
alerts = someloss
host = www.google.com
```
###Start the apache service
```
systemctl start httpd
```

start the smokeping services
```
/usr/local/smokeping/bin/smokeping --config=/usr/local/smokeping/etc/config --logfile=/var/log/smokeing.log
```
### For startup script
you can get it from here
```
wget http://oss.oetiker.ch/smokeping/pub/contrib/smokeping-start-script
\\ just edit the smokeping path then put at /etc/init.d/
chmod 755 /etc/init.d/smokeping
```
