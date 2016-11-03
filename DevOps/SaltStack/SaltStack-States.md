## SaltStack的state

SaltStack使用state模块文件进行配置管理，state使用YAML语法编写，其实它也支持python编写。sls(salt state file)文件为SaltStack state模块的核心，sls文件表示一个系统应处于的系统状态，并且有一个简单的格式设置这些数据，称为配置管理。

- It is all just data
  其实sls文件只是一个数据结构，对于sls文件的深入理解会有助于对salt state的深入理解和应用。sls文件事实上只是一个字典、列表、字符串或者数字。通过对配置进行数据结构化，使其满足开发者的各种需求，写的越多，越易于理解。

- The top file
  所有的state file都可以通过top.sl文件来分配不同的主机使用，这是个整体入口描述，在执行命令的时候，会先检查这个文件，可以看作是基础配置文件

- Default data -yaml
  默认情况下salt表现的数据格式采用最简单的序列化数据格式-YAML，由于不同架构经常使用不同的名称和安装包，apache在红帽系列中是httpd，其他发行版多为apache，salt对于底层服务器管理使用init下的脚本，系统命令名，配置文件等，执行service.get_all函数来获取对应服务器可用的服务名称

---

## 使用state

###  通过命令查看state使用方法
```shell
// 查看所有states列表
salt -N minion' sys.list_state_modules
// 查看指定states的functions
salt -N 'minion' sys.list_state_functions file
//查看指定states的用法
salt -N 'minion' sys.state_doc file
```

### 通过示例了解state

- 安装软件包及启动服务

由于不同架构经常使用不同的名称和安装包，apache在红帽系列中是httpd，其他发行版多为apache，salt对于底层服务器管理使用init下的脚本，系统命令名，配置文件等，执行service.get_all函数来获取对应服务器可用的服务名称


```yaml
httpd:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: httpd
```
这些sls数据确保apache包被安装而且apache服务处于运行状态。
第一行：被称为ID，这个ID是将要执行这些命令的名字
第二行和第四行：用来声明salt state开始的状态，分别使用包管理和服务管理，这个pkg状态管理，通过本地的软件包管理器进行软件安装，service管理系统守护进程
第三行、第五行：是要执行的function，这些函数被定义在pkg和service中，这里标示包会被安装，并且apache守护进行会运行
最后一行：require是一个必要的声明，用来定义状态之剑的依赖，他们保证apache服务安装成功后才会启动apache守护进程
state和方法可以通过点连接起来，上例和下文相同：
```yaml
httpd:
  pkg.installed
  service.running
    - require:
      - pkg: httpd
```

在实际配置管理中，需要编写大量state.sls文件。这些文件会有一个top.sls（非必须）文件作为入口文件，负责指定minion调用某些state.sls文件。

将上面的sls保存为init.sls放置在salt://apache目录下，

```yaml
/srv/salt/
├── apache
│   └── init.sls
└── top.sls
```

- 添加配置文件和用户

​    当建立类似Apache服务器这样的服务时，许多组件需要被安装。apache的配置文件要被管理起来，而且还需要特定的用户和用户

```yaml
httpd:
  pkg:
    - installed
  service:
    - running
    - watch:
      - pkg: httpd
      - file: /etc/httpd/conf/httpd.conf
      - user: apache
  user.present:
    - name: apache
    - uid: 48
    - gid: 48
    - home: /var/www
    - shell: /bin/nologin
    - require:
      - group: apache
  group.present:
    - name: apache
    - gid: 48
    - require:
      - pkg: httpd
/etc/httpd/conf/httpd.conf:
  file.managed:
    - source: salt://apache/httpd.conf
    - user: root
    - group: root
    - mode: 644
```

​    这个例子扩展了上面，其中包括了一个配置文件、一个用户、一个用户组还有一个新的声明：watch。在service中的require换成了watch，从需要一个软件包改成监视3个state（分别是pkg、file、user）。watch语句和require很相似，都能保证被监视或者需要的state在自己之前执行，但是watch还有其他作用。当被监视的state发生变化时，定义watch语句的state与执行自己的watcher函数，当更新软件包、配置文件或者修改apache用户的uid都会触发service state的watcher函数，在本例子中，service state的watcher会重启apache服务。

- 多个sls文件

​    在具有扩展性的SaltStack时，需要不止一个sls，上面的例子中只使用了1个sls文件，多个sls文件可以结合成state tree。sls文件以一定的目录结构分布在master，sls和要发到minion上的文件只是普通文件.

ssh/init.sls

```yaml
::::::::::::::
init.sls
::::::::::::::
include:
  - client
  - server

::::::::::::::
client.sls
::::::::::::::
openssh-clients:
  pkg.installed
/etc/ssh/ssh_config:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - source: salt://ssh/files/ssh_config
    - require:
      - pkg: openssh-clients
      
::::::::::::::
server.sls
::::::::::::::
include:
  - ssh
openssh-server:
  pkg.installed
sshd:
  service.running:
    - require:
      - pkg: openssh-clients
      - pkg: openssh-server
      - file: /etc/ssh/sshd_config
/etc/ssh/sshd_config:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - source: salt://ssh/files/sshd_config
    - require:
      - pkg: openssh-server
```

- 扩展被引用的sls数据

    什么是扩展呢。在ssh/server.sls文件中定义了一个apache通用的服务器，现在需要增加一个带有mod_python模块的apache，不需要重新写sls，可以直接include原来的server.sls，然后增加安装mod_python的state，在apache service的watch列表中增加mod_python即可。****

python/mod_ypthon.sls内容如下：

```
include:  
- apache

extend:
  apache:
    service:
      - watch: 
        - pkg:mod_python

mod_python:  pkg.installed
```

这个例子中，先把apache目录下init.sls文件包含进来（在include一个目录时，salt会自动查找init.sls文件），然后拓展了ID为apache下的service state中的watch列表。也可以在extending中修改下载文件位置。extend是salt 的sls更加灵活。

- 理解渲染系统Render System

   因为sls仅是数据，所以不是非要用YAML来表达。salt 默认用YAML，只是因为容易学习和使用，只要提供一个渲染器，sls文件可以以任意格式呈现出来。

​    缺省的渲染系统是yaml_jinja渲染器。yaml_jinja渲染器使用jinjia2模版引擎来处理sls，然后在调用YAML解析。其他可用的渲染其还包括：yaml_mako模版引擎；yaml_wempy，使用Wempy模版引擎；py，使用Python写sls文件；pydsl，建立在python语法基础上的描述语言。

* 默认渲染器---yaml_jinja

  关于jinjia模板系统使用参考官方稳定：[http://jinja.pocoo.org/docs](http://jinja.pocoo.org/docs)

在基于模板引擎的渲染器，可以从3个组件中获取需要的数据：salt，grains和pilla。在模板文件中，salt对象允许任何salt函数从模板内容进行调用，grains允许grains从模板中访问：

```
apache:
  pkg:
    - installed
    {% if grains[ 'os' ] == 'CentOS' %}
    - name: httpd
    {% endif %}
  service:
    - running
    {% if grains[ 'os' ] == 'CentOS'%}
    - name: httpd
    {% endif %}
    - watch:
      - pkg: apache
      - file: /etc/httpd/conf/httpd.conf
      - user: apache
  user.present:
    - name: apache
    - uid: 48
    - gid: 48
    - home: /var/www
    - shell: /bin/nologin
    - require:
      - group: apache
  group.present:
    - name: apache
    - gid: 48
    - require:
      - pkg: apache
/etc/httpd/conf/httpd.conf:
  file.managed:
    - source: salt://apache/files/httpd.conf
    - user: root
    - group: root
    - mode: 644
```

这个例子很容易理解，用到jinja中的条件结构，如果grains中os表明minion的操作系统是CentOS，那么apache的软件包和服务名应当是httpd。更有意思的例子，用到jinja的循环结构，在设置MooseFS分布式中chunkserver：

```yaml
moosefs/chunk.sls：
include:
    - moosefs
{% for mnt in salt['cmd.run']('ls /dev/data/moose*').split() %}
/mnt/moose{{ mnt[-1] }}:
  mount.mounted:
    - device: {{ mnt }}
    - fstype: xfs
    - mkmnt: True
  file.directory:
    - user: mfs
    - group: mfs
    - require:
      - user: mfs
      - group: mfs
{% endfor %}
/etc/mfshdd.cfg:
  file.managed:
    - source: salt://moosefs/mfshdd.cfg
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - pkg: mfs-chunkserver
 
/etc/mfschunkserver.cfg:
  file.managed:
    - source: salt://moosefs/mfschunkserver.cfg
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - pkg: mfs-chunkserver
 
mfs-chunkserver:
  pkg:
    - installed
mfschunkserver:
  service:
    - running
    - require:
{% for mnt in salt['cmd.run']('ls /dev/data/moose*') %}
      - mount: /mnt/moose{{ mnt[-1] }}
      - file: /mnt/moose{{ mnt[-1] }}
{% endfor %}
      - file: /etc/mfschunkserver.cfg
      - file: /etc/mfshdd.cfg
      - file: /var/lib/mfs
```

这个例子展示了jinja的强大之处，多个for循环用来动态的检查并挂载磁盘，并多次使用salt cmd.run执行模块执行shell命令。

- 运行和调用salt states

 一旦写好sls文件，就应该测试，以保证能够正常工作，调用这些规则，只需要在命令行中执行 salt * state.highstate。如果返回的只有主机名，很可能是sls文件存在问题，在minion，使用salt-call命令执行 salt-call state.highstate -l debug来调试输出的作物信息，亦可以在前台执行salt-minion -l debug

### state多环境配置

- master

```
file_roots:
  base:
    - /srv/salt/base
  dev:
    - /srv/salt/dev
```

- 通过命令执行不同环境state

```
salt -N 'minion' state.sls saltenv='dev'
salt -N 'minion' state.sls saltenv='base'
```