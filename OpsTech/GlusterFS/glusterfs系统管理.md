## glusterfs系统部署 ##

### 系统环境介绍 ###

* OS版本：CentOS 6.5 x86_64
* 软件版本： 3.7.3
* 系统节点 

|ip地址|挂载路径|
|---:|:---|
|172.161.8.241|/export/brick1/gv0|
|172.161.8.242|/export/brick1/gv0|
|172.161.8.243|/export/brick1/gv0|
|172.161.8.244|/export/brick1/gv0|

### gluster安装部署 ###

#### 安装GlusterFS软件包 ####

```
// 安装软件包
yum install -y glusterfs glusterfs-fuse glusterfs-server xfsprogs
// 启动服务，添加自启动
/etc/init.d/glusterd start 
chkconfig glusterfsd on
```

#### 添加节点到GlusterFS集群 ####

```
//添加节点到存储池，在其中一个节点上操作
 gluster peer probe 172.16.18.241
peer probe: success: on localhost not needed

 gluster peer probe 172.16.18.242
peer probe: success

gluster peer probe 172.16.18.243
peer probe: success

 gluster peer probe 172.16.18.244
peer probe: success

//查看各个节点状态
gluster peer status
Number of Peers: 3
Hostname: 172.16.18.242
Uuid: beb0aae7-a939-45ec-a273-0c21c2f59546
State: Peer in Cluster (Connected)
Hostname: 172.16.18.243
Uuid: eab486b3-d1a1-4851-b9ec-45aab1ef9a66
State: Peer in Cluster (Connected)
Hostname: 172.16.18.244
Uuid: 3108764d-d6b3-4356-810d-88872d56ceb6
State: Peer in Cluster (Connected)
```

#### 创建数据存放目录 ####

```
parted  /dev/sdb rm 1
mkfs.xfs -i size=512 /dev/sdb -f
mkdir -p /export/brick1
/bin/mount -t xfs /dev/sdb /export/brick1
mkdir /export/brick1/gv0
echo "/dev/sdb        /export/brick1  xfs     defaults        1       2" >> /etc/fstab
```

#### 创建GlusterFS磁盘 ####

```
// 创建系统卷gv0（副本卷）
gluster volume create gv0 replica 2 172.16.18.241:/export/brick1/gv0 172.16.18.242:/export/brick1/gv0 172.16.18.243:/
export/brick1/gv0 172.16.18.244:/export/brick1/gv0 force

//启动系统卷gv0
 gluster volume start gv0
volume create: gv0: success: please start the volume to access data

//查看系统卷信息
gluster volume info
 
Volume Name: gv0
Type: Distributed-Replicate
Volume ID: e64cb61c-0f18-41b5-bf4d-c45ee085ca3b
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.16.18.241:/export/brick1/gv0
Brick2: 172.16.18.242:/export/brick1/gv0
Brick3: 172.16.18.243:/export/brick1/gv0
Brick4: 172.16.18.244:/export/brick1/gv0
Options Reconfigured:
performance.readdir-ahead: on
```

#### 安装客户端并mount GlusterFS文件系统 ####

```
// 下载仓库文件
wget -P /etc/yum.repos.d  http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo

//安装软件
yum install glusterfs glusterfs-fuse glusterfs-server

//创建挂载点
mkdir -p /opt/vmx/gv0

//client挂载
/bin/mount -t glusterfs 172.16.18.241:/gv0 /opt/vmx/gv0
```

## 基本系统管理 ##

### 节点管理 ###
```
gluster peer command
```

#### 节点状态 ####

```
// 在任意节点操作，可以看到其他节点与本节点的连接状态
gluster peer status
Number of Peers: 3
Hostname: 172.16.18.242
Uuid: beb0aae7-a939-45ec-a273-0c21c2f59546
State: Peer in Cluster (Connected)
Hostname: 172.16.18.243
Uuid: eab486b3-d1a1-4851-b9ec-45aab1ef9a66
State: Peer in Cluster (Connected)
Hostname: 172.16.18.244
Uuid: 3108764d-d6b3-4356-810d-88872d56ceb6
State: Peer in Cluster (Connected)
```

####  添加节点 ####

**命令：`gluster peer HostName`**

```
// 将节点server添加到存储池中
gluster peer prober server
```

#### 删除节点 ####

**命令： `gluster peer detach HostName`**

```
// 将节点server从存储池中移除，移除节点时要保证节点上没有brick，需要提前移除brick
gluster peer detch server
```

### 卷管理 ###

#### 创建卷 ####
**命令：gluster volume create NEW-VOLNAME [transport[tcp|rdma|tcp,rdma]] NEW_BRICK...**

- 创建分布式卷(DHT)

```
// DHT卷将数据以哈希计算方式分布到各个brick上，数据是以文件为单位存取，基本达到分布均衡，提供的容量为各个brick的容量总和
gluster volume create dht_vol 172.16.18.{241,242,243,244}:/export/brick1/gv0
```

- 创建副本卷(AFR)

```
// AFR提供数据副本，副本数为replica，即每个文件存储replica份数，文件不分割，以文件为存储单位：副本数需要等于brick数；当brick数是副本的倍数时，则自动变化为Replicated-Distributed卷
gluster volume create afr_vol replica 2 172.16.18.{241,242,243,244}:/export/brick/gv0
```
**每两个brick组成一组，每组两个副本，文件又以DHT分布在三个组上，这样是副本卷和分布式卷的组合**


- 创建条带卷

```
//stripe卷类似raid0，将数据条带化，分布在不同的brick，该方式将文件分块，将文件分成stripe块，分别进行存储，在大文件读取是有优势。stripe需要等于brick数；当brick数等于stripe数的倍数时，则自动变化为stripe-distributed卷。
gluster volume create str_vol stripe 2 172.16.18.{241,242,243,244}:/export/brick1/gv0
```
**每2个brick组成一组，每组2个brick，文件以DHT分布在两个组中，每个组中将文件条带成2块**

- 创建Replicated-Stripe-Distributed卷

```
//使用8个brick创建一个组合卷，即brick数是stripe*replica的倍数，则创建三种基本卷的组合卷，若刚好等于stripe*replica则为stript-Distrubted卷
gluster volume create str_afr_dht_vol stripe 2 replica 2 172.16.18.{241,242,243,244}:/export/brick1/gv0  172.16.18.{241,242,243,244}:/export/brick1/gv1
```

#### 卷信息 ####
**命令：gluster volume info**
```
// 该命令能够查看存储池中当前卷的信息，包括卷方式、包含的brick、卷的当期状态、卷名及UUID等
gluster volume info
 
Volume Name: gv0
Type: Distributed-Replicate
Volume ID: e64cb61c-0f18-41b5-bf4d-c45ee085ca3b
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.16.18.241:/export/brick1/gv0
Brick2: 172.16.18.242:/export/brick1/gv0
Brick3: 172.16.18.243:/export/brick1/gv0
Brick4: 172.16.18.244:/export/brick1/gv0
Options Reconfigured:
performance.readdir-ahead: on
```

#### 卷状态 ####
**命令： gluster volume status**
```
// 该命令能够查看当前卷的状态，包括其中各个brick的状态、NFS的服务状态及当前task执行情况和一些系统设置状态等
gluster volume status
Status of volume: gv0
Gluster process                             TCP Port  RDMA Port  Online  Pid
------------------------------------------------------------------------------
Brick 172.16.18.241:/export/brick1/gv0      49152     0          Y       1970 
Brick 172.16.18.242:/export/brick1/gv0      49152     0          Y       9547 
Brick 172.16.18.243:/export/brick1/gv0      49152     0          Y       1800 
Brick 172.16.18.244:/export/brick1/gv0      49152     0          Y       9741 
NFS Server on localhost                     N/A       N/A        N       N/A  
Self-heal Daemon on localhost               N/A       N/A        Y       2605 
NFS Server on 172.16.18.244                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.244           N/A       N/A        Y       15386
NFS Server on 172.16.18.243                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.243           N/A       N/A        Y       1794 
NFS Server on 172.16.18.242                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.242           N/A       N/A        Y       1966 
 
Task Status of Volume gv0
------------------------------------------------------------------------------
Task                 : Rebalance           
ID                   : fad4f770-87dd-4248-b41e-733641c8bcca
Status               : completed 
```

#### 启动、停止卷 ####
**命令： gluster volume start/stop VOLNAME**
```
// 将创建的卷启动，才能进行客户端挂载；stop能够将系统将停止；此外gluster并未提供restart的重启命令
gluster volume start gv0
volume create: gv0: success: please start the volume to access data
```

#### 删除卷 ####
**命令：gluster volume delete VOLNAME**

```
// 删除卷的操作能够将整个卷删除，操作前需要将卷先停止
gluster volume stop gv0
gluster volume delete gv0
```


### Brick管理 ###

#### 添加brick ####
**命令：gluster volume add-brick VOLNAME NEW-BRICK**
```
//添加两个brick到存储gv0，副本卷则要一次添加的bricks数是replica的整数倍；stripe同样要求
gluster peer probe 172.16.18.245
gluster peer probe 172.16.18.246
gluster volume add-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0
```

#### 移除brick ####
**命令： gluster volume remove-brick VOLNAME BRICK start/status/commit**
```
// 若是副本卷，则要移除的Brick是replica的整数倍，stripe具有同样的要求，副本卷要移除一对Brick，在执行移除操作时，数据会移到其他节点。
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 start

// 在执行移除操作后，可以使用status命令进行task状态查看
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 status

// 使用commit命令执行brick移除，则不会进行数据迁移而直接删除brick，符合不需要数据迁移的用户需求
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 commit
```
**ps：系统的扩容及缩减可以通过如上的节点、brick管理组合达到目的**
**1. 扩容时，可以下增加系统节点，然后添加新增节点上的brick即可**
**2. 缩减时，可以先移除brick，然后在进行节点删除达到缩减的目的，并保证不丢失数据**


#### 替换brick ####
** 命令：gluster volume replace-brick VOLNAME BRICKNEW-BRICK start/pause/sbort/status/commit **

```
// 将172.16.18.244：/export/brick1/gv0替换为172.16.18.245:/export/brick1/gv0。在执行replcase-brick，使用start启动命令之后，开始将原始brick的数据迁移到即将需要替换的brick上
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  start force

//在数据迁移过程中，可以查看替换状态
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  status

// 在数据迁移的过程中，可以执行abort命令终止brick替换
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0 abort

//当数据迁移结束之后，执行commit命令结束任务，则进行brick替换。使用volume info命令可以查看到brick已经被替换
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  start
```

## 系统拓展 ##

### 系统配额 ###

#### 开启、关闭系统配额#### 
```
//在使用系统配额功能时，需要使用enable将其开启；disable为关闭命令
gluster volume quota VOLNAME enable/disable
```
#### 设置目录配额  #####
```
gluster volume quota VOLNAME limit-usage /directory limit-value

//设置gv0卷下quota子目录目录限额为10GB，这个目录是以系统挂载目录为根目录，所以/quota即客户端挂载目录下的子目录
gluster volume quota gv0 limit-usage /quota 10GB
```

#### 配额查看 ####
```
gluster volume quota VOLNAME list
gluster volume quota VOLNAME list /directory_name
//可以使用上面命令查看卷的配额，第一个查看全部配额设置，第二个可以根据目录查看，显示配额大小及当前使用容量，如无使用容量则说明设置的目录有误(不存在)
gluster volume quota gv0 list
```

#### 地域复制(geo-replication) ####
```
gluster volume geo-replication MASTER SLAVE start/status/stop

//地域复制是系统提供的灾备功能，能够将系统的全部数据进行异步的增量备份到另外的磁盘中
gluster volume geo-replication gv0 172.16.18.250:/export/brick/gv0 start

//当开始执行gv0卷的所有内容备份到18.250下的/export/brick/gv0中的task，值得注意的是，这个备份目标不能是系统中的brick 
```

#### I/O信息查看 ####
`profile command`提供了一个接口查看每个卷中的每个brick的io信息
```
// 启动profiling，之后便可以进行io查看
gluster volume profile VOLNAME start

// 查看io信息，可以查看到每个brick的io信息
gluster volume profile VOLNAME info

// 管理profilinig功能
gluster volume profile VOLNAME stop
```

#### top监控 ####
`top command`允许你查看bricks的性能，read、write、file open calls、file read caclls、file write calls、directory open calls、directory read calls。所有的查看都可以设置top数，默认是1000
```
// 查看打开的fd
gluster volume top VOLNAME open [brick BRICK-NAME] [list-cnt cnt]

// 查看调用次数最多的读调用
gluster volume top VOLNAME read [brick BRICK-NAME] [list-cnt cnt]

// 查看调用次数最多的写调用
gluster volume top VOLNAME write [brick BRICK-NAME] [list-cnt cnt]

// 查看次数最多的目录调用
gluster volume top opendir [brick BRICK-NAME] [list-cnt cnt]
gluster volume top readdir [brick BRICK-NAME] [list-cnt cnt]

//查看每个brick的读性能
gluster volume top VOLNAME read-perf [bs blk-size count count] [brick BRICK-NAME] [list-cnt cnt]

//查看每个brick的写性能
gluster volume top VOLNAME write-perf [bs blk-size count count] [brick BRICK-NAME] [list-cnt cnt]
```

---
## [DigitalOcean的VPS，稳定、便宜，用于搭建自己的站点和梯子，现在注册即得10$,免费玩2个月](https://www.digitalocean.com/?refcode=9e4ab85e22ec) ##