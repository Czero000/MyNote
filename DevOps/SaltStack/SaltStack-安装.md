## 初识SaltStack

### 什么是SaltStack###

SaltStack是继Puppet、Chef之后新出现的配置管理及远程执行工具。SaltStack是基于Python开发的一套C/S架构配置关机工具，底层使用ZeroMQ消息队列pub/sub方式通信，使用SSL证书剪发的方式进行认证管理。与Puppet相比，SaltStack没有那么笨重，较为轻量，不想Puppet有一套自己的DSL用来编写配置。SaltStack使用YAML作为配置文件格式，这样写起来既简单有容易，同时也便于动态生成；此外SaltStack在远程执行命令时的速度也非常快，并包含丰富的模块，SaltStack很好的包含了状态管理的优点，大大提好运维人员的工作效率。简单总结有两大用处：

- **配置管理系统，能够维护预定义状态的远程节点（比如，确保指定的软件包被安装和特定的服务在运行）**
- **一个分布式远程执行系统，用来在远程节点上执行命令和查询数据，可以单个节点，也可以是选定规则**

![salt_functions](http://ofc9x1ccn.bkt.clouddn.com/saltstack/salt_functions.png)]

**SaltStack特点**

**简单：**

    兼顾大规模部署和小规模系统环境，Salt非常简单配置和维护，不管是本地网络系统，还是跨数据中心。salt采用C/S架构，需要的功能内建到一组daemon中，只需要简单的配置就可以工作，也可以调整来满足自己特定需求。

**并行执行：**

- 通过并行方式让远程节点执行命令
- 采用安全的加密协议
- 最小、最快使用网络和负责
- 提供简单的编程接口
- 提供更细粒度的控制，使系统不止按照主机名，还允许按照系统属性来分类

**成熟技术之上构建：**

- 网络层采用优秀的ZeroMQ库，salt的守护进程包含可行和透明的AMQ代理
- 使用公钥和Master端通信，使用更快的AES加密协议，集成认证和加密在Salt中
- 使用msgpack通讯，所以更快速和更轻量网络交换

**Python客户端接口：**

- 允许简单的拓展，Salt程序可以写成Python模块，Client收集数据发送回Master或者其他程序
- 可以从简单的Python API调用或者从命令行调用，因此可以执行一次命令或者大型应用程序的一部分

**快速、灵活、可扩展：**

- 高速在一台或者一组服务器执行命令
- 速度快、配置简单、扩展性好，提供远程执行架构，可以管理任意数量的多样化需求的服务器
- 集成最好的远程执行工具，增强处理能力、拓展使用范围，可以使用多样化复杂的网络

**开源：**

Salt是在Apache 2.0 Licence下开发，可以用在开源或者私有项目

 ![salt-module](http://ofc9x1ccn.bkt.clouddn.com/saltstack/salt-module.png)

---

### **支持的系统**

常见的发行版都已被支持：
- Arch Linux
- Debian
- Fedora
- FreeBSD
- Gentoo
- OS X
- RHEL / CentOS / Scientific Linux / Amazon Linux / Oracle Linux（EPEL5、EPEL6、EPEL7）
- Sloaris
- Ubuntu
- Windows
- SUSE

## 安装SaltStack

### SaltStack软件依赖
由于SaltStack是基于Python开发，对Python版本和python模块有一定要求。

- Python：版本大于2.6、小于3.0
- msgpack-python ：高性能消息交换格式
- YAML：SaltStack配置解析定义语法
- Jinja2：SaltStack配置模版
- MarkupSafe：Python unicode转换库
- apache-libcloud：SaltStack对云架构编排库
- Requests：HTTP Python库
- ZeroMQ：SaltStack消息系统
  - pyzmq：ZeroMQ Python库
  - PyCrypto：Python密码库
  - M2Crypto：Openssl Python包装库

### 安装SaltStack

SaltStack提供了四种安装方式（yum、pip、源码、salt-bootstrap），部署环境为`CentOS Linux release 7.1.1503 (Core)`

- Master（172.16.11.210）

```shell
rpm -ivh http://mirrors.yun-idc.com/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
yum install salt-master -y
systemctl start salt-master
```
- Minion（172.16.11.211）
```shell
rpm -ivh http://mirrors.yun-idc.com/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
yum install salt-minion -y
sed -i 's/#master: salt/master: 172.16.11.210/g' /etc/salt/minion   // 这里为Master的ip地址
echo "172.16.11.211" > /etc/salt/minion_id                          // 在Master认证是显示的minion id
systemctl start salt-minion
```
---
## SaltStack证书管理

Salt在master和minion通信使用AES加密，保证发给minion的指令安全，Master和minion之间认证采用信任接受的Key，在发送命令到minion之前，minon的key需要先被master所接受，运行salt-key可以列出当前key状态。

```shell
salt-key -L                                // 查看当前证书情况
 Accepted Keys:
 Denied Keys:
 Unaccepted Keys:
 172.16.11.211
 Rejected Keys:

salt-key -A -y                              // 同意签证所有没接受的请求                                 
 The following keys are going to be accepted:
 Unaccepted Keys:
 172.16.11.211
 Key for minion 172.16.11.211 accepted.

salt-key -L                               
 Accepted Keys:
 172.16.11.211
 Denied Keys:
 Unaccepted Keys:
 Rejected Keys:
```

更多的证书管理通过`salt-key  -h`查看。

---
## 配置SaltStack

### Master端
master端的配置文件是`/etc/salt/master`，其中的配置选项较多，在日常使用中，需要经常修改Master的配置文件。SaltStack的大部分配置都可以保持默认，只需根据自己的实际需求更改配置即可。其中下面几个在平时使用过程中，会经常能改。

- max_open_files ：     根据Master将Minin数量进行适当的调整
- timeout  ： 可以根据Master 和Minion的网络状况调整
- auto_accept和autosign_file： 在大规模部署Minion的时候可以设置为自动签证
- master_tops和所有以external开头的参数： 这些参数是SaltStack与外部系统进行整合的相关配置参数

详细配置信息可以参考：http://arlen.blog.51cto.com/7175583/1423997

### Minion
master端的配置文件是`/etc/salt/minion`，大部分情况保持默认即可
详细配置信息可以参考：http://arlen.blog.51cto.com/7175583/1424008

---
## SaltStack常用命令操作

#### Master端

- salt              // salt master核心操作命令

```shell
salt [options] '<target>' <function> [arguments]
salt '*' test.ping
```

- salt-cp         // 文件传输命令 ，不支持目录分发

```
salt-cp [options] '<target>' SOURCE DEST
salt-cp '*' test.txt /root/
```

- salt-key       // 证书管理

```
salt-key [options]
salt-key -L          
```

- salt-master  // 服务命令

```
salt-master [options]
salt-master -d         //后台运行master
```

- salt-run       // 执行 runner

```
salt-run [options] [runner.func]
salt-run manage.status
```

- salt-unity

### Minion端

- salt-call   //  拉取命令

```
salt-call [options] <function> [arguments]
salt-call test.ping           //自己执行test.ping命令
```

- salt-minion  // 服务命令

```
salt-minion [options]
salt-minion -d         //后台运行
```

---
## SaltStack常用模块

Saltstack通过模块来实现管理，具备丰富的模块功能，命令形式也较为自由。

- sys.doc：类似Linux的man命令，可以显示minion支持的模块的详细操作说明

```
salt '*' sys.doc status.all_status        //查询status.all_status模块函数的使用方法                                                                     
'status.all_status:'
    Return a composite of all status data and info for this minion.
    Warning: There is a LOT here!
    CLI Example:
        salt '*' status.all_status
```
- status ：status模块是系统状态的常用信息模块，可以利用status模块查看系统信息

```
salt '172.16.11.211' status.loadavg   // 查询负载信息，还有status.[cpuinfo,diskstats,meminfo,w]
172.16.11.211:
    ----------
    1-min:
        0.05
    15-min:
        0.05
    5-min:
        0.07
```

- test：  更多使用方法使用访问官方网站或者`salt '*' sys.doc test`

```
salt '172.16.11.211'  test.ping
172.16.11.211:
    True
```

- state：是salt state的管理模块，可以通过state模块简单的对minin操作sls状态

```
salt '172.16.11.211' state.highstate //更新指定minons的所有sls状态
salt '172.16.11.211' state.running //查看当前运行的sls状态\
salt '172.16.11.211' state.single pkg.installed name=vim //动态指定一个sls状态
```

- saltutil ： SaltStack的一些辅助操作命令模块

```
salt '*' saltutil.is_running state.highstate     //判断一个函数是否正在使用
salt '*' saltutil.kill_job <job id>              // 强制关闭一个job进程
```
