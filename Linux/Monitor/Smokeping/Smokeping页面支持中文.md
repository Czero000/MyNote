### smokeping页面和rrdtool图片支持中文
smokeping默认不支持中文，只需要修改如下便可：
#### 页面支持中文
在配置文件的`*** Presentation ***`下面添加
```
charset = utf-8
```
#### rrd图片支持中文

##### 安装中文支持
```
yum groupinstall "chinese support"
```

##### 查看中文字体支持：
```
fc-list :lang=zh
AR PL ZenKai Uni,文鼎PL中楷Uni:style=Medium
AR PL ShanHeiSun Uni,文鼎PL細上海宋Uni,文鼎PL细上海宋Uni:style=Regular
```

##### 修改配置文件
编辑 /usr/local/smokeping/lib/Smokeping/Graphs.pm
```
插入 "'--font TITLE:20:AR PL ShanHeiSun Uni'，"
if ($mode =~ /[anc]/){
        my $val = 0;
        for my $host (@hosts){
            my ($graphret,$xs,$ys) = RRDs::graph
            ("dummy",
            '--start', $tasks[0][1],
            '--end', $tasks[0][2],
            '--font TITLE:20:AR PL ShanHeiSun Uni',
            "DEF:maxping=$cfg->{General}{datadir}${host}.rrd:median:AVERAGE",
            'PRINT:maxping:MAX:%le' );
            my $ERROR = RRDs::error();
            return "
RRDtool did not understand your input: $ERROR. " if $ERROR;
            $val = $graphret->[0] if $val  [0];
        }
        $val = 1e-6 if $val =~ /nan/i;
        $max = { $tasks[0][1] => $val * 1.5 };
    }
```
