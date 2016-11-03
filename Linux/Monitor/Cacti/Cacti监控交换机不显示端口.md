Cacti监控cisco设备时图表上的标题显示为GigabitEthernet而并没有指出具体的端口号,一般说来，图片的流量统计描述都是`|host_description| - Traffic - |query_ifName| `按照这个形式来描述的，对于华为的设备，Gi显示成GigabitEthernet，可能导致后面的模块号，端口好无法显示。原因是Cacti的 ” 最大域 长度(用于显示数据查询区域的最大字符数.) ” 默认为15.

修改方法:

### 中文版

配置 -> 设置 -> 可视化 -> 最大域长度 80




###  英文版

```

Console -> Settings -> Visual -> Maximum Field Length: 默认15,修改成80就OK了。

The maximum number of characters to display for a data query field.

Maximum Title Length

The maximum number of characters to display for a graph title.

Maximum Field Length

The maximum number of characters to display for a data query field.

```

同时修改了以上2个选项，但是还是不行。

发现流量的绘图引用的是`Interface - Traffic (bits/sec)`这个模板，

`console-Graph Templates-Interface - Traffic (bits/sec)`



 在后面的框框里面加上了`- |query_ifName|`这部分内容，以前这里是没有的！

 最后重新添加图，发现端口已经出来了！
