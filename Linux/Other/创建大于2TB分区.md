### parted命令介绍
parted命令可以划分单个分区大于2T的GPT格式的分区，也可以划分普通的MBR分区，fdisk命令对于大于2T的分区无法划分，所以用fdisk无法看到parted划分的GPT格式的分区。

Parted 命令分为两种模式：命令行模式和交互模式。

* 命令行模式： parted [option] device [command] ,该模式可以直接在命令行下对磁盘进行分区操作，比较适合编程应用。
* 交互模式：parted [option] device 类似于使用fdisk /dev/xxx
* MBR：MBR分区表(即主引导记录)大家都很熟悉。所支持的最大卷：2T，而且对分区有限制：最多4个主分区或3个主分区加一个扩展分区
* GPT： GPT（即GUID分区表）。是源自EFI标准的一种较新的磁盘分区表结构的标准，是未来磁盘分区的主要形式。与MBR分区方式相比，具有如下优点。突破MBR 4个主分区限制，每个磁盘最多支持128个分区。支持大于2T的分区，最大卷可达18EB。


parted是一个可以分区并进行分区调整的工具，他可以创建，破坏，移动，复制，调整`ext2 linux-swap fat fat32 reiserfs`类型的分区，可以创建，调整，移动`Macintosh`的HFS分区，检测`jfs，ntfs，ufs，xfs`分区。

使用方法：`parted [options] [device [command [options...]...]]`

```
options
-h  显示帮助信息
-l  显示所有块设备上的分区
device 对哪个块设备进行操作，如果没有指定则使用第一个块设备
command [options...]

check partition  对分区做一个简单的检测

cp [source-device] source dest  复制source-device设备上的source分区到当前设备的dest分区

mklabel label-type 创建新分区表类型，label-type可以是："bsd", "dvh", "gpt",  "loop","mac", "msdos", "pc98", or "sun" 一般的pc机都是msdos格式，如果分区大于2T则需要选用gpt格式的分区表。

mkfs partition fs-type   在partition分区上创建一个fs-type文件系统，fs-type可以是："fat16", "fat32", "ext2", "linux-swap","reiserfs" 注意不支持ext3格式的文件系统，只能先分区然后用专有命令进行格式化。

mkpart part-type [fs-type] start end  创建一个part-type类型的分区，part-type可以是："primary", "logical", or "extended" 如果指定fs-type则在创建分区的同时进行格式化。start和end指的是分区的起始位置，单位默认是M。

eg：
mkpart  primary  0  -1   0表示分区的开始  -1表示分区的结尾  意思是划分整个硬盘空间为主分区
mkpartfs part-type fs-type start end 创建一个fs-type类型的part-type分区，不推荐使用，最好是使用mkpart分区完成后使用mke2fs进行格式化。
name partition name 给分区设置一个名字，这种设置只能用在Mac, PC98, and GPT类型的分区表，设置时名字用引号括起来
select device 在机器上有多个硬盘时，选择操作那个硬盘
resize partition start end  调整分区大小
rm partition  删除一个分区
rescue start end  拯救一个位于stat和end之间的分区
unit unit 在前面分区时，默认分区时数值的单位是M，这个参数卡伊改变默认单位，"kB", "MB",  "GB",  "TB"
move partition start end 移动partition分区
print  显示分区表信息  
quit 退出parted
```

### 实战演练

#### 初始磁盘信息
服务器新增3块4TB硬盘
```
fdisk -l                                                                                                                             

Disk /dev/sdd: 4000.8 GB, 4000787030016 bytes
255 heads, 63 sectors/track, 486401 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/sdb: 4000.8 GB, 4000787030016 bytes
255 heads, 63 sectors/track, 486401 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/sdc: 4000.8 GB, 4000787030016 bytes
255 heads, 63 sectors/track, 486401 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/sda: 146.8 GB, 146815733760 bytes
255 heads, 63 sectors/track, 17849 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000081

Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1          26      204800   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2              26         548     4194304   82  Linux swap / Solaris
Partition 2 does not end on cylinder boundary.
/dev/sda3             548        1070     4194304   83  Linux
/dev/sda4            1070       17850   134780308    5  Extended
/dev/sda5            1071       17850   134778880   83  Linux
```
#### 尝试通过fdisk命令进行分区
```
fdisk /dev/sdb
Device contains neither a valid DOS partition table, nor Sun, SGI or OSF disklabel
Building a new DOS disklabel with disk identifier 0x6001e0a2.
Changes will remain in memory only, until you decide to write them.
After that, of course, the previous content won't be recoverable.

Warning: invalid flag 0x0000 of partition table 4 will be corrected by w(rite)

WARNING: The size of this disk is 4.0 TB (4000787030016 bytes).
DOS partition table format can not be used on drives for volumes
larger than (2199023255040 bytes) for 512-byte sectors. Use parted(1) and GUID
partition table format (GPT).


WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
         switch off the mode (command 'c') and change display units to
         sectors (command 'u')
```
fdisk 命令无法对大于2TB以上的硬盘进行分区

### 通过parted命令进行分区

##### 更改分区表类型
```
parted -s /dev/sdb mklabel gpt
parted -s /dev/sdc mklabel gpt
parted -s /dev/sdd mklabel gpt
```
##### 磁盘分区
```
parted /dev/sdb 'mkpart primary 0 -1'
parted /dev/sdc 'mkpart primary 0 -1'
parted /dev/sdd 'mkpart primary 0 -1'
```

##### 格式化分区
```
mkfs.ext4 -q /dev/sdb1
mkfs.ext4 -q /dev/sdc1
mkfs.ext4 -q /dev/sdd1
```

#### 挂载目录
```
mkdir /MFS_DATA1; mount /dev/sdb1 /MFS_DATA1;echo "mount /dev/sdb1 /MFS_DATA1" >> /etc/rc.local
mkdir /MFS_DATA2; mount /dev/sdc1 /MFS_DATA2;echo "mount /dev/sdc1 /MFS_DATA2" >> /etc/rc.local
mkdir /MFS_DATA3; mount /dev/sdd1 /MFS_DATA3;echo "mount /dev/sdd1 /MFS_DATA3" >> /etc/rc.local
```

#### 查看磁盘挂载
```
df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda5       127G  1.1G  120G   1% /
tmpfs           7.8G   12K  7.8G   1% /dev/shm
/dev/sda1       194M   29M  155M  16% /boot
/dev/sda3       4.0G  254M  3.5G   7% /var
/dev/sdb1       3.6T  196M  3.4T   1% /MFS_DATA1
/dev/sdc1       3.6T  196M  3.4T   1% /MFS_DATA2
/dev/sdd1       3.6T  196M  3.4T   1% /MFS_DATA3
```
