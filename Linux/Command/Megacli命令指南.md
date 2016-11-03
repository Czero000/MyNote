MegaCli是一款管理维护硬件RAID软件，可以通过它来了解当前raid卡的所有信息，包括 raid卡的型号，raid的阵列类型，raid 上各磁盘状态，等等。通常，我们对硬盘当前的状态不太好确定，一般通过机房人员巡检来完成，有没有通过软件的方式来检查确定这个问题呢。MegaCli就可以做到，一般通过 MegaCli 的Media Error Count: 1 Other Error Count: 0 这两个数值来确定阵列中磁盘是否有问题；Medai Error Count 表示磁盘可能错误，可能是磁盘有坏道，这个值不为0值得注意，数值越大，危险系数越高，Other Error Count 表示磁盘可能存在松动，可能需要重新再插入。MegaCli 可以对阵列中所有的磁盘进行检测，我们可以通过脚本的方式来检测相关参数，从而通知管理人员。
       
下载MegCli,目前针对公司DB数据库是IBM的服务器，直接从IBM官方下载，如果其它服务器的，使用各官方下载或者 LSI网站上进行相关下载。一般来说，是通用的。这个包适用32 /64位操作系统平台
 
下载地址：ftp://download2.boulder.ibm.com/ecc/sar/CMA/XSA/ibm_utl_sraidmr_megacli-8.00.48_linux_32-64.zip
       
### 安装
```
unzip ibm_utl_sraidmr_megacli-8.00.48_linux_32-64.zip
cd linux
rpm -ivh Lib_Utils-1.00-09.noarch.rpm  MegaCli-8.00.48-1.i386.rpm
```

### 使用命令及参数
 
#### 命令使用：
* /opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -Lall -aALL 查raid级别
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL 查raid卡信息
* /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL 查看硬盘信息
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -aAll 查看电池信息
* /opt/MegaRAID/MegaCli/MegaCli64 -FwTermLog -Dsply -aALL 查看raid卡日志
* /opt/MegaRAID/MegaCli/MegaCli64 -adpCount 【显示适配器个数】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpGetTime –aALL 【显示适配器时间】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aAll 【显示所有适配器信息】
* /opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -LALL -aAll 【显示所有逻辑磁盘组信息】
* /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aAll 【显示所有的物理信息】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL |grep 'Charger Status' 【查看充电状态】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuStatus -aALL【显示BBU状态信息】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuCapacityInfo -aALL【显示BBU容量信息】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuDesignInfo -aALL 【显示BBU设计参数】
* /opt/MegaRAID/MegaCli/MegaCli64 -AdpBbuCmd -GetBbuProperties -aALL 【显示当前BBU属性】
* /opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL 【显示Raid卡型号，Raid设置，Disk相关信息】
 
#### 磁带状态的变化，从拔盘，到插盘的过程中。
```
Device |Normal|Damage|Rebuild|Normal
Virtual Drive |Optimal|Degraded|Degraded|Optimal
Physical Drive |Online|Failed –> Unconfigured|Rebuild|Online
```

#### 查看磁盘缓存策略
* /opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -Cache -L0 -a0
* /opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -Cache -L1 -a0
* /opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -Cache -LALL -a0
* /opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -Cache -LALL -aALL
* /opt/MegaRAID/MegaCli/MegaCli64 -LDGetProp -DskCache -LALL -aALL

#### 设置磁盘缓存策略
缓存策略解释：

* WT (Write through
* WB (Write back)
* NORA (No read ahead)
* RA (Read ahead)
* ADRA (Adaptive read ahead)
* Cached
* Direct
```
/opt/MegaRAID/MegaCli/MegaCli64 -LDSetProp WT|WB|NORA|RA|ADRA -L0 -a0
/opt/MegaRAID/MegaCli/MegaCli64 -LDSetProp -Cached|-Direct -L0 -a0 enable / disable disk cache
/opt/MegaRAID/MegaCli/MegaCli64 -LDSetProp -EnDskCache|-DisDskCache -L0 -a0
```
#### 创建一个 raid5 阵列，由物理盘 2,3,4 构成，该阵列的热备盘是物理盘 5
```
/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r5 [1:2,1:3,1:4] WB Direct -Hsp[1:5] -a0
```
#### 创建阵列，不指定热备
```
/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r5 [1:2,1:3,1:4] WB Direct -a0
```

#### 删除阵列
```
/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -L1 -a0
```
#### 在线添加磁盘
```
/opt/MegaRAID/MegaCli/MegaCli64 -LDRecon -Start -r5 -Add -PhysDrv[1:4] -L1 -a0
```
#### 阵列创建完后，会有一个初始化同步块的过程，可以看看其进度。

* /opt/MegaRAID/MegaCli/MegaCli64 -LDInit -ShowProg -LALL -aALL 或者以动态可视化文字界面显示
* /opt/MegaRAID/MegaCli/MegaCli64 -LDInit -ProgDsply -LALL -aALL

#### 查看阵列后台初始化进度 
```
/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -ShowProg -LALL -aALL
```

或者以动态可视化文字界面显示
```
/opt/MegaRAID/MegaCli/MegaCli64 -LDBI -ProgDsply -LALL -aALL
```
#### 指定第 5 块盘作为全局热备
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDHSP -Set [-EnclAffinity] [-nonRevertible] -PhysDrv[1:5] -a0
```

#### 指定为某个阵列的专用热备
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDHSP -Set [-Dedicated [-Array1]] [-EnclAffinity] [-nonRevertible] -PhysDrv[1:5] -a0
```

#### 删除全局热备
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDHSP -Rmv -PhysDrv[1:5] -a0
```

#### 将某块物理盘下线/上线
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDOffline -PhysDrv [1:4] -a0
/opt/MegaRAID/MegaCli/MegaCli64 -PDOnline -PhysDrv [1:4] -a0
```

#### 查看物理磁盘重建进度
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDRbld -ShowProg -PhysDrv [1:5] -a0
```
或者以动态可视化文字界面显示
```
/opt/MegaRAID/MegaCli/MegaCli64 -PDRbld -ProgDsply -PhysDrv [1:5] -a0
```

#### 磁带状态的变化，从拔盘，到插盘的过程中：

```
Device |Normal|Damage|Rebuild|Normal
Virtual Drive |Optimal|Degraded|Degraded|Optimal
Physical Drive |Online|Failed –> Unconfigured|Rebuild|Online
```

#### raid 电池设置相关
查看电池状态信息(Display BBU Status Information)
```
MegaCli -AdpBbuCmd -GetBbuStatus -aN|-a0,1,2|-aALL
MegaCli -AdpBbuCmd -GetBbuStatus -aALL
```
查看电池容量（Display BBU Capacity Information）
```
MegaCli -AdpBbuCmd -GetBbuCapacityInfo -aN|-a0,1,2|-aALL
MegaCli -AdpBbuCmd -GetBbuCapacityInfo –aALL
```

查看电池设计参数(Display BBU Design Parameters)
```
MegaCli -AdpBbuCmd -GetBbuDesignInfo -aN|-a0,1,2|-aALL
MegaCli -AdpBbuCmd -GetBbuDesignInfo –aALL
```
 
查看电池属性（Display Current BBU Properties）
```
MegaCli -AdpBbuCmd -GetBbuProperties -aN|-a0,1,2|-aALL
MegaCli -AdpBbuCmd -GetBbuProperties –aALL
```

设置电池为学习模式为循环模式（Start BBU Learning Cycle）
```
Description Starts the learning cycle on the BBU.
No parameter is needed for this option.
MegaCli -AdpBbuCmd -BbuLearn -aN|-a0,1,2|-aALL
```

设置磁盘的缓存模式和访问方式 （Change Virtual Disk Cache and Access Parameters）
```
Description Allows you to change the following virtual disk parameters:
-WT (Write through), WB (Write back): Selects write policy.
-NORA (No read ahead), RA (Read ahead), ADRA (Adaptive read ahead): Selects read policy.
-Cached, -Direct: Selects cache policy.
-RW, -RO, Blocked: Selects access policy.
-EnDskCache: Enables disk cache.
-DisDskCache: Disables disk cache.
MegaCli -LDSetProp { WT | WB|NORA |RA | ADRA|-Cached|Direct} |
{-RW|RO|Blocked} |
{-Name[string]} |
{-EnDskCache|DisDskCache} –Lx |
-L0,1,2|-Lall -aN|-a0,1,2|-aALL
MegaCli -LDSetProp WT -L0 -a0
```

显示磁盘缓存和访问方式（Display Virtual Disk Cache and Access Parameters）
```
MegaCli -LDGetProp -Cache | -Access | -Name | -DskCache -Lx|-L0,1,2|
-Lall -aN|-a0,1,2|-aALL
Displays the cache and access policies of the virtual disk(s):
-WT (Write through), WB (Write back): Selects write policy.
-NORA (No read ahead), RA (Read ahead), ADRA (Adaptive read ahead): Selects read policy.
-Cache, -Cached, Direct: Displays cache policy.
-Access, -RW, -RO, Blocked: Displays access policy.
-DskCache: Displays physical disk cache policy.
```
 
Megaraid 必知必会 使用LSI的megaraid可以对raid进行有效监控。别的厂商比如HP,IBM也有自己的raid API


* MegaCli -ldinfo -lall -aall 查询raid级别，磁盘数量，容量，条带大小
* MegaCli -cfgdsply -aALL |grep Policy 查询控制器cache策略
* MegaCli -LDSetProp WB -L0 -a0 设置write back功能
* MegaCli -LDSetProp CachedBadBBU -L0 -a0 设置即使电池坏了还是保持WB功能
* MegaCli -AdpBbuCmd -BbuLearn a0 手动充电
* MegaCli -FwTermLog -Dsply -aALL 查询日志
* MegaCli -adpCount 显示适配器个数
 
显示所有适配器信息

```
MegaCli -AdpAllInfo -aAll
Critical Disks : 0
Failed Disks : 0
```
 
显示所有逻辑磁盘组信息： `MegaCli -LDInfo -LALL -aAll`
显示所有的物理信息： 
```
MegaCli -PDList -aAll
Media Error Count: 0
Other Error Count: 0
```
 
查看充电状态：
```
MegaCli -AdpBbuCmd -GetBbuStatus -aALL
Learn Cycle Requested : No
Fully Charged : Yes
```
 
显示BBU(后备电池)状态信息： `MegaCli -AdpBbuCmd -GetBbuStatus -aALL`
显示BBU容量信息： `MegaCli -AdpBbuCmd -GetBbuCapacityInfo -aALL`
显示BBU设计参数： `MegaCli -AdpBbuCmd -GetBbuDesignInfo -aALL`
显示当前BBU属性： `MegaCli -AdpBbuCmd -GetBbuProperties -aALL`
显示Raid卡型号，Raid设置，Disk相关信息： `MegaCli -cfgdsply -aALL`
查看Cache 策略设置： `MegaCli -cfgdsply -aALL |grep -i Policy
Current Cache Policy: WriteBack, ReadAheadNone, Direct, Write Cache OK if Bad BBU`
查看充电进度百分比： `MegaCli -AdpBbuCmd -GetBbuStatus -aALL`
 
各种设备和磁盘的不同状态：

```
Device |Normal|Damage|Rebuild|Normal
Virtual Drive |Optimal|Degraded|Degraded|Optimal
Physical Drive |Online|Failed –> Unconfigured|Rebuild|Online
```

#### 通过脚本检测RAID 磁盘状态
Linux下脚本
```
#!/bin/bash
#check raid disk status
MEGACLI="/opt/MegaRAID/MegaCli/MegaCli64 "
$MEGACLI -pdlist -aALL  | grep "Firmware state" | awk -F : '{print $2}' | awk -F , '{print $1}' >/tmp/fireware.log
$MEGACLI -pdlist -aALL  | grep -E "Media Error|Other Error" | awk -F : '{print $2}' >/tmp/disk.log
for i in `cat < /tmp/disk.log`
do
if [ $i -ne 0 ]
        then
curl "http://xxxxxxB&state=ALARM&description=raid_disk_error"
fi
done
for i in `cat < /tmp/fireware.log`
do
if [ $i !=  Online ]
        then
curl "http://xxxxxxstate=ALARM&description=raid_disk_offline"
fi
done
Windows 下脚本
Windows下脚本用的工具是gnu for windows平台的一些软件，如 bash grep awk cat
通过bash直接调用脚本
如：G:\raid_check\unixtools>bash.exe  G:\disk.sh
#check raid disk status
MEGACLI="//G/raid_check/MegaCli.exe"
GREP="//G/raid_check/unixtools/grep.exe"
AWK="//G/raid_check/unixtools/awk.exe"
CAT="//G/raid_check/unixtools/cat.exe"
CURL="//G/raid_check/unixtools/curl.exe"
$MEGACLI -pdlist -aALL  | $GREP "Firmware state" |$AWK -F: '{print $2}' |$AWK -F , '{print $1}' >//c/fireware.log
$MEGACLI -pdlist -aALL  | $GREP -E "Media Error|Other Error" | $AWK -F : '{print $2}' > //c/disk.log
for i in `$CAT c:/disk.log`
do
if [ $i -ne 0 ]
        then
$CURL "http://xxxxxx&description=raid_disk_error"
fi
done
for i in `$CAT c:/fireware.log`
do
if [ $i != Online ]
        then
$CURL "http://xxxxx&state=ALARM&description=raid_disk_offline"
fi
```
