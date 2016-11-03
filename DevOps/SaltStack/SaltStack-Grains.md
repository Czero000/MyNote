# 什么是Grains
Grains是SaltStack组件中非常重要的组件，在实际使部署配置中会经常使用到grains。Grains与Puppet中facter功能类似，存放minion启动时收集的静态信息，也可以理解为Grains记录每台minion的常用属性，例如CPU、内存、硬盘、网络等，在下次启动minion之前，grains收集的数据不会改变所以称之为静态信息。我们可以通过`grains.items`查看某台或多台minion的grains信息。grains信息是在每台minion在启动时上报到master，在实际应用中，经常会根据实际业务需求，自定义grains，自定义grains方法如下：
- 通过minion配置文件定义
- 通过grains相关模块定义
- 通过python脚本定义

## Grains常用操作

```shell
salt '172.16.11.211' sys.list_functions grains
172.16.11.211:
    - grains.append
    - grains.delval
    - grains.filter_by
    - grains.get
    - grains.get_or_set_hash
    - grains.has_value
    - grains.item
    - grains.items
    - grains.ls
    - grains.remove
    - grains.setval
    - grains.setvals

salt '*' grains.ls   //列出可用的grains    
salt '*' grains.items   //列出所有grains的名称和内容
```

---

## 定义Grains

### 通过minion配置文件
通过文件定义Grains，有三种格式符合YAML格式的

`Key:value`：`os:CentOS`

字典格式:`ip_interfaces: {'lo': ['127.0.0.1'], 'em1': ['172.16.11.211'], em2: []}`

多分行列表：

```shell
osmajorrrelease:
    6
    5
```
修改minion配置文件，将`default_include: minion.d/*.conf`取消注释，并在`/etc/salt/minion.d/`添加grains配置文件

```shell
grains:                  //官方示例
  roles:
    - webserver
    - memcache
  deployment: datacenter4
  cabinet: 13
  cab_u: 14-15
```
重启minion，使自定义grains生效

```shell
salt '172.16.11.211' grains.item roles
172.16.11.211:
    ----------
    roles:
        - webserver
        - memcache
// 可以看到自定义的grainis已经生效
```

### 通过grains模块定义

- 设置自定义granins

```shell
salt '172.16.11.211' grains.append salt 'Hello World'     //自定义granins
172.16.11.211:
    ----------
    salt:
        - Hello World

salt '172.16.11.211' grains.item salt                        // 查看grains
172.16.11.211:
    ----------
    salt:
        - Hello World
```

- 使用Grains.setvals同时设置多个grains

```shell
salt '172.16.11.211' grains.setvals "{'Salt': 'Hello', 'Stack': 'World'}"
172.16.11.211:
    ----------
    Salt:
        Hello
    Stack:
        World
```

- 在_grains目录定义grains

使用默认的master的`file_root配置路径 /srv/salt，那么_grains的位置是/srv/salt/_grains`，添加自定义grains item，注意的是python脚本返回值是一个字典。

```shell
// 脚本内容
def my_grains():
    grains = {'zero' : ['HelloWorld']}
    return grains

//推送_grains内模块到minion
salt '*' saltutil.sync_grains

// 查看新増grains
 salt '*' grains.item zero
172.16.11.211:
    ----------
    zero:
        - HelloWorld
//重新加载模块，刷新grains静态数据
salt '*' sys.reload_modules
```

在minin的`/var/cache/salt/minion/extmods/grains`目录下，可以找到master下发的grains文件

- 删除自定义granins

```
salt '172.16.11.211' grains.remove salt 'Hello SaltStack'
```
