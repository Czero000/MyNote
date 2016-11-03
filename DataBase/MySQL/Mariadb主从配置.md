# 概述
由于Oracle收购Sun公司后，MySQL越来越走向封闭，对Sun公司原有的开源项目处置方式都让人担忧，主流Linux发行版和大的组织机构、公司都转移到MariaDB上来，例如：Red Hat, Google, Wikipedia, Mozilla等，MariaDB相对MySQL也有很多改进，对MySQL也是兼容的，故推荐使用MariaDB。系统环境采用Ubuntu16.04_LTS

# 主从复制原理
MySQL的主从复制是指从服务器向主服务器获取二进制日志文件，然后在从服务器上对这些日志重新执行，从而使从服务器和主服务器保持同步。但由于是异步的复制，从服务器在一定程度上落后于主服务器，刚写入到主服务器上的数据可能服务在从服务器上查询得到。
![replication](http://ofc9x1ccn.bkt.clouddn.com/mysql/replication.gif)

## mysql支持的复制类型
- statement 基于语句的复制：在主服务器上执行的SQL语句，在从服务器上执行同样的语句。MySQL默认采用基于语句的复制，效率比较高。一旦发现没法精确复制时，会自动选着基于行的复制。
- row 基于行的复制：把改变的内容复制过去，而不是把命令在从服务器上执行一遍. 从mysql5.0开始支持
- mixed 混合类型的复制: 默认采用基于语句的复制，一旦发现基于语句的无法精确的复制时，就会采用基于行的复制。

statement格式仅仅是记录操作的SQL语句，row格式会将每行数据的变化都记录到binlog中，相对于statement要详细的多，更能够保证主从数据库的一致性。但是row格式下的二进制日志文件会显得非常庞大，会影响磁盘I/O，在传输过程中也会影响带宽，所以需要根据具体情况来设定

- 整体上来说，复制有3个步骤：
  - master将改变记录到二进制日志(binary log)中（这些记录叫做二进制日志事件，binary log events）
  - slave将master的binary log events拷贝到它的中继日志(relay log)；
  - slave重做中继日志中的事件，将改变反映它自己的数据。
  - 也就是说，总共有三个线程被启动来做主从复制，主服务器一个线程，从服务器两个线程

- 第一部分就是master记录二进制日志。在每个事务更新数据完成之前，master在二日志记录这些改变。MySQL将事务串行的写入二进制日志，即使事务中的语句都是交叉执行的。在事件写入二进制日志完成后，master通知存储引擎提交事务。
- 下一步就是slave将master的binary log拷贝到它自己的中继日志。首先，slave开始一个工作线程——I/O线程。I/O线程在master上打开一个普通的连接，然后开始binlog dump process。Binlog dump process从master的二进制日志中读取事件，如果已经跟上master，它会睡眠并等待master产生新的事件。I/O线程将这些事件写入中继日志。
- SQL slave thread（SQL从线程）处理该过程的最后一步。SQL线程从中继日志读取事件，并重放其中的事件而更新slave的数据，使其与master中的数据一致。只要该线程与I/O线程保持一致，中继日志通常会位于OS的缓存中，所以中继日志的开销很小。

在一个非常繁忙的数据库上，主库上往往有多个线程并发执行写操作，而这些事件记录到二进制日志中一定是线性的。从库上只有一个SQL线程执行写操作，长此以往，从库与主库的差距会越来越大。这种情况下在从库上可以启动多个SQL线程用于执行写操作，每个线程负责执行主库上某个数据库的所有相关事务。还有在主库上一个事务提交之后，相关的记录不会立刻同步到磁盘上，而是记录在缓冲上，每隔一段时间同步一次。这样也可能会导致主从不一致，可以在主服务器上设置参数sync_binlog=1，一但事务提交，就将二进制日志文件从内存缓冲同步至磁盘上
# 主从复制搭建

## 环境说明
- 主数据库： 172.16.8.140， Ubuntu16.04_LTS, mariadb-10.1.14.
- 从数据库： 172.16.8.144, Ubuntu16.04_LTS, mariadb-10.1.14.

## 配置文件
确保主服务器配置文件中包含下面内容

- 主数据库
```
[mysqld]
log-bin=mysql-bin
binlog_format=mixed
server-id       = 1
sync_binlog     = 1
```

- 从数据库
```
server-id       = 2
relay_log_purge = 0
read_only       = 1
slave_parallel_threads = 3
binlog-ignore-db=mysql
binlog-ignore-db=test
binlog-ignore-db=information_schema
binlog-ignore-db=performance_schema
relay_log =mysql-relay-bin
relay_log_index =mysql-relay-bin.index
log-slave-updates
```

## 启动服务
```
/etc/init.d/mysqld start
```

## 增加授权
```
//主数据库
GRANT replication slave, replication client ON *.* TO 'repluser'@'172.16.8.144' identified by 'replpasswd';      
//从数据库检查授权情况
/usr/local/mysql/data# mysql -urepluser -h172.16.8.140 -p
```

## 配置主从

- 主数据库
```
MariaDB [(none)]> show master status;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000004 |      851 |              |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.00 sec)
```

- 从数据库
首先查看主服务器二进制日志所处的位置（show master status;）,如果服务器已经运行了一段时间，可以先对主服务器进行备份（备份至某个位置），在从服务器上恢复，再从该位置进行同步。
```
change master to master_host='172.16.8.140',master_port=3306,master_user='repluser',master_password='replpasswd',master_log_file='mysql-bin.000004',master_log_pos=851;  
Query OK, 0 rows affected (0.03 sec)
```
注：host、port、user、password、log_file、log_pos等需要根据实际master信息

## 启动启动IO线程和sql线程
```
MariaDB [(none)]> start slave;
MariaDB [(none)]> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 172.16.8.140
                  Master_User: repluser
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000004
          Read_Master_Log_Pos: 851
               Relay_Log_File: mysql-relay-bin.000004
                Relay_Log_Pos: 537
        Relay_Master_Log_File: mysql-bin.000004
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 851
              Relay_Log_Space: 1689
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
               Master_SSL_Crl:
           Master_SSL_Crlpath:
                   Using_Gtid: No
                  Gtid_IO_Pos:
      Replicate_Do_Domain_Ids:
  Replicate_Ignore_Domain_Ids:
                Parallel_Mode: conservative
1 row in set (0.00 sec)
```
# 查看master和slave节点状态
```
show processlist;
+----+----------+--------------------+------+-------------+------+-----------------------------------------------------------------------+------------------+----------+
| Id | User     | Host               | db   | Command     | Time | State                                                                 | Info             | Progress |
+----+----------+--------------------+------+-------------+------+-----------------------------------------------------------------------+------------------+----------+
| 12 | root     | localhost          | NULL | Query       |    0 | init                                                                  | show processlist |    0.000 |
| 15 | repluser | 172.16.8.144:57508 | NULL | Binlog Dump |  265 | Master has sent all binlog to slave; waiting for binlog to be updated | NULL             |    0.000 |
+----+----------+--------------------+------+-------------+------+-----------------------------------------------------------------------+------------------+----------+
2 rows in set (0.00 sec)
```

# 测试主从同步
在同数据库创建测试库，查看从库是否同步
