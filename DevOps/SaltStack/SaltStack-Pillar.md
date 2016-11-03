## 什么是pillar

Pillar是SaltStack非常重要的一个组件，经常与States配合使用在配置管理中。它用于给特定的minin定义任何你需要的数据，定义存储格式与grains类似，都是用dict结构，使用YAML格式。pillar数据和minion相关联，每个minion只可以看到自己的数据，所以可以用pillar传递敏感数据。pillar可以在以下场景中使用到：

- 敏感数据
  例如ssh key、加密证书、由于Pillar使用独立的加密session，可以确保敏感数据不被其他minion看到
- 变量
  可以在pillar中处理平台差异化，比如针对不同的操作系统设置软件包名称，然后在state中引用
- 其他数据
  可以在pillar中添加任意可以使用到的数据，例如定义用户和UID的关系、minion角色
- Targetting
  可以用来选择minion，使用-I参数
  默认master配置文件中的所有数据到添加到pillar中，且对所有minion可用。如果要禁用，可以在修改master配置文件`#pillar_opts: True `

---
## 使用配置pillar

### 创建pillar目录
```shell
// 修改master配置文件，定义pillar工作目录
pillar_roots:
  base:
    - /srv/pillar

// 创建工作目录
mkdir /srv/pillar

//创建top.sls入口文件,用来组织其他pillar文件,可以定义多个环境不同的pillar目录
cat top.sls
base:                        //指定环境
  '*':                       // 引用主机
    - packages               // 引用packages.sls或者packages/init.sls
    - services               // 引用services.sls或者services/init.sls
    - test                   // 引用test.sls或者test/init.sls
dev:
  'os:CentOS'                 //pillar还可以使用其他的匹配方式来选择minion
    - git

// 定义pillar
cat test/init.sls
NAME: zero
ID: 1314
CONTENT: This is a test !!

cat packages/init.sls
{% if grains['os'] == 'CentOS' %}
  apache: httpd
  git: git
{% elif grains['os'] == 'Debian' %}
  apache: apache2
  git: git-core
{& endif &}

```
base环境中所有的minion都具有packages、services、test 中定义的数据。pillar采用与file server相同的文件映射方式。packages映射到文件/srv/pillar/packages/init.sls。services映射到/srv/pillar/services/init.sls。值得注意的是key与value要用冒号分隔，没有空格的话解析会失败。

### 查看定义的pillar
```shell
salt '*' pillar.data
172.16.11.211:
    ----------
    CONTENT:
        This is a test !!
    ID:
        1314
    NAME:
        zero
    http:
        ----------
        package-name:
            httpd
        port:
            80
        user:
            nobody
        version:
            2.4.6


salt '*' saltutil.refresh_pillar  // 在master上修改pillar文件后，需要用命令刷新minion数据
```


### 在pillar中使用列表
pillar的key/value结构中的value可以是string，也可以是一个list。pillar文件定义如下：

```shell
/srv/pillar/users/init.sls:
users:
  zero:  1000
  damon:  1001

在top.sls中引用pillar文件，对所有的minion应用users中的内容：
/srv/pillar/top.sls:
base:
  '*':
    - users

// 现在所有的minion都既有user数据，可以在state文件中使用：
/srv/salt/user/init.sls:
{% for user,uid in pillar.get('users',{}).items() %}
{{user}}:
  user.present:
    - uid: {{uid}}
{% endfor %}
```

### 利用pillar处理平台差异
不同的操作系统不仅管理资源的方式不同，软件包的名字、配置文件的路径也有可能不一样。Salt的执行模块屏蔽了系统管理资源的差异。其他的差异可以根据grains中的os、cpuarch等信息来处理，这些条件判断可以写在state，但会使得state文件的逻辑不清晰。pillar可以很好的解决这些问题。下面的例子中，在不同的os上安装对应的软件包，但是state file完全相同，不需要针对os做修改，灵活方便。
```
/srv/pillar/pkg/init.sls:
packages:
  {% if grains['os_family'] == 'CentOS' %}
    apache: httpd
    vim:  vim-enhanced
  {% elif grains['os_family'] == 'Debian' %}
    apache: apache2
    vim:  vim
  (% elif grains['os'] == 'arch' %)
    apache: apache
    vim: vim
  {& endif &}
/srv/pillar/top.sls：
base:'*':- data
    - users
    - pkg    
/srv/salt/apache/init.sls：

apache:
  pkg.installed:- name: {{ pillar['pkgs']['apache'] }}

// 还可以在state file中设置默认值： srv/salt/apache/init.sls：

apache:
  pkg.installed:- name: {{ salt['pillar.get']('pkgs:apache', 'httpd') }}

```

### Grains 和Pillar区别

在下面的表格中通过多个维度对它们进行对比。



| 名称     | 存储位置    | 数据类型 | 数据采集更新方式                                 | 应用                                       |
| ------ | ------- | ---- | ---------------------------------------- | ---------------------------------------- |
| Grains | Minion端 | 静态数据 | Minion启动时收集，也可以使用saltutil.sync_grains进行刷新。 | 存储Minion基本数据。比如用于匹配Minion，自身数据可以用来做资产管理等。 |
| Pillar | Master端 | 动态数据 | 在Master端定义，指定给对应的Minion。可以使用saltutil.refresh_pillar刷新 | 存储Master指定的数据，只有指定的Minion可以看到。用于敏感数据保存   |
