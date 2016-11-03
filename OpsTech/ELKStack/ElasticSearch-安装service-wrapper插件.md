使用elasticsearch-servicewrapper这个es插件，它支持通过参数，指定是在后台或前台运行es，并且支持启动，停止，重启es服务（默认es脚本只能通过ctrl+c关闭es）

### 下载软件包：
```
wget https://github.com/elasticsearch/elasticsearch-servicewrapper/archive/master.zip -O elasticsearch-servicewrapper.zip
```
### 解压、拷贝：
```
unzip elasticsearch-servicewrapper.zip 
mv elasticsearch-servicewrapper-master/service/ /usr/local/elasticsearch/bin/
```

### 执行：
```
bin/service/elasticsearch +
console 在前台运行es
start 在后台运行es
stop 停止es
install 使es作为服务在服务器启动时自动启动
remove 取消启动时自动启动
```

在service目录下有个elasticsearch.conf配置文件，主要是设置一些java运行环境参数，其中比较重要的是下面的
参数：
```
#es的home路径，不用用默认值就可以
set.default.ES_HOME=
#分配给es的最小内存
set.default.ES_MIN_MEM=256
#分配给es的最大内存
set.default.ES_MAX_MEM=1024

# 启动等待超时时间（以秒为单位）
wrapper.startup.timeout=300
# 关闭等待超时时间（以秒为单位）
wrapper.shutdown.timeout=300
# ping超时时间(以秒为单位)
wrapper.ping.timeout=300
```
