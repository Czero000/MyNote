# MFS 概述
MooseFS 是一款具有冗余容错功能的分布式文件系统。它把数据分散在多台服务器上，确保一份数据多个备份副本，对外提供统一的结构。

## 功能特性
对于标准的文件操作，MooseFS 表现与其他类Unix文件系统一致。
支持的通过文件系统特性：

 - 层次结构（目录树）
 - 兼容 POSIX 文件属性
 - 支持特殊文件
 - 符号链接和硬链接
 - 基于 IP 地址和密码的访问控制

## 独有特性

- 高可靠性(数据的多个副本存储在不同服务器)
- 容量动态扩展（添加新硬盘或者服务器）
- 可以回收在制定时间内删除的文件，类似回收站功能
- 可以对整个文件甚至是正在被写入的文件创建文件快照

## MFS整体架构的四种角色

- Master（元数据服务器）
  负责各个数据存储服务器的管理，文件读写调度，文件空间回收以及恢复，多节点拷贝。

- Metalogger（元数据日志服务器）
  负责备份Master服务器的changelog。文件类型为 `changelog.*.mfs`，以便在 Master 出问题时接替其工作

- Chunk（数据存储服务器）
  负责连接 Master，听从 Master 调度，提供存储空间，并为客户端提供数据传输

- Client（客户端挂载）
  通过FUSE内核接口挂载远程管理服务器（master）上所管理的数据存储服务器，使用起来和本地文件系统一样

## MFS工作图解
- 网络架构

![MooseFS-NetWork.png](http://ofc9x1ccn.bkt.clouddn.com/moosefs/moosefs-network.png 'MooseFS-NetWork')

- 工作原理

![moosefs-write-process.png](http://ofc9x1ccn.bkt.clouddn.com/moosefs/moosefs-write-process.png 'MooseFS Write Process')


![moosefs-read-process.png](http://ofc9x1ccn.bkt.clouddn.com/moosefs/moosefs-read-process.png 'MooseFS Read Process')

- 集群拓扑

![mfs-topology.png](http://ofc9x1ccn.bkt.clouddn.com/moosefs/mfs-topology.png 'MooseFS-Topology')

---

# 安装配置 MFS

## 系统环境介绍
- OS：`CentOS Linux release 7.2.1511 (Core)`
- 软件版本：2.0.81-1
- 节点配置

| ip地址          | 角色         |
| ------------- | ---------- |
| 172.16.18.137 | master     |
| 172.16.18.134 | metalogger |
| 172.16.18.183 | chunk      |
| 172.16.18.184 | chunk      |
| 172.16.18.185 | chunk      |
| 172.16.18.186 | chunk      |
| 172.16.18.187 | chunk      |

chunk 上有四块硬盘，第一块为系统，剩下三块作为数据存储，每块容量为4TB

## 软件安装

### 从官方软件库安装MFS

- 添加yum key

```
  curl "http://ppa.moosefs.com/RPM-GPG-KEY-MooseFS" > /etc/pki/rpm-gpg/RPM-GPG-KEY-MooseFS
```


- 下载软件库配置文件

```
//For EL7 family:
curl "http://ppa.moosefs.com/MooseFS-stable-el7.repo" > /etc/yum.repos.d/MooseFS.repo

//For EL6 family:
curl "http://ppa.moosefs.com/MooseFS-stable-el6.repo" > /etc/yum.repos.d/MooseFS.repo

For EL5 family:
Due to GPGv4 incompatibility with CentOS 5, CentOS 5 is deprecated.
If you really need CentOS 5 packages, please contact support@moosefs.com.
```

- 安装软件包

```
// For Master Server:
yum install moosefs-master moosefs-cli moosefs-cgi moosefs-cgiserv

// For Chunkservers:
yum install moosefs-chunkserver

//For Metaloggers:
yum install moosefs-metalogger

For Clients:
//yum install moosefs-client
```
- 启动服务

```
//To start process manually:
mfsmaster start
mfschunkserver start

//For systemd OS family - EL7:
systemctl start moosefs-master.service
systemctl start moosefs-chunkserver.service

//For SysV OS family - EL6:
service moosefs-master start
service moosefs-chunkserver start
```

---

### 从源码安装MFS

- 下载软件包

```
wget http://ppa.moosefs.com/src/moosefs-2.0.88-1.tar.gz
```

- 添加用户和组

```
useradd -s /sbin/nologin  -M mfs
```

- 安装软件包

```
tar-zxf moosefs-2.0.88-1.tar.gz
cd moosefs-2.0.88

// For master
./configure --prefix=/usr/local/mfs --with-default-user=mfs --with-default-group=mfs --disable-mfschunkserver --disable-mfsmount

// For metalogger
./configure --prefix=/usr/local/mfs --with-default-user=mfs --with-default-group=mfs --disable-mfschunkserver --disable-mfsmount

// For chunk
./configure --prefix=/usr/local/mfs --with-default-user=mfs --with-default-group=mfs --disable-mfsmaster --disable-mfsmount --disable-mfscgi --disable-mfscgiserv
```

- 安装MFS client

client安装需要 fuse 支持，fuse 可以从源码和仓库中安装

```
./configure --prefix=/usr/local/mfs --with-default-user=mfs --with-default-group=mfs --disable-mfsmaster --disable-mfschunkserver --disable-mfscgi --disable-mfscgiserv
```

## 配置MFS

### Master

- 配置文件

```
// mfsmaster.cfg
# WORKING_USER = mfs 运行 master server 的用户
# WORKING_GROUP = mfs 运行 master server 的组
# SYSLOG_IDENT = mfsmaster master server 在 syslog中的标识，说明是由 master serve 产生的
# LOCK_MEMORY = 0 是否执行 mlockall()以避免 mfsmaster 进程溢出（默认为 0）
# NICE_LEVEL = -19 运行的优先级(如果可以默认是 -19; 注意: 进程必须是用 root启动)

# EXPORTS_FILENAME = /usr/local/mfs/etc/mfsexports.cfg 被挂接目录及其权限控制文件的存放位置

# TOPOLOGY_FILENAME = /usr/local/mfs/etc/mfs/mfstopology.cfg

# DATA_PATH = /usr/local/mfs/var/mfs 数据存放路径，此目录下大致有三类文件，changelog，sessions和 stats；

# BACK_LOGS = 50 metadata 的改变 log 文件数目(默认是 50);
# BACK_META_KEEP_PREVIOUS = 1

# REPLICATIONS_DELAY_INIT = 300 延迟复制的时间（默认是 300s）;
# REPLICATIONS_DELAY_DISCONNECT = 3600 chunkserver 断开的复制延迟（默认是 3600）；

# MATOML_LISTEN_HOST = * metalogger 监听的 IP 地址(默认是*，代表任何 IP)；
# MATOML_LISTEN_PORT = 9419 metalogger 监听的端口地址(默认是 9419)；
# MATOML_LOG_PRESERVE_SECONDS = 600

# MATOCS_LISTEN_HOST = * 用于 chunkserver 连接的 IP 地址（默认是*，代表任何 IP）；
# MATOCS_LISTEN_PORT = 9420 用于 chunkserver 连接的端口地址（默认是 9420）；

# MATOCU_LISTEN_HOST = * 用于客户端挂接连接的 IP 地址(默认是*，代表任何 IP)；
# MATOCU_LISTEN_PORT = 9421 用于客户端挂接连接的端口地址（默认是 9421）；

# CHUNKS_LOOP_MAX_CPS = 100000
# CHUNKS_LOOP_MIN_TIME = 300 chunks 的回环频率（默认是：300 秒）；
注：原文为Chunks loop frequency in seconds (default is 300)

# CHUNKS_SOFT_DEL_LIMIT = 10
# CHUNKS_HARD_DEL_LIMIT = 25
# CHUNKS_WRITE_REP_LIMIT = 2
# CHUNKS_READ_REP_LIMIT = 10
# ACCEPTABLE_DIFFERENCE = 0.1

# SESSION_SUSTAIN_TIME = 86400
# REJECT_OLD_CLIENTS = 0 弹出低于 1.6.0 的客户端挂接（0 或 1，默认是 0）注意mfsexports 访问控制对于那些老客户是没用的
# deprecated:
# CHUNKS_DEL_LIMIT - use CHUNKS_SOFT_DEL_LIMIT instead
# LOCK_FILE - lock system has been changed, and this option is used only to search for old lockfile


\\ mfsexport.cfg
#* / ro
#192.168.1.0/24 / rw
#192.168.1.0/24 / rw,alldirs,maproot=0,password=passcode
#10.0.0.0-10.0.0.5 /test rw,maproot=nobody,password=test
* . rw
#* / rw,alldirs,maproot=0
172.16.18.221          .               rw                             \\ 回收站
172.16.18.221          /               rw,alldirs,maproot=0
172.16.18.134          /               rw,alldirs,maproot=0
```

- 修改配置文件

```
cd /usr/local/mfs/etc/
mv mfsmaster.cfg.dist mfsmaster.cfg
mv mfsexports.cfg.dist mfsexports.cfg
```

mfsmaster.cfg : master的主配置文件，配置文件中所有的选项都是用#注释掉的，这代表的是将会使用的选项的默认参数，如果要修改只需取消注释修改其值为你所要使用的值即可；

mfsexportes.cfg 为共享mfs文件系统的控制文件，NFS要共享一个目录时，我们会使用vim /etc/exports命令，编写共享给谁，所要共享的目录，共享出去的属性这些内容，而mfsexports.cfg的作用与其类似其书写格式如下：

```
client		Directory			Property
*                /       	rw,alldirs,maproot=0
client支持格式：ip、ip/netmask、ip/位数掩码、ip-ip、*
```

该文件每一个条目分为三部分：
第一部分：客户端的ip 地址
第二部分：被挂接的目录
第三部分：客户端拥有的权限
```
//地址可以指定的几种表现形式：
* 所有的ip 地址
n.n.n.n 单个ip 地址
n.n.n.n/b IP 网络地址/位数掩码
n.n.n.n/m.m.m.m IP 网络地址/子网掩码
f.f.f.f-t.t.t.t IP 段

//目录部分需要注意两点：
/ 标识MooseFS 根;
. 表示MFSMETA 文件系统

//权限部分：
ro 只读模式共享
rw 读写的方式共享
alldirs 许挂载任何指定的子目录
```

- 启动服务

```
/usr/local/mfs/sbin/mfsmaster start

//为了监控moosefs的当前运行状态，我们可以运行cgi服务，这样就可以用浏览器查看整个moosefs的运行情况
/usr/local/mfs/sbin/mfscgiserv
```

### Metalogger

- 修改配置文件

```
mv mfsmetalogger.cfg.dist mfsmetalogger.cfg

META_DOWNLOAD_FREQ = 24 \\元数据备份下载请求频率，设置为1小时
MASTER_HOST = 172.16.18.137 \\修改MASTER_HOST的值，为MASTER_HOST的ip地址
```

- 启动服务

```
/usr/local/mfs/sbin/mfsmetalogger start
```

### ChunkServer

- 配置分区

```
parted -s /dev/sdb 'mklabel gpt';parted -s /dev/sdc 'mklabel gpt';parted -s /dev/sdd 'mklabel gpt'
parted -s /dev/sdb  'mkpart primary 0 -1'; parted -s /dev/sdc  'mkpart primary 0 -1'; parted -s /dev/sdd 'mkpart primary 0 -1'
mkfs.ext4 -q -T largefile /dev/sdb1;mkfs.ext4 -q -T largefile /dev/sdc1;mkfs.ext4 -q -T largefile /dev/sdd1
mkdir /MFS_data{1,2,3}  
mount /dev/sdb1 /MFS_data1; mount /dev/sdc1 /MFS_data2; mount /dev/sdd1 /MFS_data3
chown mfs:mfs /MFS_data*
```

- 修改配置文件

```
mv mfschunkserver.cfg.dist mfschunkserver.cfg
修改MASTER_HOST的值，为MASTER_HOST的ip地址：
MASTER_HOST = 172.16.18.137

mv mfshdd.cfg.dist mfshdd.cfg
增加挂载目录信息
/MFS_data1
/MFS_data2
/MFS_data3
```

- 启动服务

```
/usr/local/mfs/sbin/mfschunkserver start
```

### Client

- 挂载 MFS

```
mkdir /MFS_data
/usr/local/mfs/bin/mfsmount /MFS_data -H 172.16.18.137
mfsmaster accepted connection with parameters: read-write,restricted_ip ; root mapped to root:root
```

特别需要注意的是，所有的MFS 都是挂接同一个元数据服务器 master 的 IP ,而不是其他数据存储
服务器 chunkserver 的 IP

---

# 使用MFS

## MFS文件系统使用

Client通过MFS软件提供的工具来管理MFS文件系统，下面是工具介绍

```
/usr/local/mfs/bin/mfstools -h
mfs multi tool

usage:
        mfstools create - create symlinks (mfs<toolname> -> /usr/local/mfs/bin/mfstools)

tools:
        mfsgetgoal                               // 设定副本数
        mfssetgoal                               // 获取副本数
        mfsgettrashtime                          // 设定回收站时间
        mfssettrashtime                          // 设定回收站时间
        mfscheckfile                             // 检查文件
        mfsfileinfo                              // 文件信息
        mfsappendchunks                            
        mfsdirinfo                                // 目录信息
        mfsfilerepair                             // 文件修复
        mfsmakesnapshot                           // 快照     
        mfsgeteattr                               // 设置权限
        mfsseteattr
        mfsdeleattr

deprecated tools:                                  // 递归设置
        mfsrgetgoal = mfsgetgoal -r
        mfsrsetgoal = mfssetgoal -r
        mfsrgettrashtime = mfsgettreshtime -r
        mfsrsettrashtime = mfssettreshtime -r
```

### 挂载文件系统

MooseFS 文件系统利用下面的命令：

```
mfsmount mountpoint [-d][-f] [-s][-m] [-n][-p] [-HMASTER][-PPORT] [-S PATH][-o OPT[,OPT...]]
-H MASTER：是管理服务器（master server）的ip 地址
-P PORT： 是管理服务器（ master server）的端口号，要按照mfsmaster.cfg 配置文件中的变量
MATOCU_LISTEN_POR 的之填写。如果master serve 使用的是默认端口号则不用指出。
-S PATH：指出被挂接mfs 目录的子目录，默认是/目录，就是挂载整个mfs 目录。
```

Mountpoint：是指先前创建的用来挂接 mfs 的目录。
在开始 mfsmount 进程时，用一个`-m` 或`-o mfsmeta` 的选项，这样可以挂接一个辅助的文件系统 MFSMETA，这么做的目的是对于意外的从 MooseFS 卷上删除文件或者是为了释放磁盘空间而移动的文件而又此文件又过去了垃圾文件存放期的恢复，例如

```
/usr/local/mfs/bin/mfsmount -m /MFS_meta/ -H 172.16.18.137
```

### 设定副本数量

目标（goal），是指文件被拷贝副本的份数，设定了拷贝的份数后是可以通过mfsgetgoal 命令来证实的，也可以通过mfsrsetgoal 来改变设定。

```
mfssetgoal 3 /MFS_data/test/
mfssetgoal 3 /MFS_data/test/
```

用`mfsgetgoal -r` 和`mfssetgoal -r` 同样的操作可以对整个树形目录递归操作，其等效于`mfsrsetgoal`命令。实际的拷贝份数可以通过`mfscheckfile` 和`mfsfile info`命令来证实。

**注意以下几种特殊情况：**

- 一个不包含数据的零长度的文件,尽管没有设置为非零的目标（the non-zero "goal"）,但用mfscheckfile 命令查询将返回一个空的结果；将文件填充内容后，其会根据设置的goal创建副本；这时再将文件清空，其副本依然作为空文件存在。
- 假如改变一个已经存在的文件的拷贝个数，那么文件的拷贝份数将会被扩大或者被删除，这个过程会有延时。可以通过mfscheckfile 命令来证实。
- 对一个目录设定“目标”，此目录下的新创建文件和子目录均会继承此目录的设定，但不会改变已经存在的文件及目录的拷贝份数。

可以通过mfsdirinfo来查看整个目录树的信息摘要。


### 垃圾回收站

一个被删除文件能够存放在一个 "垃圾箱" 的时间就是一个隔离时间， 这个时间可以用`mfsgettrashtime` 命令来验证，也可以使用`mfssettrashtime 命令来设置`。

```
mfssettrashtime 64800 /MFS_data/test/test1
mfsgettrashtime /MFS_data/test/test1
```

时间的单位是秒(有用的值有:1 小时是3600 秒,24 - 86400 秒,1天 - 604800 秒)。就像文件被存储的份数一样, 为一个目录设定存放时间是要被新创建的文件和目录所继承的。数字0 意味着一个文件被删除后, 将立即被彻底删除，在想回收是不可能的。

删除文件可以通过一个单独安装MFSMETA 文件系统。特别是它包含目录/ trash (包含任然可以被还原的被删除文件的信息)和/ trash/undel (用于获取文件)。只有管理员有权限访问MFSMETA(用户的uid 0，通常是root)。

```
/usr/local/mfs/bin/mfsmount -m /MFS_meta/ -H 172.16.18.137
```

被删文件的文件名在“垃圾箱”目录里还可见,文件名由一个八位十六进制的数 i-node 和被删文件的文件名组成，在文件名和 i-node 之间不是用“/”,而是用了“|”替代。如果一个文件名的长度超过操作系统的限制（通常是255 个字符），那么部分将被删除。通过从挂载点起全路径的文件名被删除的文件任然可以被读写。

移动这个文件到 trash/undel 子目录下，将会使原始的文件恢复到正确的 MooseFS 文件系统上路径下（如果路径没有改变）。如果在同一路径下有个新的同名文件，那么恢复不会成功。

从“垃圾箱”中删除文件结果是释放之前被它站用的空间(删除有延迟,数据被异步删除)。

在MFSMETA中还有另一个目录reserved，该目录内的是被删除但依然打开的文件。在用户关闭了这些被打开的文件后，reserved 目录中的文件将被删除，文件的数据也将被立即删除。在reserved 目录中文件的命名方法同trash 目录中的一样，但是不能有其他功能的操作。

### 快照snapshot
MooseFS 系统的另一个特征是利用 mfsmakesnapshot 工具给文件或者是目录树做快照
```
mfsmakesnapshot source ... destination
```
Mfsmakesnapshot 是在一次执行中整合了一个或是一组文件的拷贝，而且任何修改这些文件的源文件都不会影响到源文件的快照， 就是说任何对源文件的操作,例如写入源文件，将不会修改副本(或反之亦然)。
也可以使用mfsappendchunks：
```
mfsappendchunks destination-file source-file ...
```
当有多个源文件时，它们的快照被加入到同一个目标文件中（每个chunk 的最大量是 chunk）。



## MFS集群维护

### 启动MFS集群

安全的启动MooseFS 集群（避免任何读或写的错误数据或类似的问题）的方式是按照以下命令步骤：

1. 启动mfsmaster 进程
2. 启动所有的mfschunkserver 进程
3. 启动mfsmetalogger 进程（如果配置了mfsmetalogger）
4. 当所有的chunkservers 连接到MooseFS master 后，任何数目的客户端可以利用mfsmount 去挂接被export 的文件系统。（可以通过检查master 的日志或是CGI 监视器来查看是否所有的chunkserver被连接）。

### 停止MFS集群

安全的停止MooseFS 集群：

1. 在所有的客户端卸载MooseFS 文件系统（用umount 命令或者是其它等效的命令）
2. 用mfschunkserver stop 命令停止chunkserver 进程
3. 用mfsmetalogger stop 命令停止metalogger 进程
4. 用mfsmaster stop 命令停止master 进程

### Chunkservers 的维护

若每个文件的goal（目标）都不小于2，并且没有under-goal 文件（这些可以用mfsgetgoal –r和mfsdirinfo 命令来检查），那么一个单一的chunkserver 在任何时刻都可能做停止或者是重新启动。以后每当需要做停止或者是重新启动另一个chunkserver 的时候，要确定之前的chunkserver 被连接，而且要没有under-goal chunks。

### MFS元数据备份

通常元数据有两部分的数据：

- 主要元数据文件metadata.mfs，当mfsmaster 运行的时候会被命名为 metadata.mfs.back
- 元数据改变日志changelog.`*.mfs`，存储了过去的N 小时的文件改变（N 的数值是由BACK_LOGS参数设置的，参数的设置在mfschunkserver.cfg 配置文件中）。

主要的元数据文件需要定期备份，备份的频率取决于取决于多少小时changelogs 储存。元数据changelogs 实时的自动复制。1.6版本中这个工作都由metalogger完成。

### MFS Master的恢复

一旦mfsmaster 崩溃（例如因为主机或电源失败），需要最后一个元数据日志changelog 并入主要的metadata 中。这个操作时通过`mfsmetarestore`工具做的，最简单的方法是：

```
mfsmetarestore -a
```

如果master 数据被存储在MooseFS 编译指定地点外的路径，则要利用-d 参数指定使用，如：

```
mfsmetarestore -a -d /opt/mfsmaster
```

### 从 MetaLogger 中恢复 Master

如果 `mfsmetarestore -a` 无法修复，则使用 metalogger 也可能无法修复，暂时没遇到过这种情况，这里不暂不考虑。

1. 找回 metadata.mfs.back 文件，可以从备份中找，也可以中 metalogger 主机中找（如果启动了 metalogger 服务），然后把 metadata.mfs.back 放入 data 目录，一般为`{prefix}/var/mfs`
2. 从在 master 宕掉之前的任何运行 metalogger 服务的服务器上拷贝最后 metadata 文件，然后放入 mfsmaster 的数据目录。
3. 利用 mfsmetarestore 命令合并元数据 changelogs，可以用自动恢复模式`mfsmetarestore -a`，也可以利用非自动化恢复模式

```
mfsmetarestore -m metadata.mfs.back -o metadata.mfs changelog_ml.*.mfs

```

或：强制使用 metadata.mfs.back 创建 metadata.mfs，可以启动 master，但丢失的数据暂无法确定。



### Automated Failover

生产环境使用 MooseFS 时，需要保证 master 节点的高可用。 使用 `ucarp` 是一种比较成熟的方案，或者DRBD+[hearbeat|keepalived]。`ucarp` 类似于 `keepalived`，通过主备服务器间的健康检查来发现集群状态，并执行相应操作。另外 MooseFS商业版本已经支持双主配置，解决单点故障。
