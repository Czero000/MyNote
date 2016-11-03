Centos7是Centos系列的最新版本，与老版本出现了较大操作差异，下面是安装中文支持
###中文支持
* 安装语言包
```
yum install kde-l10n-Chinese -y
```

* 修改系统默认语言
```
localectl set-locale LANG=zh_CN.utf8
```

* 安装中文字体

```
yum install ibus-table-chinese*
```

* 查看已安装的字体
```
fc-list :lang=zh
/usr/share/fonts/cjkuni-ukai/ukai.ttc: AR PL UKai TW:style=Book
/usr/share/fonts/cjkuni-ukai/ukai.ttc: AR PL UKai HK:style=Book
/usr/share/fonts/cjkuni-ukai/ukai.ttc: AR PL UKai CN:style=Book
/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc: 文泉驿点阵正黑,文泉驛點陣正黑,WenQuanYi Zen Hei Sharp:style=Regular
/usr/share/fonts/cjkuni-uming/uming.ttc: AR PL UMing TW MBE:style=Light
/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc: 文泉驿等宽正黑,文泉驛等寬正黑,WenQuanYi Zen Hei Mono:style=Regular
/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc: 文泉驿正黑,文泉驛正黑,WenQuanYi Zen Hei:style=Regular
/usr/share/fonts/cjkuni-ukai/ukai.ttc: AR PL UKai TW MBE:style=Book
/usr/share/fonts/cjkuni-uming/uming.ttc: AR PL UMing TW:style=Light
/usr/share/fonts/cjkuni-uming/uming.ttc: AR PL UMing HK:style=Light
/usr/share/fonts/cjkuni-uming/uming.ttc: AR PL UMing CN:style=Light
```

* 重新连接终端即可
