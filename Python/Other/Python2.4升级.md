RHEL5.4系统中自带的Python版本是2.4，但是目前许多基于Python的应用要求的Python版本都要高于2.4，在升级Python版本时不要卸载Python2.4在安装Python2.7，这样会有很多的问题，保守的方法是直接安装Python2.7的源码包（系统中有很多程序依赖Python）

#### 系统版本
```
lsb_release -a
LSB Version:    :core-3.1-ia32:core-3.1-noarch:graphics-3.1-ia32:graphics-3.1-noarch
Distributor ID: RedHatEnterpriseServer
Description:    Red Hat Enterprise Linux Server release 5.4 (Tikanga)
Release:        5.4
Codename:       Tikanga
```

#### Python版本
```
python -V
Python 2.4.3
```

#### 下载并安装Python2.7

```
cd /usr/local/src
wget www.python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2
tar -jxf Python-2.7.2.tar.bz2  
cd Python-2.7.2
./configure
make && make install 
```

Python2.7安装后路径默认是/usr/local/lib/python2.7，查看Python版本

```
/usr/local/bin/python2.7 -V
Python 2.7.2
```

#### 建立软连接，使系统默认的Python指向Python2.7
正常情况下，即使Python2.7安装成功后，系统默认的Python版本仍然是2.4
```
python -V
Python 2.4.3
```

#### 将系统默认的Python指到2.7
```
mv /usr/bin/python /usr/bin/python.bak
ln -s /usr/local/bin/python2.7 /usr/bin/python
```

#### 测试是否成功
```
python -V
Python 2.7.2
```

#### yum工具是基于Python2.4才能运行
```
edit /usr/bin/yum
#!/usr/bin/python => #!/usr/bin/python2.4
```
这样yum工具就可以正常使

---
## [DigitalOcean的VPS，稳定、便宜，用于搭建自己的站点和梯子，现在注册即得10$,免费玩2个月](https://www.digitalocean.com/?refcode=9e4ab85e22ec) ##