debian与ubuntu有很大的相似性，但是debian相对更原始，比如在语言支持这一块，如果在安装ubuntu的时候，选择的系统语言是英文，那么系统显示的肯定是英文，但是查看中文文件的时候，肯定还是能查看的，因为系统默认支持了中文，中文字体，语言包等已经安装好了，但是 debian不同，如果你安装的时候选择了英文，那么进入系统之后，只要查看不是英文的东西都是乱码，就连网页上的汉字都是一个个的方块。

要解决这个问题，只能自己手动添加中文支持：

#### 生成locales:
运行 dpkg-reconfigure locales，选择上以下选项：
```
en_US ISO-8859-1
zh_CN GB2312
zh_CN.GBK GBK
zh_CN.UTF-8 UTF-8
zh_TW BIG5
zh_TW.UTF-8 UTF-8
```
接下来要安装中文字体，一共有以下几个包需要安装：
```
ttf-arphic-gbsn00lp (AR PL SungtiL GB)
ttf-arphic-gkai00mp (AR PL KaitiM GB)
ttf-arphic-bsmi00lp (AR PL Mingti2L Big5)
ttf-arphic-bkai00mp (AR PL KaitiM Big5)
```
前面两个是简体的，后面两个是繁体的，但是最好都装上，否则到时候很可能乱码。

执行：
```
sudo apt-get install ttf-arphic-gbsn00lp ttf-arphic-gkai00mp ttf-arphic-bsmi00lp ttf-arphic-bkai00mp
```
**PS:这些只是基本字体，只能保证中文正常显示，如果要说好看那是谈不上的。如果要好看一点的话，可以在软件中心搜索安装xfonts**

接下来就是安装中文输入法，个人推荐使用ibus，比较好用而且兼容性也还行，可以参考http://www.cnblogs.com/pengdonglin137/p/3280520.html

当然，在X环境下还要设置locale变量：

可以在`/etc/X11/Xsession.d/95xinput`这个文件里写上如下语句：
```
export LANG=zh_CN.gb2312
```
**PS:如果你在启动之后执行这条命令不会有效，只能重启并在加载X window之前执行才有效，这就是为什么把它写入文件的原因（这个文件在X window启动前被加载。）**

这样一来，你的系统菜单等也会变成中文，如果你还是想要英文菜单，但是只要能显示中文，那么就要多设置几个变量：
```
ENCODING="en_US"
#export LC_ALL=$ENCODING
export LC_MESSAGES=$ENCODING
#export LC_COLLATE=$ENCODING
#export LC_CTYPE=$ENCODING
export LC_TIME=$ENCODING
export LC_NUMERIC=$ENCODING
#export LC_MONETARY=$ENCODING
#export LC_PAPER=$ENCODING
#export LC_NAME=$ENCODING
export LC_ADDRESS=$ENCODING
export LC_TELEPHONE=$ENCODING
export LC_MEASUREMENT=$ENCODING
export LC_IDENTIFICATION=$ENCODING
```
同样把这些写入`/etc/X11/Xsession.d/95xinput`文件，重启就行了。
最后要说一下终端对中文的支持：
KDE默认的终端是konsole, 默认就支持中文，而且还支持得不错，gnome默认的终端是gnome-terminal, 要支持中文的话只要在菜单里选上中文相应的编码就行了。
