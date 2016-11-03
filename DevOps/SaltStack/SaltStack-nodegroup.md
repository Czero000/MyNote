# Nodegroup
为了便于管理功能相似的minion，SaltStack提供了分组模式，官方文档：http://docs.saltstack.com/en/latest/topics/targeting/nodegroups.html
Node group为预先在master配置文件中定义的minion组，用来进行批量对minion操作。在master配置文件中，删除`default_include: master.d/*.conf`注释。

- 编辑配置文件： /etc/salt/master.d/nodegroup.conf

```
#####         Node Groups           #####
##########################################
# Node groups allow for logical groupings of minion nodes. A group consists of a group
# name and a compound target.
nodegroups:
  minion: '172.16.11.211'
```

- 重启master

测试通过-N参数在命令行指定运行的节点组：
```
salt -N minion test.ping
172.16.11.211:
    True
```

- 在top file中增加组分类

```
base:
  minion:
    - match: nodegroup
    - apache
    - ssh
```

![nodegroup](http://ofc9x1ccn.bkt.clouddn.com/saltstack/nodegroup.png)
