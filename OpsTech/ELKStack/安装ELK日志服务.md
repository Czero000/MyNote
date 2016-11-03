## 什么是ELK
  ELK是ElasticSearch、Logstash、Kibana三个开源软件的组合，这三个产品可以单独使用，但当他们组合在一起使用时，你会发现一个强大的、可扩展的日志服务，而且都是归于Elastic.co公司名下，所以有此简称。
  ELK具有如下几个优点：

* 处理方式灵活：Elasticsearch是实时全文索引，不需要像storm那样预先编程才能使用；
* 配置简、易上手：ElasticSearch全部采用JSON接口，Logstash是Ruby DSL设计，都是目前业界最 通用的配置语法设计；
* 检索性能高效：虽然每次查询都是实时计算，但是优秀的设计和实现基本可以到达百亿级数据查询的秒级响应；
* 集群线性扩展：不管是ElasticSearch集群还是Logstash集群都是可以线性扩展；
*  前端操作绚丽：Kibana界面，只需要点击鼠标，就可以完成搜索、聚合、生成绚丽的仪表盘；

软件介绍：

* ElasticSearch：数据实时检索、分析
* Logstash：  收集、分析、存储数据
* Kibana： 可视化数据
* redis: 日志队列

ELK Stack示意图：
![ELK Stack示意图](http://ofc9x1ccn.bkt.clouddn.com/elk/elk_for_log.png "THe ELK Platform for log management")


## 安装准备

### 系统环境
#### 查看系统：
```shell
cat /etc/redhat-release
CentOS Linux release 7.1.1503 (Core)
```

#### 设置selinux状态
```
getenforce
Disabled`
```

#### 安装EPEL源
```
yum -y install epel-release
```

### 下载软件
* [ElasticSearch]( https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.2.tar.gz)
* [Logstash](https://download.elastic.co/logstash/logstash/logstash-1.5.4.tar.gz)
* [kabana](https://download.elastic.co/kibana/kibana/kibana-4.1.2-linux-x64.tar.gz)
* [redis](http://download.redis.io/releases/redis-3.0.4.tar.gz)

### 安装java支持（ELK Stack需要JAVA支持）

#### 安装JAVA（ORACLE）
```
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u40-b25/jre-8u40-linux-x64.tar.gz"
tar -zxf jre-8u40-linux-x64.tar.gz
chown -R root: jre1.8.0_40
mv jre1.8.0_40/ /usr/local/java
cat >> /etc/profile export JAVA_HOME=/usr/local/java
export JAVA_BIN=/usr/local/java/bin
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME JAVA_BIN PATH CLASSPATH
EOF
source /etc/profile
java -version
java version "1.8.0_40"
Java(TM) SE Runtime Environment (build 1.8.0_40-b25)
Java HotSpot(TM) 64-Bit Server VM (build 25.40-b25, mixed mode)
```

#### 安装OpenJDK
```
yum install -y java-1.8.0-openjdk

```

## 安装ELK Stack
### 安装Redis
```
yum -y install redis
```

### 安装ElasticSearch
#### 安装
```
tar -zxf elasticsearch-1.7.2.tar.gz
mv elasticsearch-1.7.2 /usr/local/elasticsearch
sed -i 's/#network.host: 192.168.0.1/network.host: 172.16.11.230/g' /usr/local/elasticsearch/config/elasticsearch.yml
```

#### 启动
```
/usr/local/elasticsearch/bin/elasticsearch -d
```

#### 测试
```
curl -XGET http://172.16.11.230:9200
{
  "status" : 200,
  "name" : "Chemistro",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "1.7.2",
    "build_hash" : "e43676b1385b8125d647f593f7202acbd816e8ec",
    "build_timestamp" : "2015-09-14T09:49:53Z",
    "build_snapshot" : false,
    "lucene_version" : "4.10.4"
  },
  "tagline" : "You Know, for Search"
}
```
这说明你的ElasticSearch集群已经启动并且正常运行。

### 安装kibana

#### 安装
```
tar -zxf kibana-4.1.2-linux-x64.tar.gz
mv kibana-4.1.2-linux-x64 /usr/local/kibana
sed -i '/host/ s/0.0.0.0/172.16.11.230/g' /usr/local/kibana/config/kibana.yml
sed -i '/elasticsearch_url/ s/localhost/172.16.11.230/g' /usr/local/kibana/config/kibana.yml
```

#### 配置启动（通过Systemctl来控制）
```
cat >> /etc/systemd/system/kibana4.service  [Service]
ExecStart=/usr/local/kibana/bin/kibana
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=kibana4
User=root
Group=root
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
```
#### 启动kabana
```
systemctl enable kibana4.service       
ln -s '/etc/systemd/system/kibana4.service' '/etc/systemd/system/multi-user.target.wants/kibana4.service'
systemctl start kibana4
```
登录`172.16.11.230:5601`出现下面界面说明安装成功
![kibana_logo](http://ofc9x1ccn.bkt.clouddn.com/elk/kibana_logo.png?imageView/2/w/619/q/90 "kibani登录界面")


### 安装Logstash
```
tar -zxf logstash-1.5.4.tar.gz
mv logstash-1.5.4 /usr/local/logstash
```

### 安装nginx服务（反向代理）
#### 安装
```
yum install openssl-devel pcre-devel -y
tar -zxf nginx-1.7.3.tar.gz
cd nginx-1.7.3/
./configure --prefix=/usr/local/nginx --group=nobody --user=nobody --with-http_stub_status_module --with-http_ssl_module --with-pcre
make && make install
```

#### 配置
```
cat kibana.conf
server {
       listen  80;
        server_name     elk.mydomain.com;
        charset utf-8;
        index index.html;
        root /usr/local/nginx/html;
        access_log  logs/elk.mydomain.com_access.log combined;
        error_log   logs/elk.mydomain.com_error.log;
        location / {
                proxy_pass      http://172.16.11.230:5601$request_uri;
                proxy_set_header Host $http_host;
        }
}
```
#### 配置启动脚本
```
cat /etc/systemd/system/nginx.service
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=process
KillSignal=SIGQUIT
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

启动nginx，访问`elk.mydomain.com`是不是就跳转到kibana的界面了呢
