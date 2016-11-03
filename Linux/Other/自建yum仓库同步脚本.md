### 自建yum仓库
自建内部yum仓库，提高软件安装速度和方便性，同时不需要对新服务器开通对公网的访问权限，也提高了安全性。

### 系统环境
安装httpd作为web server，提供文件下载。安装环境请参考cobbler安装。

### 同步脚本
```
#!/bin/bash
######################################################
## Title: Rsync CentOS\EPEL Yum Mirrors Script      ##
## Version: 1.0                                     ##
## Date: 2015-12-17                                 ##
## Author: Charlie.Cui                              ##
## Email: charlie.cui127@gmail.com
## License: General Public License (GPL)            ##
## Copyright© 2015, Charlie.Cui All Rights Reserved ##
######################################################
Date=`date +%Y%m%d`
LogFile="/tmp/update_mirror.log"
_TrunkVer="epel centos ubuntu ubuntu-releases archlinux"
COMMAND=/usr/bin/rsync
Option="-vazrtopg --progress --delete"
YumWebsite="rsync://mirrors.yun-idc.com"
for Class in $_TrunkVer;do
echo "----$Date `date +%T` Begin Rsync $Class-------">> $LogFile
_Path=/data/mirrors/$Class/
$COMMAND $Option $YumWebsite/$Class/ $_Path >> $LogFile
echo "----$Date `date +%T` Complate Rsync $Class--------">> $LogFile
done
```
