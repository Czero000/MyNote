title: binlog日志清理
date: 2016/12/09 11:35:50
updated: 2016/12/09 11:35:50
categories:
- DataBases
- MySQL
---
# 日志清理

方法如下
```
PURGE {MASTER | BINARY} LOGS TO 'log_name'
PURGE {MASTER | BINARY} LOGS BEFORE 'date'
```
用于删除列于在指定的日志或日期之前的日志索引中的所有二进制日志。这些日志也会从记录在日志索引文件中的清单中被删除，这样被给定的日志成为第一个。
例如：
```
PURGE MASTER LOGS TO 'mysql-bin.010';
PURGE MASTER LOGS BEFORE '2008-06-23 15:00:00';
```

## 清除3天前的 binlog
```
PURGE MASTER LOGS BEFORE DATE_SUB( NOW( ), INTERVAL 3 DAY);
```
BEFORE变量的date自变量可以为'YYYY-MM-DD hh:mm:ss'格式。MASTER和BINARY是同义词。

 如果您有一个活性的从属服务器，该服务器当前正在读取您正在试图删除的日志之一，则本语句不会起作用，而是会失败，并伴随一个错误。不过，如果从属服
务器是休止的，并且您碰巧清理了其想要读取的日志之一，则从属服务器启动后不能复制。当从属服务器正在复制时，本语句可以安全运行。您不需要停止它们。

##  要清理日志，需按照以下步骤：
1. 在每个从属服务器上，使用SHOW SLAVE STATUS来检查它正在读取哪个日志。
2. 使用SHOW MASTER LOGS获得主服务器上的一系列日志。
3. 在所有的从属服务器中判定最早的日志。这个是目标日志。如果所有的从属服务器是更新的，这是清单上的最后一个日志。
4. 制作您将要删除的所有日志的备份。（这个步骤是自选的，但是建议采用。）
5. 清理所有的日志，但是不包括目标日志,因为从服务器还要跟它同步
