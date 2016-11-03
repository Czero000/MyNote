### smokeping Master/Slave分布式模式
在使用smokeping过程中，很容易发现，如果从单个节点去探测网络性能，并不能充分检测到整个网络的一个状态。smokeping提供了基于多节点的分布式模式，可以从多个节点去探测到网络的状态，这样我们才能全面客观的监控真个网络。
smokeping的分布式为主从模式，M/S模式配置起来很简单，slave的配置基本与master的配置相同，只是slave不需要config文件，而是在启动过程中请求master上面的config文件，这样只需要维护master上面的config文件即可。
  smokeping分布式的检测方式为被动方式，由slave节点在启动时从master上获取config文件，然后进行探测，探测后的数据在通过cgi提交给master。slave可为多个，M/S直接通信认证是通过`--shared-secret=filename`来和`master`进行密码认证。
```
[slave 1]     [slave 2]      [slave 3]
        |             |              |
        +-------+     |     +--------+
                |     |     |
                v     v     v
              +---------------+
              |    master     |
              +---------------+
```

### Smokeping主从通信认证

smokeping主从验证通过Master和和Slave的/usr/local/smokeping/etc/smokeping_secrets文件进行的，但是Master和Slave的验证文件书写方式是有所不同。

#### Master验证文件格式

```
SlaveName:Password
```
SlaveName是在Master配置文件中定义slave是指定的名称，这个名称要唯一。

**注:`/usr/local/smokeping/etc/smokeping_secrets` 文件属性必须是600**



#### Slave验证文件格式
```
Password
```

Slave的secrets文件在启动时要指定，Master和Slave的密码要保持一致。

**注: `/usr/local/smokeping/etc/smokeping_secrets` 文件属性必须是600**



### 配置Slave

#### 修改配置文件

配置主从主要有两步，一是修改smokeping_secrets文件，添加SlaveName和Password。二是修改Master上面的config文件

在配置文件中添加如下内容：
```
*** Slaves ***                               
secrets=/usr/local/smokeping/etc/smokeping_secrets            ###验证文件
+boomer                                                       ###SlaveName，要和smokeping_secrets保持一致，slave启动时也是这个名字
display_name=boomer                                           ###页面显示的名字
color=0000ff                                                  ###绘图颜色，要小写
```
slave可以配置多个，名字要唯一，颜色也要不同，配置完slave后，还要在监控节点上面添加slave


#### 部署slave

部署slave和Master步骤相同，可以参考Master 的部署过程。


#### 启动Slave

slave并不需要config配置文件，在启动时要指定master地址等相关信息，格式如下：
```
/usr/local/smokeping/bin/smokeping --master-url=http://masterip/ping/smokeping.cgi  --cache-dir=/var/smokeping --shared-secret=/usr/local/smokeping/etc/secrets  --slave-name=SlaveName
```
