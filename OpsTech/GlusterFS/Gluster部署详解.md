本文详细介绍gluster fs 安装配置及之后的维护

### 环境介绍
系统版本:CentOS 6.5 x86_64

###  安装GlusterFS软件包
```
yum install -y glusterfs glusterfs-fuse glusterfs-server xfsprogs
/etc/init.d/glusterd start
chkconfig glusterfsd on
```
### 配置整个GlusterFS集群
```
gluster peer probe 172.16.18.241
peer probe: success: on localhost not needed

 gluster peer probe 172.16.18.242
peer probe: success

gluster peer probe 172.16.18.243
peer probe: success

 gluster peer probe 172.16.18.244
peer probe: success

 gluster peer status
gluster peer status
Number of Peers: 3
Hostname: 172.16.18.242
Uuid: beb0aae7-a939-45ec-a273-0c21c2f59546
State: Peer in Cluster (Connected)
Hostname: 172.16.18.243
Uuid: eab486b3-d1a1-4851-b9ec-45aab1ef9a66
State: Peer in Cluster (Connected)
Hostname: 172.16.18.244
Uuid: 3108764d-d6b3-4356-810d-88872d56ceb6
State: Peer in Cluster (Connected)
```

### 创建数据存放目录
```
parted  /dev/sdb rm 1
mkfs.xfs -i size=512 /dev/sdb -f
mkdir -p /export/brick1
/bin/mount -t xfs /dev/sdb /export/brick1
mkdir /export/brick1/gv0
```

### GlusterFS磁盘
```
gluster volume create gv0 replica 2 172.16.18.241:/export/brick1/gv0 172.16.18.242:/export/brick1/gv0 172.16.18.243:/
export/brick1/gv0 172.16.18.244:/export/brick1/gv0 force

gluster volume start gv0
volume create: gv0: success: please start the volume to access data

gluster volume info
 Volume Name: gv0
Type: Distributed-Replicate
Volume ID: e64cb61c-0f18-41b5-bf4d-c45ee085ca3b
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.16.18.241:/export/brick1/gv0
Brick2: 172.16.18.242:/export/brick1/gv0
Brick3: 172.16.18.243:/export/brick1/gv0
Brick4: 172.16.18.244:/export/brick1/gv0
Options Reconfigured:
performance.readdir-ahead: on
```

### 安装客户端并mount GlusterFS文件系统
```
wget -P /etc/yum.repos.d  http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo

yum install glusterfs glusterfs-fuse glusterfs-server
mkdir -p /opt/vmx/gv0
/bin/mount -t glusterfs 172.16.18.241:/gv0 /opt/vmx/gv0
df -h
Filesystem               Size  Used Avail Use% Mounted on
/dev/mapper/centos-root   50G  5.6G   45G  12% /
devtmpfs                  12G     0   12G   0% /dev
tmpfs                     12G   12K   12G   1% /dev/shm
tmpfs                     12G   25M   12G   1% /run
tmpfs                     12G     0   12G   0% /sys/fs/cgroup
/dev/mapper/centos-home  217G   33M  217G   1% /home
/dev/sda1                497M  102M  395M  21% /boot
/dev/sdb                 280G   33M  280G   1% /export/brick1
172.16.6.60:/gv0         559G  1.6G  558G   1% /opt/vmx/gv0
```

### 读写可用性测试

*在挂载点上写入数据：*
```
echo "172.16.18.245" > /opt/vmx/gv0/test.txt
mkdir /opt/vmx/gv0/test
```

*在server数据目录中进行查看*
```
ls /export/brick1/gv0/
test  test.txt
```
*结果： 数据写入成功*

### 扩容与缩减

扩容步骤：系统的扩容与缩减可以通过节点、brick管理达到目的
* 扩容时，可以先增加系统节点，然后添加新的Brick即可
* 缩减时，先移除Brick，然后在进行删除达到缩容目的，并保持数据不丢失

在线扩容

*查看节点状态*
```
gluster peer status
Number of Peers: 3
Hostname: 172.16.18.242
Uuid: 5f4f3352-6b28-471f-8c1e-a990b49f77c2
State: Peer in Cluster (Connected)
Hostname: 172.16.18.243
Uuid: 3a7e17b5-4407-4ff0-8645-69cc6ace54f9
State: Peer in Cluster (Connected)
Hostname: 172.16.18.241
Uuid: e19a56c0-a060-4bcc-80d8-99de3d85a484
State: Peer in Cluster (Connected)
```

*增加节点*
```
gluster peer probe 172.16.18.245
peer probe: success.
gluster peer probe 172.16.18.246
peer probe: success.
```

*验证节点添加*
```
gluster peer status
Number of Peers: 5
Hostname: 172.16.18.242
Uuid: 5f4f3352-6b28-471f-8c1e-a990b49f77c2
State: Peer in Cluster (Connected)
Hostname: 172.16.18.243
Uuid: 3a7e17b5-4407-4ff0-8645-69cc6ace54f9
State: Peer in Cluster (Connected)
Hostname: 172.16.18.241
Uuid: e19a56c0-a060-4bcc-80d8-99de3d85a484
State: Peer in Cluster (Connected)
Hostname: 172.16.18.245
Uuid: ce286cd4-6ca2-48cb-8207-d58a99ff37dc
State: Peer in Cluster (Connected)
Hostname: 172.16.18.246
Uuid: d4ecc341-7b45-4374-90a5-2f53449c8c86
State: Peer in Cluster (Connected)
```

*查看卷信息*
```
gluster volume info

Volume Name: gv0
Type: Distributed-Replicate
Volume ID: 8377a30e-6f6e-4dfc-9378-f56c1b3559e1
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.16.18.241:/export/brick1/gv0
Brick2: 172.16.18.242:/export/brick1/gv0
Brick3: 172.16.18.243:/export/brick1/gv0
Brick4: 172.16.18.244:/export/brick1/gv0
Options Reconfigured:
diagnostics.count-fop-hits: on
diagnostics.latency-measurement: on
performance.readdir-ahead: on
```

*添加brick*
```
 gluster volume add-brick gv0 172.16.18.245:/export/brick1/gv0 172.16.18.246:/export/brick1/gv0  
volume add-brick: success
```

*验证Brick添加*
```
gluster volume info  

Volume Name: gv0
Type: Distributed-Replicate
Volume ID: 8377a30e-6f6e-4dfc-9378-f56c1b3559e1
Status: Started
Number of Bricks: 3 x 2 = 6
Transport-type: tcp
Bricks:
Brick1: 172.16.18.241:/export/brick1/gv0
Brick2: 172.16.18.242:/export/brick1/gv0
Brick3: 172.16.18.243:/export/brick1/gv0
Brick4: 172.16.18.244:/export/brick1/gv0
Brick5: 172.16.18.245:/export/brick1/gv0
Brick6: 172.16.18.246:/export/brick1/gv0
Options Reconfigured:
diagnostics.count-fop-hits: on
diagnostics.latency-measurement: on
performance.readdir-ahead: on
```

*重新分配数据*
```
gluster volume rebalance gv0 start
volume rebalance: gv0: success: Rebalance on gv0 has been started successfully. Use rebalance status command to check status of the rebalance process.
ID: 0d7c4099-cde7-4a37-9d3e-2a9ae83e6843
gluster volume rebalance gv0 status
                                    Node Rebalanced-files          size       scanned      failures       skipped               status   run time in secs
                               ---------      -----------   -----------   -----------   -----------   -----------         ------------     --------------
                               localhost                0        0Bytes             0             0             0            completed               0.00
                           172.16.18.242                0        0Bytes             0             0             0            completed               0.00
                           172.16.18.243                0        0Bytes             4             0             0            completed               0.00
                           172.16.18.241                0        0Bytes             4             0             1            completed               0.00
                           172.16.18.245                0        0Bytes             1             0             0            completed               0.00
                           172.16.18.246                0        0Bytes             0             0             0            completed               0.00
volume rebalance: gv0: success:
```

在线缩减

*移除Brick*
若是副本卷，则要溢出的Brick是replica的整数倍，stripe具有同样的要求，一次副本卷要移除一对Brick，数据会移到其他节点。
```
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 start
volume remove-brick start: success
ID: b3600ab0-b103-405a-8458-4edb820c0ca1
 gluster volume status
Status of volume: gv0
Gluster process                             TCP Port  RDMA Port  Online  Pid
------------------------------------------------------------------------------
Brick 172.16.18.241:/export/brick1/gv0      49152     0          Y       1970
Brick 172.16.18.242:/export/brick1/gv0      49152     0          Y       9547
Brick 172.16.18.243:/export/brick1/gv0      49152     0          Y       9558
Brick 172.16.18.244:/export/brick1/gv0      49152     0          Y       9741
Brick 172.16.18.245:/export/brick1/gv0      49152     0          Y       13266
Brick 172.16.18.246:/export/brick1/gv0      49152     0          Y       12484
NFS Server on localhost                     N/A       N/A        N       N/A  
Self-heal Daemon on localhost               N/A       N/A        Y       15073
NFS Server on 172.16.18.243                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.243           N/A       N/A        Y       13755
NFS Server on 172.16.18.242                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.242           N/A       N/A        Y       1424
NFS Server on 172.16.18.241                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.241           N/A       N/A        Y       2124
NFS Server on 172.16.18.246                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.246           N/A       N/A        Y       12511
NFS Server on 172.16.18.245                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.245           N/A       N/A        Y       13293

Task Status of Volume gv0
------------------------------------------------------------------------------
Task                 : Remove brick        
ID                   : b3600ab0-b103-405a-8458-4edb820c0ca1
Removed bricks:     
172.16.18.245:/export/brick1/gv0
172.16.18.246:/export/brick1/gv0
Status               : completed
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0  status
                                    Node Rebalanced-files          size       scanned      failures       skipped               status   run time in secs
                               ---------      -----------   -----------   -----------   -----------   -----------         ------------     --------------
                           172.16.18.245                1       42Bytes             1             0             0            completed               1.00
                           172.16.18.246                0        0Bytes             0             0             0            completed               0.00

gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 commit
Removing brick(s) can result in data loss. Do you want to Continue? (y/n) y
volume remove-brick commit: success
Check the removed bricks to ensure all files are migrated.
If files with data are found on the brick path, copy them via a gluster mount point before re-purposing the removed brick.
```

*移除节点*
```
gluster peer detach 172.16.18.245
peer detach: success
gluster peer detach 172.16.18.246
peer detach: success
 gluster volume status            
Status of volume: gv0
Gluster process                             TCP Port  RDMA Port  Online  Pid
------------------------------------------------------------------------------
Brick 172.16.18.241:/export/brick1/gv0      49152     0          Y       1970
Brick 172.16.18.242:/export/brick1/gv0      49152     0          Y       9547
Brick 172.16.18.243:/export/brick1/gv0      49152     0          Y       9558
Brick 172.16.18.244:/export/brick1/gv0      49152     0          Y       9741
NFS Server on localhost                     N/A       N/A        N       N/A  
Self-heal Daemon on localhost               N/A       N/A        Y       15386
NFS Server on 172.16.18.241                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.241           N/A       N/A        Y       2605
NFS Server on 172.16.18.242                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.242           N/A       N/A        Y       1966
NFS Server on 172.16.18.243                 N/A       N/A        N       N/A  
Self-heal Daemon on 172.16.18.243           N/A       N/A        Y       14272

Task Status of Volume gv0
------------------------------------------------------------------------------
There are no active volume tasks
```

替换某个Brick

*增加一个节点*
```
gluster peer probe 172.16.18.245
peer probe: success.
```

*将172.16.18.244：/export/brick1/gv0替换为172.16.18.245:/export/brick1/gv0*

```
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  start force
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0 commit
```


### 其它操作笔记

*删除GlusterFS卷*
```
# gluster volume stop gv0
# gluster volume delete gv0
```

*ACL访问控制*
```
# gluster volume set gv0 auth.allow 172.16.18.*,192.168.1.*
```

*添加GlusterFS节点及brick*
```
# gluster peer probe 172.16.18.245
# gluster peer probe 172.16.18.246
# gluster volume add-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0
```

*删除GlusterFS节点*
```
gluster peer detach 172.16.18.242
```

*删除GlusterFS brick*
```
# gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0

```

*数据重新分配*
```
gluster volume rebalance gv0 start
gluster volume rebalance gv0 status
gluster volume rebalance gv0 stop
```

性能监控

*profile*
```
gluster volume profile mamm-vol start    
gluster volume profile info   
gluster volume profile mamm-vol stop  
```

*top*
```
gluster volume top mamm-vol {open|read|write|opendir|readdir} brick node1:/exp1 list-cnt 1  
```

*显示当前某个brick或NFS路径读文件或写文件数据的性能*
```
gluster volume top mamm-vol read-perf|write-perf bs 256 count 10 brick node1:/exp1 list-cnt 1  
```

*内部计数导出*
```
gluster volume statedump mamm-vol  
```

*迁移GlusterFS磁盘数据*
```
# gluster volume remove-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.242:/export/brick1/gv0  start
# gluster volume remove-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.242:/export/brick1/gv0 pause
# gluster volume remove-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.242:/export/brick1/gv0 status
# gluster volume remove-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.242:/export/brick1/gv0 commit
# gluster volume remove-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.242:/export/brick1/gv0 abort
```

*修复GlusterFS磁盘数据（例如172.16.18.241宕机的情况下）*
```
# gluster volume replace-brick gv0 172.16.18.241:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 commit -force
# gluster volume heal gv0
# gluster volume heal gv0 full
# gluster volume heal gv0 info
```

### GlusterFS常用中继介绍
* storage/posix   #指定一个本地目录给GlusterFS内的一个卷使用；
* protocol/server   #服务器中继，表示此节点在GlusterFS中为服务器模式，可以说明其IP、守护端口、访问权限；
* protocol/client   #客户端中继，用于客户端连接服务器时使用，需要指明服务器IP和定义好的卷；
* cluster/replicate   #复制中继，备份文件时使用，若某子卷掉了，系统仍能正常工作，子卷起来后自动更新（通过客户端）；
* cluster/distribute   #分布式中继，可以把两个卷或子卷组成一个大卷，实现多存储空间的聚合；
* features/locks    #锁中继，只能用于服务器端的posix中继之上，表示给这个卷提供加锁(fcntl locking)的功能；
* performance/read-ahead     #预读中继，属于性能调整中继的一种，用预读的方式提高读取的性能，有利于应用频繁持续性的访问文件，当应用完成当前数据块读取的时候，下一个数据块就已经准备好了，主要是在IB-verbs或10G的以太网上使用；
* performance/write-behind   #回写中继，属于性能调整中继的一种，作用是在写数据时，先写入缓存内，再写入硬盘，以提高写入的性能，适合用于服务器端；
* performance/io-threads   #IO线程中继，属于性能调整中继的一种，由于glusterfs 服务是单线程的，使用IO 线程转换器可以较大的提高性能，这个转换器最好是被用于服务器端；
* erformance/io-cache   #IO缓存中继，属于性能调整中继的一种，作用是缓存住已经被读过的数据，以提高IO 性能，当IO 缓存中继检测到有写操作的时候，它就会把相应的文件从缓存中删除，需要设置文件匹配列表及其设置的优先级等内容；
* luster/stripe   #条带中继，将单个大文件分成多个小文件存于各个服务器中，实现大文件的分块存储。
