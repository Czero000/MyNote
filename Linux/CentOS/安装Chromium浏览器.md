之前Google就说了，由于CentOS/RHEL 6已经是过期的系统，所以不再会有Chrome了。 虽然后来由于引起了社区的抗议，从而改口，不再提CentOS/RHEL 6是过期系统了；但是，目前在CentOS/RHEL 6上已经没有Chrome可以下载使用了。
  其实，根本的原因不是CentOS/RHEL 6有多老，连Windows XP和停止更新的Ubuntu 10.04都能继续使用Chrome呢。实际的原因是，Chrome由于种种考虑，使用了CentOS/RHEL 6中所不支持的C++ 11，所以才不能继续更新CentOS/RHEL 6上的Chrome。
  那么，如果希望在CentOS/RHEL 7出来之前继续使用Chrome怎么办？使用Chrome的开源版本：**Chromium**

#### 切换到root
```
su - 或者 sudo -i
```
#### 下载新的软件源定义
```
cd /etc/yum.repos.d
wget http://people.centos.org/hughesjr/chromium/6/chromium-el6.repo
```
#### 安装Chromium
```
yum install -y chromium
```
这样就安装完成了。可以通过菜单来启动浏览器
![启动浏览器](http://ofc9x1ccn.bkt.clouddn.com/centos/chromium-1.png)

启动后

![启动后](http://ofc9x1ccn.bkt.clouddn.com/centos/chromium-2.png)



如果需要查看Flash和PDF，可以继续下面两步来安装插件。

#### 安装Pepper Flash插件：
##### 下载 hughesjr 辅助安装脚本
```
cd /tmp
wget https://raw.github.com/hughesjr/chromium_el_builder/master/chrome_pepperflash_copy.sh
```

##### 设置 chrome_pepperflash_copy.sh 为可执行
```
chmod +x chrome_pepperflash_copy.sh
```
##### 安装（你可以查看一下脚本内容来了解发生了什么）

```
./chrome_pepperflash_copy.sh
```
安装后，如果需要通过命令行方式启动（带有Flash支持），可以输入以下命令：

```
/opt/chromium/chrome-wrapper %U --ppapi-flash-path=/opt/chromium/PepperFlash/libpepflashplayer.so --ppapi-flash-version=$(grep '"version":' /opt/chromium/PepperFlash/manifest.json | grep -Po '(?<=version": ")(?:\d|\.)*')
```
 也可以修改系统菜单中的对应命令

![Flash plugin ](http://ofc9x1ccn.bkt.clouddn.com/centos/chromium-3.png)


#### 安装Google Chrome PDF Viewer插件：
##### 下载 hughesjr 辅助安装脚本
```
cd /tmp
wget https://raw.github.com/hughesjr/chromium_el_builder/master/chrome_libpdf_copy.sh
```
##### 设置 chrome_libpdf_copy.sh 为可执行
```
chmod +x chrome_libpdf_copy.sh
```

##### 执行脚本进行安装（你可以查看一下脚本内容来了解发生了什么）
```
./chrome_libpdf_copy.sh
```
![pdf plugin](http://ofc9x1ccn.bkt.clouddn.com/centos/chromium-3.png)
