由于某些不可抗因素，Python官方的包在国内有时无法访问或出现网络不稳定现象。为了解决这个问题就需要将Pip中自带的源地址修改为镜像地址。

目前收集的比较好的镜像地址有：
```
http://pypi.v2ex.com/simple/
http://pypi.douban.com/simple/
http://mirrors.aliyun.com/pypi/simple/
```

- 直接修改配置的方法`~/.pip/pip.conf`

```
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple/
```

- 不改配置文件，每次手动指定

```
pip install -i http://<mirror>/simple <package>
pip install -i http://pypi.douban.com/simple simplejson
```
