## SaltStack主机定位

### 为什么需要定位主机

作为自动化配置管理工具，首先要解决如何确定特定配置能够准确推送到一个或多个目标主机，否则又何谈自动化大批量主机的分类配置管理。

### SaltStack的target机制

SaltStack建立一套很完善的minion定位机制，叫“target minion‘。通过多种途径，指定minion具有的属性，来区分推送命令或者状态的对应目标。

- globbing （默认匹配方式，linux shell风格的通配）
- Perl-compatible regular expressions （E，正则匹配方式，对象是minion id）
- Lists （L，直接跟一串minion id 列表）
- Grains （G，使用grains值匹配）
- NodeGroup  （N，master配置文件中预定义好的组信息）
- Subnet （S，利用minion的ip属性来进行匹配）
- Range cluster （R，设置ranger服务器反馈值来匹配）
- Pillar （I，用pillar数据匹配）
- Compound （c，复合匹配，用上面一种或多钟方式联合匹配）

```
salt '*' test.ping     
salt \* test.ping       
salt '172.1[1-7].*' test.ping
salt -E '172*' test.ping  
salt -L 'Test01,Test02' test.ping
salt -G 'os:CentOS' test.ping
salt -N 'group1' test.ping
salt -S '172.16.11.0/24' test.ping
salt -I 'key:value' test.ping
salt -C 'E@Test0.* and G@os:CentOS' test.ping
```

### 使用Batch选项进行分批次运行

SaltStack提供了-b 选项，允许对target选中的所有主机分批次进行处理，每次只推送指定的数量或百分比，直至全部推送完毕。

```
salt '*' -b 10 test.ping  //一次10台
salt -G 'os:RedHat' --batch-size 25% test.ping //一次25%
```
