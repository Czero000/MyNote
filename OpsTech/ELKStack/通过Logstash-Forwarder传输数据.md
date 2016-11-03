logstash 作为无状态的软件，配合消息队列系统，可以很轻松的做到线性扩,Redis 已经帮我们解决了很多的问题，而且也很轻量，为什么我们还需要 logstash-forwarder 呢? 简而言之它很好，但是它不安全。下面开始配置Logstash-forwarder
>Redis provides simple authentication but no transport-layer encryption or authorization. This is perfectly fine in trusted environments. However, if you're connecting to Redis between datacenters you will probably want to use encryption.

简而言之它很好，但是它不安全。下面开始配置Logstash-forwarder

## indexer端配置

在logstash作为index server角色这端，首先要生成证书：
```
cd /etc/pki/tls/
openssl req -subj '/CN=elk.mydomain.com/' -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt
```
如果按照官方文档操作，`logstsh-forwarder`会报错:`Failure connecting to 172.16.11.230: dial tcp elk.mydomain.com:5000: connection refused`，为了避免报错，这里比官方的增加了 ***" -subj '/CN=elk.mydomain.com/'"***。 

然后把证书发送到logstash-forwarder的shipper端服务器上
```
scp private/logstash-forwarder.key 172.16.11.175:/etc/pki/tls/private 
scp certs/logstash-forwarder.crt 172.16.11.175:/etc/pki/tls/certs 
```


创建logstash的配置文件：
> I’m a lumberjack and I’m ok! I sleep when idle, then I ship logs all day! I parse your logs, I eat the JVM agent for lunch! ♫

```
input {
  lumberjack {
    port => 5000
    type => "syslog"
   ssl_certificate => "/etc/pki/tls/certs/logstash-forwarder.crt"
   ssl_key => "/etc/pki/tls/private/logstash-forwarder.key"
  }
}

filter {
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    syslog_pri { }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
}

output {
  stdout { codec => rubydebug }
}
```
这样，logstash index端已经配置完
>lumberjack 是 logstash-forwarder 还没用 Golang 重写之前的名字

**默认安装的logstash会报错：``"The error reported is: uninitialized constant Concurrent::D elay::Executor"``，需要更新`logstash-input-lumberjack`这个插件（国内需要变更更gem 安装的源为https://ruby.taobao.org）**


## shipper端安装
先安装logstash-forwarder软件。
```
wget https://download.elastic.co/logstash-forwarder/binaries/logstash-forwarder-0.4.0-1.x86_64.rpm
rpm -ivh logstash-forwarder-0.4.0-1.x86_64.rpm 
```

配置logstash-forwarder
logstash-frowarder的配置文件是纯JSON格式。配置如下：
```
cat /etc/logstash-forwarder.conf
{
  "network": {
    "servers": [ "elk.mydomain.com:5000" ],
      "timeout": 15,
      "ssl ca" : "/etc/pki/tls/certs/logstash-forwarder.crt",
      "ssl key": "/etc/pki/tls/private/logstash-forwarder.key"
  },
  "files": [
    {
      "paths": [
        "/var/log/message",
        "/var/log/secure"
        ],
      "fields": { "type": "syslog" }
    }
  ]
}
```
这样就可以在index端接受到数据，在通过kibana将数据可视化
