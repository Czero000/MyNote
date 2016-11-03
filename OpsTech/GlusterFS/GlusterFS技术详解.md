# 什么是 GlusterFS

 ![logo](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/logo.png)

## GlusterFS 概述

[GlusterFS](http://www.gluster.com/products/glusterfs/)是 Scale-Out 存储解决方案 Gluster 的核心，他是一个开源的分布式文件系统，具有强大的横向扩展能力，通过扩展能够支持数PB存储容量和处理数千客户端。GlusterFS 借助 TCP/IP 或 InfiniBand RDMA (一种支持多并发链接的“转换线缆”技术)网络将物理分布的存储资源聚集在一起，使用单一全局命名空间来管理数据。GlusterFS 基于可堆叠的用户空间设计，可为各种不同的数据负载提供优异的性能。

 ![glusterfs_mount](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/glusterfs_mount.png)

GlusterFS 支持运行在任何标准IP网络上标准应用程序的标准客户端，如图2所示，用户可以在全局统一的命名空间中使用NFS/CIFS等标准协议来访问应用数据。GlusterFS 使得用户可摆脱原有的独立、高成本的封闭存储系统，能够利用普通廉价的存储设备来部署可集中管理、横向扩展、虚拟化的存储池，存储容量可扩展至TB/PB级。GlusterFS主要特征如下：

- **扩展性和高性能**

GlusterFS 利用双重特性来提供几TB至数PB的高扩展存储解决方案。Scale-Out 架构允许通过简单地增加资源来提高存储容量和性能，磁盘、计算和 I/O 资源都可以独立增加，支持 10GbE 和 InfiniBand 等高速网络互联。Gluster 弹性哈希（Elastic Hash）解除了 GlusterFS 对元数据服务器的需求，消除了单点故障和性能瓶颈，真正实现了并行化数据访问。

- **高可用性**

GlusterFS 可以对文件进行自动复制，如镜像或多次复制，从而确保数据总是可以访问，甚至是在硬件故障的情况下也能正常访问。自我修复功能能够把数据恢复到正确的状态，而且修复是以增量的方式在后台执行，几乎不会产生性能负载。GlusterFS 没有设计自己的私有数据文件格式，而是采用操作系统中主流标准的磁盘文件系统（如 EXT3、ZFS）来存储文件，因此数据可以使用各种标准工具进行复制和访问。

- **全局统一命名空间**

全局统一命名空间将磁盘和内存资源聚集成一个单一的虚拟存储池，对上层用户和应用屏蔽了底层的物理硬件。存储资源可以根据需要在虚拟存储池中进行弹性扩展， 比如扩容或收缩。当存储虚拟机映像时，存储的虚拟映像文件没有数量限制，成千虚拟机均通过单一挂载点进行数据共享。虚拟机I/O可在命名空间内的所有服务器上自动进行负载均衡，消除了SAN环境中经常发生的访问热点和性能瓶颈问题。

- **弹性哈希算法**

GlusterFS采用弹性哈希算法在存储池中定位数据，而不是采用集中式或分布式元数据服务器索引。在其他的Scale-Out存储系统中，元数据服务器通常会导致I/O性能瓶颈和单点故障问题。GlusterFS中，所有在Scale-Out存储配置中的存储系统都可以智能地定位任意数据分片，不需要查看索引或者向其他服务器查询。这种设计机制完全并行化了数据访问，实现了真正的线性性能扩展。

- **弹性卷管理**

数 据储存在逻辑卷中，逻辑卷可以从虚拟化的物理存储池进行独立逻辑划分而得到。存储服务器可以在线进行增加和移除，不会导致应用中断。逻辑卷可以在所有配置 服务器中增长和缩减，可以在不同服务器迁移进行容量均衡，或者增加和移除系统，这些操作都可在线进行。文件系统配置更改也可以实时在线进行并应用，从而可 以适应工作负载条件变化或在线性能调优。

- **基于标准协议**

Gluster存储服务支持NFS, CIFS, HTTP, FTP 以及 Gluster 原生协议，完全与 POSIX 标准兼容。现有应用程序不需要作任何修改或使用专用 API，就可以对 Gluster 中的数据进行访问。这在公有云环境中部署 Gluster 时非常有用，Gluster 对云服务提供商专用API进行抽象，然后提供标准 POSIX 接口。

---

## 设计目标

GlusterFS 的设计思想显著区别有现有并行/集群/分布式文件系统。如果 GlusterFS 在设计上没有本质性的突破，难以在与 Lustre、PVFS2、Ceph 等的竞争中占据优势，更别提与 GPFS、StorNext、ISILON、IBRIX 等具有多年技术沉淀和市场积累的商用文件系统竞争。其核心设计目标包括如下三个：

-  **弹性存储系统（Elasticity）**

存储系统具有弹性能力，意味着企业可以根据业务需要灵活地增加或缩减数据存储以及增删存储池中的资源，而不需要中断系统运行。GlusterFS 设计目标之一就是弹性，允许动态增删数据卷、扩展或缩减数据卷、增删存储服务器等，不影响系统正常运行和业务服务。GlusterFS 早期版本中弹性不足，部分管理工作需要中断服务，目前最新的 3.1.X 版本已经弹性十足，能够满足对存储系统弹性要求高的应用需求，尤其是对云存储服务系统而言意义更大。GlusterFS 主要通过存储虚拟化技术和逻辑卷管理来实现这一设计目标。

-  **线性横向扩展（Linear Scale-Out）**

线性扩展对于存储系统而言是非常难以实现的，通常系统规模扩展与性能提升之间是 LOG 对数曲线关系，因为同时会产生相应负载而消耗了部分性能的提升。现在的很多并行/集群/分布式文件系统都具很高的扩展能力，Luster 存储节点可以达到 1000 个以上，客户端数量能够达到 25000 以上，这个扩展能力是非常强大的，但是Lustre也不是线性扩展的。

纵向扩展（Scale-Up）旨在提高单个节点的存储容量或性能，往往存在理论上或物理上的各种限制，而无法满足存储需求。横向扩展（Scale-Out）通过增加存储节点来提升整个系统的容量或性能，这一扩展机制是目前的存储技术热点，能有效应对容量、性能等存储需求。目前的并行/集群/分布式文件系统大多都具备横向扩展能力。

GlusterFS是线性横向扩展架构，它通过横向扩展存储节点即可以获得线性的存储容量和性能的提升。因此，结合纵向扩展GlusterFS可以获得多维扩展能力，增加每个节点的磁盘可增加存储容量，增加存储节点可以提高性能，从而将更多磁盘、内存、I/O资源聚集成更大容量、更高性能的虚拟存储池。GlusterFS利用三种基本技术来获得线性横向扩展能力

1\. **消除元数据服务**

2\. **高效数据分布，获得扩展性和可靠性**

3\. **通过完全分布式架构的并行化获得性能的最大化**

4\. **高可靠性（Reliability）**

与GFS（Google File System）类似，GlusterFS 可以构建在普通的服务器和存储设备之上，因此可靠性显得尤为关键。GlusterFS 从设计之初就将可靠性纳入核心设计，采用了多种技术来实现这一设计目标。首先，它假设故障是正常事件，包括硬件、磁盘、网络故障以及管理员误操作造成的数据损坏等。GlusterFS 设计支持自动复制和自动修复功能来保证数据可靠性，不需要管理员的干预。其次，GlusterFS 利用了底层 EXT3/ZFS 等磁盘文件系统的日志功能来提供一定的数据可靠性，而没有自己重新发明轮子。再次，GlusterFS 是无元数据服务器设计，不需要元数据的同步或者一致性维护，很大程度上降低了系统复杂性，不仅提高了性能，还大大提高了系统可靠性。

---

## 技术特点

GlusterFS在技术实现上与传统存储系统或现有其他分布式文件系统有显著不同之处，主要体现在如下几个方面。

- **完全软件实现（Software Only）**

GlusterFS 认为存储是软件问题，不能够把用户局限于使用特定的供应商或硬件配置来解决。GlusterFS 采用开放式设计，广泛支持工业标准的存储、网络和计算机设备，而非与定制化的专用硬件设备捆绑。对于商业客户，GlusterFS 可以以虚拟装置的形式交付，也可以与虚拟机容器打包，或者是公有云中部署的映像。开源社区中，GlusterFS 被大量部署在基于廉价闲置硬件的各种操作系统上，构成集中统一的虚拟存储资源池。简而言之，GlusterFS 是开放的全软件实现，完全独立于硬件和操作系统。

- **完整的存储操作系统栈（Complete Storage Operating System Stack）**

GlusterFS 不仅提供了一个分布式文件系统，而且还提供了许多其他重要的分布式功能，比如分布式内存管理、I/O 调度、软 RAID 和自我修复等。GlusterFS 汲取了微内核架构的经验教训，借鉴了 GNU/Hurd 操作系统的设计思想，在用户空间实现了完整的存储操作系统栈。

- **用户空间实现（User Space）**

与传统的文件系统不同，GlusterFS在用户空间实现，这使得其安装和升级特别简便。另外，这也极大降低了普通用户基于源码修改 GlusterFS 的门槛，仅仅需要通用的C程序设计技能，而不需要特别的内核编程经验。

- **模块化堆栈式架构（Modular Stackable Architecture）**

GlusterFS 采用模块化、堆栈式的架构，可通过灵活的配置支持高度定制化的应用环境，比如大文件存储、海量小文件存储、云存储、多传输协议应用等。每个功能以模块形式实现，然后以积木方式进行简单的组合，即可实现复杂的功能。比如，Replicate 模块可实现 RAID1，Stripe 模块可实现 RAID0，通过两者的组合可实现 RAID10和RAID01，同时获得高性能和高可靠性。

- **原始数据格式存储（Data Stored in Native Formats）**

GlusterFS 以原始数据格式（如 EXT3、EXT4、XFS、ZFS）储存数据，并实现多种数据自动修复机制。因此，系统极具弹性，即使离线情形下文件也可以通过其他标准工具进行访问。如果用户需要从 GlusterFS 中迁移数据，不需要作任何修改仍然可以完全使用这些数据。

- **无元数据服务设计（No Metadata with the Elastic Hash Algorithm）**

对 Scale-Out 存 储系统而言，最大的挑战之一就是记录数据逻辑与物理位置的映像关系，即数据元数据，可能还包括诸如属性和访问权限等信息。传统分布式存储系统使用集中式或 分布式元数据服务来维护元数据，集中式元数据服务会导致单点故障和性能瓶颈问题，而分布式元数据服务存在性能负载和元数据同步一致性问题。特别是对于海量 小文件的应用，元数据问题是个非常大的挑战。

GlusterFS 独 特地采用无元数据服务的设计，取而代之使用算法来定位文件，元数据和数据没有分离而是一起存储。集群中的所有存储系统服务器都可以智能地对文件数据分片进 行定位，仅仅根据文件名和路径并运用算法即可，而不需要查询索引或者其他服务器。这使得数据访问完全并行化，从而实现真正的线性性能扩展。无元数据服务器 极大提高了 GlusterFS 的性能、可靠性和稳定性。

---

## 总体架构和设计

![gluster架构和组成](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/gluster架构和组成.png)

GlusterFS总体架构与组成部分如上图所示，它主要由存储服务器（Brick Server）、客户端以及 NFS/Samba 存储网关组成。不难发现，GlusterFS 架构中没有元数据服务器组件，这是其最大的设计这点，对于提升整个系统的性能、可靠性和稳定性都有着决定性的意义。GlusterFS 支持 TCP/IP 和 InfiniBand RDMA 高速网络互联，客户端可通过原生Glusterfs协议访问数据，其他没有运行 GlusterFS 客户端的终端可通过 NFS/CIFS 标准协议通过存储网关访问数据。

存储服务器主要提供基本的数据存储功能，最终的文件数据通过统一的调度策略分布在不同的存储服务器上。它们上面运行着Glusterfsd进行，负责处理来自其他组件的数据服务请求。如前所述，数据以原始格式直接存储在服务器的本地文件系统上，如EXT3、EXT4、XFS、ZFS等，运行服务时指定数据存储路径。多个存储服务器可以通过客户端或存储网关上的卷管理器组成集群，如Stripe（RAID0）、Replicate（RAID1）和DHT（分布式Hash）存储集群，也可利用嵌套组合构成更加复杂的集群，如RAID10。

由于没有了元数据服务器，客户端承担了更多的功能，包括数据卷管理、I/O 调度、文件定位、数据缓存等功能。客户端上运行 Glusterfs 进程，它实际是 Glusterfsd 的符号链接，利用 FUSE（File system in User Space）模块将GlusterFS 挂载到本地文件系统之上，实现 POSIX 兼容的方式来访问系统数据。在最新的 3.1.X 版本中，客户端不再需要独立维护卷配置信息，改成自动从运行在网关上的 glusterd 弹性卷管理服务进行获取和更新，极大简化了卷管理。GlusterFS 客户端负载相对传统分布式文件系统要高，包括CPU占用率和内存占用。

GlusterFS 存储网关提供弹性卷管理和 NFS/CIFS 访问代理功能，其上运行 Glusterd 和 Glusterfs 进程，两者都是 Glusterfsd 符号链接。卷管理器负责逻辑卷的创建、删除、容量扩展与缩减、容量平滑等功能，并负责向客户端提供逻辑卷信息及主动更新通知功能等。GlusterFS 3.1.X 实现了逻辑卷的弹性和自动化管理，不需要中断数据服务或上层应用业务。对于Windows客户端或没有安装 GlusterFS 的客户端，需要通过 NFS/CIFS 代理网关来访问，这时网关被配置成 NFS 或 Samba 服务器。相对原生客户端，网关在性能上要受到 NFS/Samba 的制约。

 ![gluster模块化堆栈设计](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/gluster模块化堆栈设计.png)

GlusterFS 是模块化堆栈式的架构设计，如图3所示。模块称为 Translator，是 GlusterFS 提供的一种强大机制，借助这种良好定义的接口可以高效简便地扩展文件系统的功能。服务端与客户端模块接口是兼容的，同一个 translator可同时在两边加载。每个 translator 都是 SO 动态库，运行时根据配置动态加载。每个模块实现特定基本功能，GlusterFS 中所有的功能都是通过 translator 实现，比如Cluster, Storage, Performance, Protocol, Features等，基本简单的模块可以通过堆栈式的组合来实现复杂的功能。这一设计思想借鉴了 GNU/Hurd 微内核的虚拟文件系统设计，可以把对外部系统的访问转换成目标系统的适当调用。大部分模块都运行在客户端，比如合成器、I/O调度器和性能优化等，服务端相对简单许多。客户端和存储服务器均有自己的存储栈，构成了一棵 Translator 功能树，应用了若干模块。模块化和堆栈式的架构设计，极大降低了系统设计复杂性，简化了系统的实现、升级以及系统维护。

---

## 弹性哈希算法

对于分布式系统而言，元数据处理是决定系统扩展性、性能以及稳定性的关键。GlusterFS 另辟蹊径，彻底摒弃了元数据服务，使用弹性哈希算法代替传统分布式文件系统中的集中或分布式元数据服务。这根本性解决了元数据这一难题，从而获得了接近线性的高扩展性，同时也提高了系统性能和可靠性。GlusterFS 使用算法进行数据定位，集群中的任何服务器和客户端只需根据路径和文件名就可以对数据进行定位和读写访问。换句话说，GlusterFS 不需要将元数据与数据进行分离，因为文件定位可独立并行化进行。GlusterFS 中数据访问流程如下

1. **计算hash值，输入参数为文件路径和文件名；**
2. **根据hash值在集群中选择子卷（存储服务器），进行文件定位；**
3. **对所选择的子卷进行数据访问。**

GlusterFS目前使用Davies-Meyer算法计算文件名hash值，获得一个32位整数。Davies-Meyer 算法具有非常好的hash分布性，计算效率很高。假设逻辑卷中的存储服务器有N个，则32位整数空间被平均划分为N个连续子空间，每个空间分别映射到一个存储服务器。这样，计算得到的32位hash值就会被投射到一个存储服务器，即我们要选择的子卷。难道真是如此简单？现在让我们来考虑一下存储节点加入和删除、文件改名等情况，GlusterFS如何解决这些问题而具备弹性的呢？

逻辑卷中加入一个新存储节点，如果不作其他任何处理，hash 值 映射空间将会发生变化，现有的文件目录可能会被重新定位到其他的存储服务器上，从而导致定位失败。解决问题的方法是对文件目录进行重新分布，把文件移动到 正确的存储服务器上去，但这大大加重了系统负载，尤其是对于已经存储大量的数据的海量存储系统来说显然是不可行的。另一种方法是使用一致性哈希算法，修改 新增节点及相邻节点的 hash 映射空间，仅需要移动相邻节点上的部分数据至新增节点，影响相对小了很多。然而，这又带来另外一个问题，即系统整体负载不均衡。GlusterFS 没有采用上述两种方法，而是设计了更为弹性的算法。GlusterFS 的 哈希分布是以目录为基本单位的，文件的父目录利用扩展属性记录了子卷映射信息，其下面子文件目录在父目录所属存储服务器中进行分布。由于文件目录事先保存 了分布信息，因此新增节点不会影响现有文件存储分布，它将从此后的新创建目录开始参与存储分布调度。这种设计，新增节点不需要移动任何文件，但是负载均衡 没有平滑处理，老节点负载较重。GlusterFS 在设计中考虑了这一问题，在新建文件时会优先考虑容量负载最轻的节点，在目标存储节点上创建文件链接直向真正存储文件的节点。另外，GlusterFS 弹性卷管理工具可以在后台以人工方式来执行负载平滑，将进行文件移动和重新分布，此后所有存储服务器都会均会被调度。

GlusterFS目前对存储节点删除支持有限，还无法做到完全无人干预的程度。如果直接删除节点，那么所在存储服务器上的文件将无法浏览和访问，创建文件目录也会失败。当前人工解决方法有两个，一是将节点上的数据重新复制到GlusterFS中，二是使用新的节点来替换删除节点并保持原有数据。

如果一个文件被改名，显然hash算法将产生不同的值，非常可能会发生文件被定位到不同的存储服务器上，从而导致文件访问失败。采用数据移动的方法，对于大文件是很难在实时完成的。为了不影响性能和服务中断，GlusterFS采 用了文件链接来解决文件重命名问题，在目标存储服务器上创建一个链接指向实际的存储服务器，访问时由系统解析并进行重定向。另外，后台同时进行文件迁移， 成功后文件链接将被自动删除。对于文件移动也作类似处理，好处是前台操作可实时处理，物理数据迁移置于后台选择适当时机执行。

 ![GlusterFS弹性卷管理](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/GlusterFS弹性卷管理.png)

弹性哈希算法为文件分配逻辑卷，那么 GlusterFS 如何为逻辑卷分配物理卷呢？GlusterFS3.1.X 实现了真正的弹性卷管理，如图4所 示。存储卷是对底层硬件的抽象，可以根据需要进行扩容和缩减，以及在不同物理系统之间进行迁移。存储服务器可以在线增加和移除，并能在集群之间自动进行数 据负载平衡，数据总是在线可用，没有应用中断。文件系统配置更新也可以在线执行，所作配置变动能够快速动态地在集群中传播，从而自动适应负载波动和性能调优。
弹性哈希算法本身并没有提供数据容错功能，GlusterFS使用镜像或复制来保证数据可用性，推荐使用镜像或3路复制。复制模式下，存储服务器使用同步写复制到其他的存储服务器，单个服务器故障完全对客户端透明。此外，GlusterFS没有对复制数量进行限制，读被分散到所有的镜像存储节点，可以提高读性能。弹性哈希算法分配文件到唯一的逻辑卷，而复制可以保证数据至少保存在两个不同存储节点，两者结合使得GlusterFS具备更高的弹性。

---

## Translators

如前所述，Translators 是 GlusterFS 提供的一种强大文件系统功能扩展机制，这一设计思想借鉴于 GNU/Hurd 微内核操作系统。GlusterFS 中所有的功能都通过 Translator 机制实现，运行时以动态库方式进行加载，服务端和客户端相互兼容。GlusterFS 3.1.X中，主要包括以下几类 Translator

1. **Cluster**：存储集群分布，目前有 AFR, DHT, Stripe 三种方式
2. **Debug**：跟踪 GlusterFS 内部函数和系统调用
3. **Encryption**：简单的数据加密实现
4. **Features**：访问控制、锁、Mac兼容、静默、配额、只读、回收站等
5. **Mgmt**：弹性卷管理
6. **Mount**：FUSE接口实现
7. **Nfs**：内部NFS服务器
8. **Performance**：io-cache, io-threads, quick-read, read-ahead, stat-prefetch, sysmlink-cache, write-behind等性能优化
9. **Protocol**：服务器和客户端协议实现
10. **Storage**：底层文件系统POSIX接口实现

这里我们重点介绍一下Cluster Translators，它是实现GlusterFS集群存储的核心，它包括AFR（Automatic File Replication）、DHT（Distributed Hash Table）和Stripe三种类型。

AFR相当于RAID1，同一文件在多个存储节点上保留多份，主要用于实现高可用性以及数据自动修复。AFR所有子卷上具有相同的名字空间，查找文件时从第一个节点开始，直到搜索成功或最后节点搜索完毕。读数据时，AFR会把所有请求调度到所有存储节点，进行负载均衡以提高系统性能。写数据时，首先需要在所有锁服务器上对文件加锁，默认第一个节点为锁服务器，可以指定多个。然后，AFR以日志事件方式对所有服务器进行写数据操作，成功后删除日志并解锁。AFR会自动检测并修复同一文件的数据不一致性，它使用更改日志来确定好的数据副本。自动修复在文件目录首次访问时触发，如果是目录将在所有子卷上复制正确数据，如果文件不存则创建，文件信息不匹配则修复，日志指示更新则进行更新。

DHT即上面所介绍的弹性哈希算法，它采用 hash 方式进行数据分布，名字空间分布在所有节点上。查找文件时，通过弹性哈希算法进行，不依赖名字空间。但遍历文件目录时，则实现较为复杂和低效，需要搜索所有的存储节点。单一文件只会调度到唯一的存储节点，一旦文件被定位后，读写模式相对简单。DHT 不具备容错能力，需要借助AFR实现高可用性, 如图5所示应用案例。

Stripe 相当于 RAID0，即分片存储，文件被划分成固定长度的数据分片以 Round-Robin 轮转方式存储在所有存储节点。Stripe 所有存储节点组成完整的名字空间，查找文件时需要询问所有节点，这点非常低效。读写数据时，Stripe涉及全部分片存储节点，操作可以在多个节点之间并发执行，性能非常高。Stripe 通常与 AFR 组合使用，构成 RAID10/RAID01，同时获得高性能和高可用性，当然存储利用率会低于50%。

 ![AFR_DHT](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/AFR_DHT.png)

---

## 设计讨论

GlusterFS 是一个具有高扩展性、高性能、高可用性、可横向扩展的弹性分布式文件系统，在架构设计上非常有特点，比如无元数据服务器设计、堆栈式架构等。然而，存储应用问题是很复杂的，GlusterFS也不可能满足所有的存储需求，设计实现上也一定有考虑不足之处，下面我们作简要分析。

- **无元数据服务器 vs 元数据服务器**

无元数据服务器设计的好处是没有单点故障和性能瓶颈问题，可提高系统扩展性、性能、可靠性和稳定性。对于海量小文件应用，这种设计能够有效解决元数据的难点 问题。它的负面影响是，数据一致问题更加复杂，文件目录遍历操作效率低下，缺乏全局监控管理功能。同时也导致客户端承担了更多的职能，比如文件定位、名字 空间缓存、逻辑卷视图维护等等，这些都增加了客户端的负载，占用相当的 CPU 和内存。

- **用户空间 vs 内核空间**

用户空间实现起来相对要简单许多，对开发者技能要求较低，运行相对安全。用户空间效率低，数据需要多次与内核空间交换，另外 GlusterFS 借助 FUSE 来实现标准文件系统接口，性能上又有所损耗。内核空间实现可以获得很高的数据吞吐量，缺点是实现和调试非常困难，程序出错经常会导致系统崩溃，安全性低。纵向扩展上，内核空间要优于用户空间，GlusterFS 有横向扩展能力来弥补。

- **堆栈式 vs 非堆栈式**

这有点像操作系统的微内核设计与单一内核设计之争。GlusterFS 堆栈式设计思想源自 GNU/Hurd 微内核操作系统，具有很强的系统扩展能力，系统设计实现复杂性降低很多，基本功能模块的堆栈式组合就可以实现强大的功能。查看GlusterFS卷配置文件我们可以发现，translator 功能树通常深达 10 层以上，一层一层进行调用，效率可见一斑。非堆栈式设计可看成类似 Linux 的单一内核设计，系统调用通过中断实现，非常高效。后者的问题是系统核心臃肿，实现和扩展复杂，出现问题调试困难。

- **原始存储格式 vs 私有存储格式**

GlusterFS使 用原始格式存储文件或数据分片，可以直接使用各种标准的工具进行访问，数据互操作性好，迁移和数据管理非常方便。然而，数据安全成了问题，因为数据是以平凡的方式保存的，接触数据的人可以直接复制和查看。这对很多应用显然是不能接受的，比如云存储系统，用户特别关心数据安全，这也是影响公有云存储发展的一 个重要原因。私有存储格式可以保证数据的安全性，即使泄露也是不可知的。GlusterFS要实现自己的私有格式，在设计实现和数据管理上相对复杂一些，也会对性能产生一定影响。

- **大文件 vs 小文件**

GlusterFS 适合大文件还是小文件存储？弹性哈希算法和 Stripe 数据分布策略，移除了元数据依赖，优化了数据分布，提高数据访问并行性，能够大幅提高大文件存储的性能。对于小文件，无元数据服务设计解决了元数据的问题。但GlusterFS 并没有在I/O方面作优化，在存储服务器底层文件系统上仍然是大量小文件，本地文件系统元数据访问是一个瓶颈，数据分布和并行性也无法充分发挥作用。因此，GlusterFS 适合存储大文件，小文件性能较差，还存在很大优化空间。

- **可用性 vs 存储利用率**

GlusterFS 使用复制技术来提供数据高可用性，复制数量没有限制，自动修复功能基于复制来实现。可用性与存储利用率是一个矛盾体，可用性高存储利用率就低，反之亦然。采用复制技术，存储利用率为1/复制数，镜像是 50%，三路复制则只有33%。其实，可以有方法来同时提高可用性和存储利用率，比如 RAID5 的利用率是 (n-1)/n，RAID6 是 (n-2)/n，而纠删码技术可以提供更高的存储利用率。但是，鱼和熊掌不可得兼，它们都会对性能产生较大影响。另外，GlusterFS 目前的代码实现不够好，系统不够稳定，BUGS 数量相对还比较多。从其官方网站的部署情况来看，测试用户非常多，但是真正在生产环境中的应用较少，存储部署容量几TB－几十TB 的占很大比率，数百TB－PB 级案例非常少。这也可以从另一个方面说明，GlusterFS 目前还不够稳定，需要更长的时间来检验。然而不可否认，GlusterFS 是一个有着光明前景的集群文件系统，线性横向扩展能力使它具有天生的优势，尤其是对于云存储系统。

---

# 使用 GlusterFS

## 术语解释

**Brick** ：GFS 中的存储单元，通过是一个受信存储池中的服务器的一个导出目录。可以通过主机名和目录名来标识，如'SERVER:EXPORT'

**Client** ：挂载了 GFS 卷的设备

**Extended Attributes:xattr** 是一个文件系统的特性，其支持用户或程序关联文件/目录和元数据。

**FUSE:Filesystem** Userspace 是一个可加载的内核模块，其支持非特权用户创建自己的文件系统而不需要修改内核代码。通过在用户空间运行文件系统的代码通过 FUSE 代码与内核进行桥接。

**Geo-Replication** 异地备份

**GFID** ：GFS 卷中的每个文件或目录都有一个唯一的 128位 的数据相关联，其用于模拟 inode

**Namespace** ：每个 Gluster 卷都导出单个 ns 作为 POSIX 的挂载点

**Node** ：一个拥有若干 brick 的设备

**RDMA**：远程直接内存访问，支持不通过双方的 OS 进行直接内存访问。

**RRDNS**：round robin DNS是一种通过 DNS 轮转返回不同的设备以进行负载均衡的方法

**Self-heal**：用于后台运行检测复本卷中文件和目录的不一致性并解决这些不一致。

**Split-brain**：脑裂

**Translator**： 翻译器，类似 Linux 系统的文件系统

**Volfile**：glusterfs 进程的配置文件，通常位于 `/var/lib/glusterd/vols/volname`

**Volume**：一组 bricks 的逻辑集合

---

## 安装 GlusterFS

### 系统环境介绍

- OS版本：`CentOS Linux release 7.1.1503 (Core)`
- 软件版本： 3.7.3（最新为3.7.10）
- 系统节点

| ip地址          | 挂载路径               |
| :------------ | :----------------- |
| 172.16.18.241 | /export/brick1/gv0 |
| 172.16.18.242 | /export/brick1/gv0 |
| 172.16.18.243 | /export/brick1/gv0 |
| 172.16.18.244 | /export/brick1/gv0 |

### 安装 GlusterFS

#### 安装软件包

```
// 下载 GlusterFs yum 源配置
wget -P /etc/yum.repos.d http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo

// 安装GlusterFS
yum install -y glusterfs glusterfs-fuse glusterfs-server xfsprogs
```

#### 配置开机启动

```
#systemctl enable glusterfsd.service
systemctl enable glusterd.service
systemctl start glusterd
#systemctl start glusterfsd
```

## 配置 GlusterFS 集群

### 添加节点到 GlusterFS 集群

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

### 创建数据存储目录

```
parted  /dev/sdb rm 1
mkfs.xfs -i size=512 /dev/sdb -f
mkdir -p /export/brick1
/bin/mount -t xfs /dev/sdb /export/brick1
mkdir /export/brick1/gv0
echo "/dev/sdb        /export/brick1  xfs     defaults        1       2" >> /etc/fstab
```

### 创建 GlusterFS 磁盘卷

```
// 创建系统卷 gv0（副本卷）
gluster volume create gv0 replica 2 172.16.18.241:/export/brick1/gv0 172.16.18.242:/export/brick1/gv0 172.16.18.243:/export/brick1/gv0 172.16.18.244:/export/brick1/gv0 force

//启动系统卷 gv0
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

### 安装客户端并 mount GlusterFS 文件系统

```
// 下载仓库文件
wget -P /etc/yum.repos.d  http://download.gluster.org/pub/gluster/glusterfs/LATEST/CentOS/glusterfs-epel.repo

//安装软件
yum install glusterfs glusterfs-fuse glusterfs-server

//创建挂载点
mkdir -p /opt/vmx/gv0

//client 挂载
/bin/mount -t glusterfs 172.16.18.241:/gv0 /opt/vmx/gv0

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
172.16.18.241:/gv0         559G  1.6G  558G   1% /opt/vmx/gv0
```

---

## 管理使用 GlusterFS

### Gluster 节点管理
在创建 volume 之前需要先将一组存储设备组成一个存储池，通过存储设备提供的 bricks 来组成卷。在设备上启动 glusterd 之后，可通过设备的主机名或 IP 地址，将设备加到存储池中。

```
gluster peer command
```

#### 节点状态

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

#### 添加节点

**命令：`gluster peer HostName`**

```
// 将节点 server 添加到存储池中
gluster peer prober server
```

#### 删除节点

**命令： `gluster peer detach HostName`**

```
// 将节点 server 从存储池中移除，移除节点时要保证节点上没有 brick，需要提前移除 brick
gluster peer detch server
```

gluster对于每个节点都会生成一个 UUID 来标识，因此如果节点的 IP 或主机名发生了变化，只需要重新执行 peer probe 即可。不过如果一个主机名曾经用过，想再改回去，则 gluster 会提示已经保存过。此时只能把节点 detach  掉，然后重新 probe。

---

### Gluster 卷管理 ###

Gluster 文件系统基于需求支持不同类型的卷类型。有些卷类型有益于扩展存储大小、一些可以提高性能、还有可以兼顾两者。

#### 卷的类型

- **Distributed Glusterfs Volume（分布卷）**

![Distributed_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Distributed_Volume.png)

这个是 GlusterFS 文件系统默认的卷类型，文件通过 hash 算法随机的分布到由bricks组成的卷上，因此不存在数据冗余。对于这样一个存储卷的优点是磁盘容量扩展强和使用率高。但是这也意味着一个 brick 损坏将导致数据丢失，除非 brick底层使用硬件 Raid 等外部冗余措施。


- **Replicated Glusterfs Volume（镜像卷、副本卷）**

![Replicated_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Replicated_Volume.png)

镜像卷类似raid1，解决了数据冗余问题，在创建时指定副本数量，副本在存储时会存放到不同 brick上， 因此，有几个复本就必须提供至少多个 brick。

**注意：在创建复本卷时，brick 数量与复本个数必须相等；否则将会报错。另外如果同一个节点提供了多个 brick，也可以在同一个结点上创建复本卷，但这并不安全，因为一台设备挂掉，其上面的所有 brick 就无法访问了。**



- **Striped Glusterfs Volume（条带卷）**

![Striped_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Striped_Volume.png)

类似与 raid0，但是考虑一个大文件被存储在一个 brick，许多客户在同一时间经常访问。这将导致单个 brick 过多的负载并会降低性能。带区卷数据存储在砖后将它划分为不同的条纹，将大文件将被分为小块(等于 brick 的数量体积),每个块都存储在一个 brick。实现负载分布和文件可以获取更快读取速度，但不提供数据冗余。



- **Distributed Replicated Glusterfs Volume（分布式复制卷）**

![Distributed_Replicated_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Distributed_Replicated_Volume.png)

此类型卷是基本复本卷的扩展,兼顾分布卷和复制卷的功能。，可以指定若干 brick 组成一个复本卷，另外若干 brick 组成另个复本卷。单个文件在复本卷内数据保持复制，不同文件在不同复本卷之间进行分布。


- **Striped Glusterfs Volume（分布式条带卷）**

![Distributed_Striped_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Distributed_Striped_Volume.png)

volume 中 brick 所包含的存储服务器数必须是s tripe 的倍数(>=2倍)，兼顾分布式和条带式的功能。

- 其他拓展卷

![Distributed_Striped_Replicated_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Distributed_Striped_Replicated_Volume.png "分布式镜像条带卷")

![Striped_Replicated_Volume](http://ofc9x1ccn.bkt.clouddn.com/glusterfs/Striped_Replicated_Volume.png "条带镜像卷")

---

#### 创建卷
- 创建分布式卷(DHT)

```
// DHT 卷将数据以哈希计算方式分布到各个 brick上，数据是以文件为单位存取，基本达到分布均衡，提供的容量为各个 brick 的容量总和
gluster volume create NEW-VOLNAME [transport [tcp | rdma | tcp,rdma]] NEW-BRICK...
gluster volume create dht_vol 172.16.18.{241,242,243,244}:/export/brick1/gv0
```

- 创建副本卷(AFR)

```
// AFR提供数据副本，副本数为 replica，即每个文件存储 replica 份数，文件不分割，以文件为存储单位：副本数需要等于brick数；当 brick 数是副本的倍数时，则自动变化为Replicated-Distributed卷
gluster volume create NEW-VOLNAME [replica COUNT] [transport [tcp | rdma | tcp,rdma]] NEW-BRICK...
gluster volume create afr_vol replica 2 [transport tcp] 172.16.18.{241,242,243,244}:/export/brick/gv0
```
**每两个 brick 组成一组，每组两个副本，文件又以DHT分布在三个组上，这样是副本卷和分布式卷的组合**


- 创建条带卷

```
//stripe卷类似raid0，将数据条带化，分布在不同的 brick，该方式将文件分块，将文件分成stripe块，分别进行存储，在大文件读取是有优势。stripe需要等于brick数；当brick数等于stripe数的倍数时，则自动变化为stripe-distributed卷。
gluster volume create NEW-VOLNAME [stripe COUNT] [transport [tcp | dma | tcp,rdma]] NEW-BRICK...
gluster volume create str_vol stripe 2 172.16.18.{241,242,243,244}:/export/brick1/gv0
```
**每2个 brick 组成一组，每组2个brick，文件以 DHT 分布在两个组中，每个组中将文件条带成2块**

- 创建Replicated-Stripe-Distributed卷

```
//使用 8 个 brick 创建一个组合卷，即brick数是 stripe*replica 的倍数，则创建三种基本卷的组合卷，若刚好等于 stripe*replica 则为 stript-Distrubted 卷
gluster volume create str_afr_dht_vol stripe 2 replica 2 172.16.18.{241,242,243,244}:/export/brick1/gv0  172.16.18.{241,242,243,244}:/export/brick1/gv1
```

#### 卷信息 ####
**命令：gluster volume info**
```
// 该命令能够查看存储池中当前卷的信息，包括卷方式、包含的 brick、卷的当期状态、卷名及 UUID 等
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
// 该命令能够查看当前卷的状态，包括其中各个 brick 的状态、NFS的服务状态及当前 task 执行情况和一些系统设置状态等
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
// 将创建的卷启动，才能进行客户端挂载；stop 能够将系统将停止；此外 gluster 并未提供 restart 的重启命令
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

#### 均衡卷

```
\\ 不迁移数据
gluster volume gv0 rebalance fix-layout start
gluster volume gv0 rebalance start
gluster volume gv0 rebalance startforce
gluster volume gv0 rebalance status
gluster volume gv0 rebalance stop
```

#### 修复卷

```
gluster volume heal mamm-volume #只修复有问题的文件  
gluster volume heal mamm-volume full #修复所有文件  
gluster volume heal mamm-volume info#查看自愈详情  
gluster volume heal mamm-volume info healed|heal-failed|split-brain  
```

**设置卷**

命令：`gluster volume set options`



#### 设置卷传输端口类型

1. Unmount the volume on all the clients using the following command

```
umount mount-point
```

2. Stop the volumes using the following command

```
gluster volume stop volname
```

3. Change the transport type. For example, to enable both tcp and rdma execute the followimg command

```
gluster volume set volname config.transport tcp,rdma OR tcp OR rdma
```

4. Mount the volume on all the clients. For example, to mount using rdma transport, use the following command

```
mount -t glusterfs -o transport=rdma server1:/test-volume /mnt/glusterfs
```

---


### Brick 管理

#### 添加 brick
**命令：gluster volume add-brick VOLNAME NEW-BRICK**
```
//添加两个 brick 到存储 gv0，副本卷则要一次添加的 bricks 数是 replica 的整数倍；stripe 同样要求
gluster peer probe 172.16.18.245
gluster peer probe 172.16.18.246
gluster volume add-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0
```

#### 移除 brick
**命令： `gluster volume remove-brick VOLNAME BRICK start/status/commit`**
```
// 若是副本卷，则要移除的 Brick 是 replica 的整数倍，stripe 具有同样的要求，副本卷要移除一对 Brick，在执行移除操作时，数据会移到其他节点。
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 start

// 在执行移除操作后，可以使用 status 命令进行 task 状态查看
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 status

// 使用 commit 命令执行 brick 移除，则不会进行数据迁移而直接删除 brick，符合不需要数据迁移的用户需求
gluster volume remove-brick gv0 172.16.18.245:/export/brick1/gv0  172.16.18.246:/export/brick1/gv0 commit
```
**ps：系统的扩容及缩减可以通过如上的节点、brick 管理组合达到目的**
**1. 扩容时，可以下增加系统节点，然后添加新增节点上的 brick 即可**
**2. 缩减时，可以先移除 brick，然后在进行节点删除达到缩减的目的，并保证不丢失数据**


#### 替换 brick
命令：`gluster volume replace-brick VOLNAME BRICKNEW-BRICK start/pause/sbort/status/commit`

```
// 将 `172.16.18.244：/export/brick1/gv0` 替换为 `172.16.18.245:/export/brick1/gv0`。在执行 replcase-brick，使用 start 启动命令之后，开始将原始 brick 的数据迁移到即将需要替换的 brick 上
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  start force

//在数据迁移过程中，可以查看替换状态
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  status

// 在数据迁移的过程中，可以执行 abort 命令终止 brick 替换
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0 abort

//当数据迁移结束之后，执行 commit 命令结束任务，则进行 brick 替换。使用 volume info 命令可以查看到 brick 已经被替换
gluster volume replace-brick gv0 172.16.18.244:/export/brick1/gv0  172.16.18.245:/export/brick1/gv0  start
```

---

## 系统拓展

### 系统配额

#### 开启、关闭系统配额
```
//在使用系统配额功能时，需要使用 enable 将其开启；disable为关闭命令
gluster volume quota VOLNAME enable/disable
```
#### 设置目录配额
```
gluster volume quota VOLNAME limit-usage /directory limit-value

//设置gv0卷下 quota 子目录目录限额为 10GB，这个目录是以系统挂载目录为根目录，所以 /quota即客户端挂载目录下的子目录
gluster volume quota gv0 limit-usage /quota 10GB
```

#### 配额查看
```
gluster volume quota VOLNAME list
gluster volume quota VOLNAME list /directory_name
//可以使用上面命令查看卷的配额，第一个查看全部配额设置，第二个可以根据目录查看，显示配额大小及当前使用容量，如无使用容量则说明设置的目录有误(不存在)
gluster volume quota gv0 list
```

#### 地域复制(geo-replication)
```
gluster volume geo-replication MASTER SLAVE start/status/stop

//地域复制是系统提供的灾备功能，能够将系统的全部数据进行异步的增量备份到另外的磁盘中
gluster volume geo-replication gv0 172.16.18.250:/export/brick/gv0 start

//当开始执行gv0卷的所有内容备份到18.250下的/export/brick/gv0中的task，值得注意的是，这个备份目标不能是系统中的brick
```

#### I/O信息查看
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
`top command`允许你查看 bricks 的性能，`read、write、file open calls、file read caclls、file write calls、directory open calls、directory read calls`。所有的查看都可以设置 top 数，默认是1000
```
// 查看打开的 fd
gluster volume top VOLNAME open [brick BRICK-NAME] [list-cnt cnt]

// 查看调用次数最多的读调用
gluster volume top VOLNAME read [brick BRICK-NAME] [list-cnt cnt]

// 查看调用次数最多的写调用
gluster volume top VOLNAME write [brick BRICK-NAME] [list-cnt cnt]

// 查看次数最多的目录调用
gluster volume top opendir [brick BRICK-NAME] [list-cnt cnt]
gluster volume top readdir [brick BRICK-NAME] [list-cnt cnt]

//查看每个 brick 的读性能
gluster volume top VOLNAME read-perf [bs blk-size count count] [brick BRICK-NAME] [list-cnt cnt]

//查看每个 brick 的写性能
gluster volume top VOLNAME write-perf [bs blk-size count count] [brick BRICK-NAME] [list-cnt cnt]
```

---

### Glusterfs 冗余镜像（AFR）修复原理以及脑裂分析

#### 什么是脑裂

所谓脑裂，就是指两个或多个节点都“认为”自身是正常节点而互相“指责”对方，导致不能选取正确的节点进行接管或修复，导致脑裂状态。这种现象出现在数据修复、集群管理等等高可用场景。Glusterfs 的冗余镜像（下文简称 AFR）提供了数据副本功能，能够在即使只有一个冗余节点的情况下仍能正常工作，不中断上层应用。当节点恢复后，能够将数据修复到一致状态，保证数据的安全。

**AFR工作原理**

AFR数据修复主要涉及三个方面：`ENTRY，META，DATA`，我们以冗余度为 2 即含有两个副本 A 和 B 的 DATA 修复为例进行讲解。记录描述副本状态的称之为 ChangeLog，记录在每个副本文件扩展属性里，读入内存后以矩阵形式判断是否需要修复以及要以哪个副本为 Source 进行修复。初始值以及正常值为 0.（注：ENTRY 和 META,DATA 分布对应着一个数值）。

Write的步骤可分解为：

1. 下发 Write 操作
2. 加锁 Lock
3. 向 A，B 副本的 ChangeLog 分别加 1，记录到各个副本的扩展属性中
4. 对 A，B 副本进行写操作
5. 若该副本写成功则 ChangeLog 减 1，若该副本写失败则 ChangLog 值不变，记录到各个副本的扩展属性中
6. 解锁 UnLock
7. 向上层返回，只要有一个副本写成功就返回成功。


**上述在AFR中是完整的一个 transaction 动作。根据两个副本记录的 ChangeLog 的数值确定了副本的几种状态：**

- WISE，智慧的，即该副本的 ChangeLog 中对方对应的数值大于0而且自身对应的数值等于0.

- INNOCENT，无辜的，即该副本上的 ChangeLog 即不指责对方也指责自己，ChangeLog全为0.

- FOOL，愚蠢的，即该副本上的 ChangeLog 是指责自己的。

- IGNORANT，忽略的，即该副本的 ChangeLog 丢失。

所以一般情况下，会选取WISE的副本作为Sourse进行修复。但是当两个节点都是WISE状态时，这就出现了声名狼藉的脑裂状态。

**AFR脑裂**

两个副本均为 WISE 时发生脑裂，那么在哪种场景下会产生脑裂呢？我们还是以冗余度为2的情况举一个简单的例子：某文件 X 的两个副本位于物理机 A 和物理机 B 上，在 A 和 B 上分别运行着进程 a 和进程 b，a 和 b 持续通过各自所在的物理机上的客户端对文件 X 进行不同的写操作。然后物理机 A 和 B 之间网络中断，因为AFR在一个副本的情况下仍能不中断上层应用，所以进程a和进程b仍会持续运行，但因为网络中断，文 件X 在 A 和 B 上的副本数据不再一致且都认为对方是异常的，当网络恢复时，两个副本互相“指责”，即出现了脑裂。当然这是脑裂发生的场景之一，有时候是有可能发生脑裂，而有时候是必然发生脑裂。

[官方提供解决方案](http://gluster.readthedocs.org/en/latest/Troubleshooting/split-brain/)

## 参考文献

[官方文档:http://gluster.readthedocs.org/en/latest/](http://gluster.readthedocs.org/en/latest/)
