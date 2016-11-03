### NFS服务简介
#### NFS简介
>NFS 是Network File System的缩写，即网络文件系统。一种使用于分散式文件系统的协议，由Sun公司开发，于1984年向外公布。功能是通过网络让不同的机器、不同的操作系统能够彼此分享彼此的数据，让应用程序在客户端通过网络访问位于服务器磁盘中的数据，是在类Unix系统间实现磁盘文件共享的一种方法。
  NFS 的基本原则是“允许不同的客户端及服务端通过一组RPC分享相同的文件系统”，它是独立于操作系统，允许不同硬件及操作系统的系统共同进行文件的分享。
  NFS在文件传送或信息传送过程中依赖于RPC协议。RPC，远程过程调用 (Remote Procedure Call) 是能使客户端执行其他系统中程序的一种机制。NFS本身是没有提供信息传输的协议和功能的，但NFS却能让我们通过网络进行资料的分享，这是因为NFS使用了一些其它的传输协议。而这些传输协议用到这个RPC功能的。可以说NFS本身就是使用RPC的一个程序。或者说NFS也是一个RPC SERVER。所以只要用到  NFS的地方都要启动RPC服务，不论是NFS SERVER或者NFS CLIENT。这样SERVER和CLIENT才能通过RPC来实现PROGRAM PORT的对应。可以这么理解RPC和NFS的关系：NFS是一个文件系统，而RPC是负责负责信息的传输。

NFS协议从诞生到现在为止，已经有多个版本，如NFS V2（rfc1094）,NFS V3（rfc1813）（最新的版本是V4（rfc3010）。
 
#### 各NFS协议版本的主要区别

V3相对V2的主要区别：

* 文件尺寸
    V2最大只支持32BIT的文件大小(4G),而NFS V3新增加了支持64BIT文件大小的技术。
* 文件传输尺寸
    V3没有限定传输尺寸，V2最多只能设定为8k，可以使用-rsize and -wsize 来进行设定。
* 完整的信息返回
    V3增加和完善了许多错误和成功信息的返回，对于服务器的设置和管理能带来很大好处。
* 增加了对TCP传输协议的支持
    V2只提供了对UDP协议的支持，在一些高要求的网络环境中有很大限制，V3增加了对TCP协议的支持
* 异步写入特性
* 改进了SERVER的mount性能
* 有更好的I/O WRITES 性能。
* 更强网络运行效能，使得网络运作更为有效
* 更强的灾难恢复功能。

异步写入特性（v3新增加）介绍：
  NFS V3 能否使用异步写入，这是可选择的一种特性。NFS V3客户端发发送一个异步写入请求到服务器，在给客户端答复之前服务器并不是必须要将数据写入到存储器中（稳定的）。服务器能确定何时去写入数据或者将多个写入请求聚合到一起并加以处理，然后写入。客户端能保持一个数据的copy以防万一服务器不能完整的将数据写入。当客户端希望释放这个copy的时候，它会向服务器通过这个操作过程，以确保每个操作步骤的完整。异步写入能够使服务器去确定最好的同步数据的策略。使数据能尽可能的同步的提交何到达。与V2比较来看，这样的机制能更好的实现数据缓冲和更多的平行（平衡）。而NFS V2的SERVER在将数据写入存储器之前不能再相应任何的写入请求。

V4相对V3的改进：

* 改进了INTERNET上的存取和执行效能
* 在协议中增强了安全方面的特性
* 增强的跨平台特性
 
### 安装部署NFS
#### 系统环境

系统平台：`Red Hat Enterprise Linux Server release 5.4 (Tikanga)`
```
NFS Server IP：172.16.7.56
NFS Client IP：172.16.7.57
```

#### 安装NFS服务
  NFS服务的安装非常简单，只需要两个软件包即可，在通常情况下，作为系统的默认软件包安装。

* nfs-utils-*    :包括基本的NFS命令与监控程序
* portmap-*    ：支持安全NFS RPC服务的连接
 
##### 查看系统是否安装NFS
```
rpm -qa nfs-utils
 nfs-utils-1.0.9-42.el5
rpm -qa portmap
 portmap-4.0-65.2.2.1
```
系统已经默认安装了nfs-utils、portmap 两个软件包，如果没有安装，可以通过rpm和yum命令安装
 
##### NFS系统守护进程
> RPC（Remote Procedure Call） NFS本身是没有提供信息传输的协议和功能的，但NFS却能让我们通过网络进行资料的分享，这是因为NFS使用了一些其它的传输协议。而这些传输协议勇士用到这个RPC功能的。可以说NFS本身就是使用RPC的一个程序。或者说NFS也是一个RPC SERVER.所以只要用到NFS的地方都要启动RPC服务，不论是NFS SERVER或者NFS CLIENT。这样SERVER和CLIENT才能通过RPC来实现PROGRAM PORT的对应。可以这么理解RPC和NFS的关系：NFS是一个文件系统，而RPC是负责负责信息的传输。
 
* NFS需要启动的Daemons：
  * pc.nfsd:    基本的NFS守护进程，主要负责Clinet登录权限检查。
  * rpm.mountd:    RPC安装守护进程，负责NFS的文件系统，当Client端通过rpc.nfsd登录NFS Server后，对Client存取Server的文件前，还必须通过文件使用权限的验证，他会读取NFS的配置文件/etc/exports来对比Client权限。
 
* NFS Server 在Red Hat平台下需要两个NFS Daemons套件
  * nfs-utils：    提供rpc.nfsd及rpc.mountd这两个NFS Daemons的套件
  * portmap：    NFS其实可以看作一个RPC Server Program，主要功能是进行端口映射。当Client尝试连接并使用RPC服务提供的服务（NFS）时，portmap会将所管理的服务对应的端口提供给客户点，从而是Client可以通过该端口请求服务。
 
##### 配置NFS服务

NFS服务的配置相对简单，只需要在对应文件中进行配置，然后启动NFS服务即可。
NFS常用文件：

* /etc/exports                              NFS服务的主要配置文件
* /usr/sbin/exportfs                        NFS服务的管理命令
* /usr/sbin/showmount                       客户端的查看命令
* /var/lib/nfs/etab                         记录NFS分享出来的目录的完整权限设定值
* /var/lib/nfs/xtab                         记录曾经登录过的Clinent 信息

NFS服务的配置文件是`/ext/exports`，这个文件是NFS的主要配置文件，不过系统并没有默认值，所以这个文件不一定存在，可能要自己手动创建，写入相应配置内容。

/etc/exports文件内容格式：

 [客户端1 选项（访问权限,用户映射,其他）] [客户端2 选项（访问权限,用户映射,其他）]

* 输出目录：
    输出目录是指NFS系统中需要共享给客户端使用的目录
* 客户端：
   客户端是指网络中可以访问这个NFS Server的主机，客户端常用的指定方式如下：
* 指定IP地址：172.16.7.57
  * 指定子网中的主机：172.16.7.0/24
  * 指定域名的主机：ssq-54-57.zerounix.com
  * 指定域中的所有主机：*.zerounix.com
  * 所有主机：*

##### 选项：
  选项用来设置输出目录的访问权限、用户映射等。
NFS主要有3类选项：

* 访问权限选项：
  * 设置输出目录只读：ro
  * 设置输出目录读写：rw

* 用户映射选项：
  * all_squash：                  将远程访问的所有普通用户及属组都映射为匿名用户或用户组(nfsnobody)；
  * no_all_squash：            与all_squash相反（default）；
  * root_squash：                将root用户及属组都映射问匿名用户或用户组（default）；
  * no_root_squash：
  * anonuid=xxx：                将远程访问的所有用户都映射为匿名用户，并指定用户问本地用户（UID=xxx）；
  * anongid=xxx：                将远程访问的所有用户都映射为匿名用户组，并指定用户问本地用户组（GID=xxx）；
* 其他选项：
 * secure：        限制客户端只能从小于1024的tcp端口连接NFS Server（default）；
 * insecure：    允许客户端从大于1024的tcp端口连接NFS Server；
 * sync：            将数据同步下乳内存缓冲区与磁盘中，效率低，但是可以保证数据的一致性；
 * async：           将数据先保存在内存缓冲区中，必要时才写入磁盘；
 * wdelay：        检查是否有相关的写操作，如果有则见这些写操作一起执行，可以提高效率（default）；
 * no_wdelay：  若有写操作立即执行，应与sync配合使用；
 * subtree：        若输出目录是一个子目录，则NFS Server将检查其父目录权限（default）；
 * no_subtree：   若输出目录是一个子目录，则NFS Server将不检查其父目录权限；

例如：编辑/etc/exports 为
```
/tmp        *(rw,no_root_squash)
/home/public    172.16.7.57(rw)    172.16.7.0/24(ro)
```

#### NFS Server的启动与停止
在对exports文件进行了正确的配置后，就可以启动NFS Server了。

##### 启动NFS Server
为了使NFS 服务可以正常工作，需要启动portmap和nfs两个服务，并且portmap要先于nfs启动。
```
service portmap start
service nfs start
```
##### 停止NFS Server
要停止NFS时，要先停止NFS服务在停止portmap，对于系统中有其他服务（如NIS）需要使用时，不要停止portmap。
```
service portmap start
Starting portmap:

service nfs start
Starting NFS services:
Starting NFS quotas:
Starting NFS daemon:
Starting NFS mountd:
```

### 实例
将NFS Server的/data/charlie/ 共享给172.16.7.57，权限读写

#### 修改配置文件exports
```
cat /etc/exports
/data/charlie   172.16.7.57(rw,no_root_squash)
```

##### 重启NFS
```
service portmap start
service nfs start
```

查看是否应用配置
```
exportfs
/data/charlie   172.16.7.57
```

##### Client挂载目录
命令格式：
```
mount options NFS_IP:共享目录 本地挂载点
mount -t nfs -o nolock 172.16.7.56:/data/zerounix /mnt
```
 
##### 查看NFS挂载状态
Server 端：
显示已经被Client挂载的目录信息
```
showmount -a
All mount points on ssq-54.56.zerounix.com:
172.16.7.57:/data/zerounix
```
 
Client端：
查看NFS共享状态
```
showmount -a
Export list for 172.16.7.56
/data/zerounix 172.16.7.57
```
 
查看文件是否统一
 
NFS有很多默认的参数，打开/var/lib/nfs/etab 查看分享出来的/home/david/ 完整权限设定值。
```
cat /var/lib/nfs/etab
/data/zerounix    172.16.7.57(rw,sync,wdelay,hide,nocrossmnt,secure,no_root_squash,no_all_squash,no_subtree_check,secure_locks,acl,mapping=identity,anonuid=65534,anongid=65534)
```
