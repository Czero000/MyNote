### 安装图形支持
```
yum groupinstall -y  'X Window System' 'Desktop' 'Desktop Platform'
```

### 安装VNC
```
yum install -y tigervnc-server
```

### 配置VNC

#### 编辑vnc服务配置文件
```
vim /etc/sysconfig/vncservers
VNCSERVERS="1:root"
VNCSERVERARGS[1]="-geometry 1024x768 -nolisten tcp "
```

##### 配置vnc密码
```
vncpasswd
```

#### 启动vnc服务
```
/etc/init.d/vncserver start
Starting VNC server: 1:root xauth:  creating new authority file /root/.Xauthority

New 'localhost.localdomain:1 (root)' desktop is localhost.localdomain:1

Creating default startup script /root/.vnc/xstartup
Starting applications specified in /root/.vnc/xstartup
Log file is /root/.vnc/localhost.localdomain:1.log

                                                           [  OK  ]
```

#### 设置vnc自动启动
```
chkconfig vncserver on
```
** 注：~/.vnc/xstartup在CentOS 6下无需增加`gnome-session &` **

#### 多用户设置

```
\\ vnc配置文件
vim /etc/sysconfig/vncservers
VNCSERVERS=”1:userA 2:userB”
VNCSERVERARGS[1]="-geometry 1024x768 -nolisten tcp "
VNCSERVERARGS[2]="-geometry 1024x768 -nolisten tcp "

\\ vnc密码
su - userA
vncpasswd

su - userB
vncpasswd
```

### 实用命令
```
usage: vncserver [:] [-name ] [-depth ]
                 [-geometry x]
                 [-pixelformat rgbNNN|bgrNNN]
                 [-fp ]
                 [-fg]
                 ...


       vncserver -kill 
       vncserver -list
vncserver[:n]             \\开启服务
vncserver -list           \\查看运行列表
vncserver -kill :n        \\杀掉第几个x-display
vncpasswd                 \\修改密码
```
