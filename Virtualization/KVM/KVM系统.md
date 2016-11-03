[TOC]

# 什么是虚拟化

虚拟化，是指通过虚拟化技术将一台计算机虚拟为多台逻辑计算机。在一台计算机上同时运行多个逻辑计算机，每个逻辑计算机可运行不同的操作系统，并且应用程序都可以在相互独立的空间内运行而互不影响，从而显著提高计算机的工作效率。虚拟化使用软件的方法重新定义划分IT资源，可以实现IT资源的动态分配、灵活调度、跨域共享，提高IT资源利用率，使IT资源能够真正成为社会基础设施，服务于各行各业中灵活多变的应用需求。

---

## 虚拟化定义

虚拟化的广义与狭义的理解

广义——将不存在的食物或现象“虚拟”成为存在的事物或现象的方法，计算机科学中的虚拟化包括平台虚拟化、应用程序虚拟化、存储虚拟化、网络虚拟化、设备虚拟化等。

狭义——指在计算机上模拟运行多个操作系统平台。

目前对于虚拟化-Virtualization并没有统一的标准定义，但大多数定义都包含这样几个方面，

1. 虚拟的内容是资源（包括CPU、内存、存储、网络等）；
2. 被虚拟的物理资源有着统一的逻辑表示，而且这种逻辑表示提供给用户大部分相同或完全相同的物理资源的功能；
3. 经过一系列的虚拟化过程，使得资源不受物理限制约束，由此可以带给我们与传统IT相比更多的优势——资源整合、提高资源利用率、动态IT等；

解虚拟化既是对资源的逻辑抽象、隔离、再分配、管理的一个过程。所有虚拟化厂商所宣传的各种功能特色，都可以归结为逻辑抽象、隔离、再分配、管理这四个过程中。

---

## 虚拟化分类

虚拟化的方式多种多样，耳朵很熟悉的一些名字有：全虚拟化，类虚拟化，硬件虚拟化，混合虚拟化等等。这些不同的虚拟化方式，并不是根据同一个标准来分类的，以下介绍三种主要的分类方法，并相应介绍一些目前主流的虚拟化实现方式，以及对应的产品。

### 从虚拟平台的角度来划分的话，主要分为全虚拟化和类虚拟化

- 全虚拟化是指VMM虚拟出来的平台是现实中存在的平台，因此对于客户机来说，并不知道自己是运行在虚拟的平台上。正因为此，全虚拟化中的客户机操作系统是不需要做任何修改的。


- 类虚拟化是指通过对客户机进行源码级的修改，让客户机可以使用虚拟化的资源。由于需要修改客户机内核，因此类虚拟化一般都会被顺便用来优化I/O，客户机的操作系统通过高度优化的I/O协议，可以和VMM紧密结合达到近似于物理机的速度。

**对于全虚拟化来说，从虚拟化支持的层次划分，主要分为软件辅助的虚拟化和硬件支持的虚拟化：**

- 软件辅助的虚拟化是指通过软件的方法，让客户机的特权指令陷入异常，从而触发宿主机进行虚拟化处理。主要使用的技术是优先级压缩和二进制代码翻译。
  - 优先级压缩是指让客户机运行在Ring 1级别，由于处于非特权级别，所以客户机的指令基本上都会触发异常，然后宿主机进行接管。
  - 但是有些指令并不能触发异常，因此就需要二进制代码翻译技术来对客户机中无法触发异常的指令进行转换，使之无法逃出宿主机的控制。
  - 通过软件级的全虚拟化，可以让一台x86的物理机运行64位操作系统。更有胜者，通过IA64机型模拟古老的Mainframe虚拟机，从而把Mainframe机器的系统迁移至新机型中。


- 硬件辅助的虚拟化主要是由于在技术层面上用软件手段达到全虚拟化非常麻烦，而且效率较低，才由Intel等处理器厂商直接在芯片上提供了对虚拟化的支持。硬件直接可以对敏感指令进行虚拟化执行。比如Intel的VT-x技术。

**从实现结构来看，主要分为Hypervisor型虚拟，宿主模型虚拟，混合模型虚拟：**

- Hypervisor虚拟是指，硬件资源之上没有操作系统，而是直接由VMM作为Hypervisor接管，Hypervisor负责管理所有资源和虚拟环境支持。这种结构的主要问题是，硬件设备多种多样，VMM不可能把每种设备的驱动都一一实现，所以此模型支持有限的设备。目前主要的产品是VMware EX Server，是当前最高端和成熟的虚拟化产品。
- 宿主模型，是在硬件资源之上有个普通的操作系统，负责管理硬件设备，然后VMM作为一个应用搭建在宿主OS上负责虚拟环境的支持，在VMM之上再加载客户机。此方式由底层操作系统对设备进行管理，因此VMM完全不用操心实现设备驱动。而它的主要缺点VMM对硬件资源的调用依赖宿主机，因此效率和功能受宿主机影响较大。目前主要产品是VMware Server，Virtual PC/Server。
- 混合模型，是综合了以上两种实现模型的虚拟化技术。首先VMM直接管理硬件，但是它会让出一部分对设备的控制权，交给运行在特权虚拟机中的特权操作系统来管理（称之为Domain 0）。VMM和Domain 0合作搭建起虚拟环境，在其上运行客户虚拟机(Domain N)。这个模型还是具有一些缺点，由于在需要特权操作系统提供服务时，就会出现上下文切换，这部分的开销会造成性能的下降。目前主要产品有Windows 2008， Xen。

---

## 虚拟化软件介绍

- RedHat KVM

虚拟化方式：完全虚拟化
架构：寄居架构（linux内核）;祼金属架构RHEV-H
特点：祼金属架构RHEV-H或在关键的硬盘和网卡上支持半虚拟化VirtIO，达到最佳性能。
I/O协议栈：KVM重用了整个Linux I/O协议栈，所以KVM的用户就自然就获得了最新的驱动和I/O协议栈的改进。

 ![kvm-vt](http://ofc9x1ccn.bkt.clouddn.com/kvm/kvm-vt.png)

- VmWare ESX

虚拟化方式：完全虚拟化
架构：裸金属架构
I/O协议栈：VMware选择性能，但是把I/O协议栈放到了hypervisor里面。不幸的是，VMware kernel是专有的，那就意味着VMware不得不开发和维护整个协议栈，会导致开发速度会减慢，你的硬件可能要等一段时间才会得到VMware的支持。

 ![vmware-vt](http://ofc9x1ccn.bkt.clouddn.com/kvm/vmware-vt.png)

- Citrix XenServer

虚拟化方式：半虚拟化(linux安装linux);全虚拟化(linux安装windows),硬件辅助虚拟化
架构：裸金属架构
I/O协议栈：Xen选择了可维护这条道路，它将所有的I/O操作放到了Linux guest里面，也就是所谓的domain-0里面。重用Linux来做I/O, Xen的维护者就不用重写整个I/O协议栈了。但不幸的是，这样就牺牲了性能：每一个中断都必需经过Xen的调度，才能切换到domain 0, 并且所有的东西都不得不经过一个附加层的映射。

 ![xen-vt](http://ofc9x1ccn.bkt.clouddn.com/kvm/xen-vt.png)

- Microsoft Hyper-V

虚拟化方式：半虚拟化
架构：裸金属架构Hyper-V Server;寄居架构 Windows 2008
特点：父分区（宿主机操作系统）的位置挪到了子分区（虚拟机操作系统）的旁边，宿主机操作系统和虚拟机操作系统是平级的，没有谁依附谁之上的关系。
I/O协议栈：虚拟机看到的所有设备不再都是虚拟出来的，有部分的硬件资源是真实的物理设备。

 ![hyper-vt](http://ofc9x1ccn.bkt.clouddn.com/kvm/hyper-vt.png)

---

# 安装kvm虚拟机

## 系统要求
KVM 需要有CPU的支持(Intel VT 或 AMD SVM)，在安装 KVM 之前检查一下 CPU 是否提供了虚拟技术的支持

* 基于`Intel`处理器的系统，运行`grep vmx /proc/cpuinfo`查找 CPU flags 是否包括`vmx`关键词
* 基于`AMD`处理器的系统，运行`grep svm /proc/cpuinfo`查找 CPU flags 是否包括`svm`关键词
* 检查BIOS，确保BIOS里开启`VT`选项

**注:**

* 一些厂商禁止了机器 BIOS 中的 VT 选项 , 这种方式下 VT 不能被重新打开

* /proc/cpuinfo 仅从 Linux 2.6.15(Intel) 和 Linux 2.6.16(AMD) 开始显示虚拟化方面的信息。请使用 uname -r 命令查询您的内核版本。如有疑问，请联系硬件厂商

```
egrep "(vmx|svm)" /proc/cpuinfo
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 popcnt lahf_lm dts tpr_shadow vnmi flexpriority ept vpid
```

## 安装kvm软件
- 安装KVM模块、管理工具和libvirt (一个创建虚拟机的工具)
```
yum install -y qemu-kvm libvirt virt-install virt-manager bridge-utils
/etc/init.d/libvirtd start
chkconfig libvirtd on
```

- 确保正确加载kvm模块
```
lsmod  | grep kvm
kvm_intel              54285  0 
kvm                   333172  1 kvm_intel
```

- 检查kvm是否正确安装
```
virsh -c qemu:///system list
Id    Name                           State
```

如果这里是错误信息，说明安装出现问题

----------------------------------------------------


## 配置网络
kvm上网有两种配置，一种是default，它支持主机和虚拟机的互访，同时也支持虚拟机访问互联网，但不支持外界访问虚拟机，另外一种是bridge方式，可以使虚拟机成为网络中具有独立Ip的主机。

- 默认网络virbro

默认的网络连接是virbr0，它的配置文件在/var/lib/libvirt/network目录下，默认配置为

```
cat /var/lib/libvirt/network/default.xml 

default
77094b31-b7eb-46ca-930e-e0be9715a5ce
```

- 桥接网络

配置桥接网卡，配置如下：
```
more /etc/sysconfig/network-scripts/ifcfg-*
::::::::::::::
/etc/sysconfig/network-scripts/ifcfg-br0
::::::::::::::
DEVICE=br0
ONBOOT=yes
TYPE=Bridge
BOOTPROTO=static
IPADDR=192.168.39.20
NETMASK=255.255.255.0
GATEWAY=192.168.39.1
DNS1=8.8.8.8
::::::::::::::
/etc/sysconfig/network-scripts/ifcfg-br1
::::::::::::::
DEVICE=br1
ONBOOT=yes
TYPE=Bridge
BOOTPROTO=static
IPADDR=10.10.39.8
NETMASK=255.255.255.0
::::::::::::::
/etc/sysconfig/network-scripts/ifcfg-em1
::::::::::::::
DEVICE=em1
TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=static
BRIDGE=br0
::::::::::::::
/etc/sysconfig/network-scripts/ifcfg-em2
::::::::::::::
DEVICE=em2
TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=static
BRIDGE=br1
```

## 使用virt-manager安装建立虚拟机
virt-manager 是基于 libvirt 的图像化虚拟机管理软件，操作类似vmware，不做详细介绍。

---

# 通过virsh命令管理虚拟机

libvirt有两种控制方式，命令行和图形界面。 有两种控制方式，命令行和图形界面。

- 图形界面：通过执行名 图形界面：通过执行命令`virt-manager` ，启动`libvirt`  的图形界面，在图形界面下就可以一步一步的创建虚拟机，管理还直接控制桌面。
- 下面介绍如果用命令行控制虚拟机

## 创建虚拟机

在`/etc/libvirt/qemu`下新建`*.xml`文件，如`node.xml`。需要有内存、cpu、硬盘设置、光驱以及 vnc等等。

```xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh edit JCPT-Serverlist-54-127
or other application using the libvirt API.
-->

<domain type='kvm'>
  <name>JCPT-Serverlist-54-127</name>
  <uuid>be97ad3b-6d06-4f8d-8603-d0419e28d47d</uuid>
  <memory unit='KiB'>4194304</memory>
  <currentMemory unit='KiB'>4194304</currentMemory>
  <vcpu placement='static'>4</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/opt/vmx/gv0/instance/JCPT/JCPT-Serverlist-54-127.img'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </disk>
    <controller type='usb' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>
    </controller>
    <controller type='pci' index='0' model='pci-root'/>
    <controller type='ide' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
    </controller>
    <interface type='bridge'>
      <mac address='52:54:56:38:83:44'/>
      <source bridge='br1'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
    <interface type='bridge'>
      <mac address='52:54:00:e1:72:8b'/>
      <source bridge='br210'/>
      <model type='e1000'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </interface>
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <input type='tablet' bus='usb'/>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='vnc' port='5912' autoport='no' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
    <video>
      <model type='cirrus' vram='16384' heads='1'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </memballoon>
  </devices>
</domain>
```

---

## 代码分析

```
//kvm guest 定义开始
<domain type='kvm'>

//guest的short name。由字母和数字组成，不能包含空格
<name>JCPT-Serverlist-54-127</name>

//uuid，由命令行工具 uuidgen生成。
<uuid>e5fff551-bbe1-e748-c8e4-8ecb3bffb902</uuid>

//在不reboot guest的情况下，guset可以使用的最大内存，以KB为单位
<memory>1048576</memory>

//guest启动时内存，可以通过virsh setmem来调整内存，但不能大于最大可使用内存。
<currentMemory>1048576</currentMemory>

//分配的虚拟cpu
<vcpu>4</vcpu>

//有关OS
架构：i686、x86_64
machine：宿主机的操作系统
boot:指定启动设备，可以重复多行，指定不同的值，作为一个启动设备列表。
<os>
<type arch='x86_64' machine='rhel6.0.0'>hvm</type>
<boot dev='hd'/>
</os>

//处理器特性
<features>
<acpi/>
<apic/>
<pae/>
</features>

//时钟。使用本地时间：localtime
<clock offset='localtime'/>

//定义了在kvm环境中power off，reboot，或crash时的默认的动作分别为destroy和restart。其他允许的动作包括： preserve，rename-restart.。
destroy：停止该虚拟机。相当于关闭电源。
restart重启虚拟机。
<on_poweroff>destroy</on_poweroff>
<on_reboot>restart</on_reboot>
<on_crash>restart</on_crash>

//设备定义开始
<devices>

//模拟元素，此处写法用于kvm的guest
<emulator>/usr/libexec/qemu-kvm</emulator>

//用于kvm存储的文件。在这个例子中，在guest中显示为IDE设备。使用qemu-img命令创建该文件，kvm image的默认目录为：/var/lib/libvirt/images/
<disk type='file' device='disk'>
<driver name='qemu' type='raw' cache='none'/>
<source file='/home/kvm/images/dcs01.img'/>
<target dev='hda' bus='ide'/>
<address type='drive' controller='0' bus='0' unit='0'/>
</disk>

//补充：可以定义多个磁盘。
使用virtio：
采用普通的驱动，即硬盘和网卡都采用默认配置情况下，网卡工作在 模拟的rtl 8139 网卡下，速度为100M 全双工。采用 virtio 驱动后，网卡工作在 1000M 的模式下。采用普通的驱动，即硬盘和网卡都采用默认配置情况下，硬盘是 ide 模式。采用 virtio 驱动后，硬盘工作是SCSI模式下。
<disk type='file' device='disk'>
<driver name='qemu' type='raw'/>
<source file='/usr/local/kvm/vmsample/disk.os'/>
<target dev='vda' bus='virtio'/>
</disk>

　　CD-ROM device：
<disk type='file' device='cdrom'>
<driver name='qemu' type='raw'/>
<target dev='hdc' bus='ide'/>
<readonly/>
<address type='drive' controller='0' bus='1' unit='0'/>
</disk>

//使用网桥类型。确保每个kvm guest的mac地址唯一。将创建tun设备，名称为vnetx（x为0,1,2...）
<interface type='bridge'>
<mac address='52:54:00:ad:75:98'/>
<source bridge='br0'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
补充：
使用默认的虚拟网络代替网桥，即guest为NAT模式。也可以省略mac地址元素，这样将自动生成mac地址。
<interface type='network'>
<source network='default'/>
<mac address="3B:6E:01:69:3A:11"/>
</interface>
默认分配192.168.122.x/24的地址，也可以手动指定。网关为192.168.122.1

　　使用virtio：
采用普通的驱动，即硬盘和网卡都采用默认配置情况下，网卡工作在 模拟的rtl 8139 网卡下，速度为100M 全双工。采用 virtio 驱动后，网卡工作在 1000M 的模式下。
<interface type='bridge'>
<source bridge='br1'/>
<model type='virtio' />
</interface>

//输入设备
<input type='tablet' bus='usb'/>
<input type='mouse' bus='ps2'/>

//定义与guset交互的图形设备。在这个例子中，使用vnc协议。listen的地址为host的地址。prot为-1，表示自动分配端口号，通过以下的命令查找端口号：
virsh vncdisplay <KVM Guest Name>

这里未设置
<graphics type='vnc' port='-1' autoport='yes'/>

//设备定义结束
</devices>

//KVM定义结束
</domain>
```



## 其他virsh命令

- kvm虚拟机配置文件位置：`/etc/libvirt/qemu`
- autostart目录配置是kvm虚拟机开机自启动目录


- 查看kvm虚拟机状态

```
virsh list -all
```

- 启动虚拟机

```
virsh start node
```

- 虚拟机关机或者断电

```
//关机，默认情况下virsh工具不能对linux虚拟机进行关机操作，linux操作系统需要开启与启动acpid服务。在安装KVM linux虚拟机必须配置此服务。
virsh shutdown node

//强制关机
virsh destroy node
```

- 通过配置文件启动虚拟机

```
virsh create /etc/libvirt/qemu/node.xml
```

- 配置开机自启动虚拟机

```
virsh autostart node
```

- 导出kvm虚拟机配置文件

```
virsh dumpxml node > /etc/libvirt/qemu/node01.xml
```

- 添加和删除虚拟机

```
// 删除kvm虚拟机，该命令只是删除node的配置文件，并不删除磁盘文件
virsh undefine node
// 通过配置文件定义虚拟机
virsh define /etc/libvirt/qemu/node.xml
```

- 编辑kvm虚拟机配置文件

```
virsh edit node
```

- 挂起修复服务器

```
virsh suspend node
virsh resume node
```
