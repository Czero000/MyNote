## apache添加cgi模块
Apache需要运行cgi程序的，却发现先前编译安装Apache的时候，没有安装Apache的cgi模块。
```
cd /usr/local/src/httpd-2.2.25/modules/generators
/usr/local/apache/bin/apxs -i -a -c mod_cgi.c
```
省略部分内容
```
chmod 755 /usr/local/apache/modules/mod_cgi.so
[activating module `cgi' in /usr/local/apache/conf/httpd.conf]ap
```

apxs参数介绍：
* -i：表示要执行安装操作
* -a：自动添加一个LoadModule行到httpd.conf文件中，使模块激活

