国内smokeping配置如下：
```
\\ 主配置文件,加载各部分配置文件
cat config
@include /usr/local/smokeping/etc/config.d/General
@include /usr/local/smokeping/etc/config.d/Database
@include /usr/local/smokeping/etc/config.d/Alerts
@include /usr/local/smokeping/etc/config.d/Probes
@include /usr/local/smokeping/etc/config.d/Slave
@include /usr/local/smokeping/etc/config.d/Targets

\\ 全局配置
cat config.d/General 
*** General ***
owner    = Charlie.Cui
contact  = cuiyuanlong@8864.com
mailhost = mail.8864.com
sendmail = /usr/sbin/sendmail
# NOTE: do not put the Image Cache below cgi-bin
# since all files under cgi-bin will be executed ... this is not
# good for images.
imgcache = /usr/local/smokeping/htdocs/cache
imgurl   = cache
datadir  = /usr/local/smokeping/data
piddir  = /usr/local/smokeping/var
cgiurl   = http://172.16.6.100/ping/smokeping.fcgi
smokemail = /usr/local/smokeping/etc/smokemail
tmail = /usr/local/smokeping/etc/tmail
# specify this to get syslog logging
syslogfacility = local0
# each probe is now run in its own process
# disable this to revert to the old behaviour
# concurrentprobes = yes


\\ 汇总数据配置
cat /config.d/Database
*** Database ***

step     = 60
pings    = 10

# consfn mrhb steps total

AVERAGE  0.5   1  1008
AVERAGE  0.5  12  4320
    MIN  0.5  12  4320
    MAX  0.5  12  4320
AVERAGE  0.5 144   720
    MAX  0.5 144   720
    MIN  0.5 144   720

*** Presentation ***

template = /usr/local/smokeping/etc/basepage.html
charset = UTF-8

###+charts
###
###menu = Charts
###title = The most interesting destinations
###
###++stddev
###sorter = StdDev(entries=>4)
###title = Top Standard Deviation
###menu = Std Deviation
###format = Standard Deviation %f
###
###++max
###sorter = Max(entries=>5)
###title = Top Max Roundtrip Time
###menu = by Max
###format = Max Roundtrip Time %f seconds
###
###++loss
###sorter = Loss(entries=>5)
###title = Top Packet Loss
###menu = Loss
###format = Packets Lost %f
###
###++median
###sorter = Median(entries=>5)
###title = Top Median Roundtrip Time
###menu = by Median
###format = Median RTT %f seconds


+overview 

width = 800
height = 100
range = 1h

+detail

width = 600
height = 200
unison_tolerance = 2

"Last 3 Hours"    3h
"Last 30 Hours"   30h
"Last 10 Days"    10d
"Last 365 Days"   365d

##+ hierarchies
##++ owner
##title = Host Owner
##++ location
##title = Location

\\ 报警类型配置
cat config.d/Alerts 
*** Alerts ***
to = mon@8864.com
from = monitor@8864.com

+网络中断
type = rtt
pattern = !=U,==U
comment = 网络中断
priority = 1

+中断恢复
type = rtt
pattern = ==U,!=U,!=U
comment = 中断恢复
priority = 2

+丢包严重
type = loss
pattern = >50%
comment = 丢包大于50%
priority = 3

+丢包报警
type = loss
pattern = >10%,>10%,>10%
comment = 连续3次丢包10%以上
priority = 4

+延迟较高
type = rtt
pattern = >180,>180,>180
comment = 连续3次延时180以上
priority = 5

\\ 声明使用工具
 cat config.d/Probes 
*** Probes ***
+ FPing
binary = /usr/local/sbin/fping

\\ Slave配置
cat config.d/Slave 
*** Slaves ***
secrets=/usr/local/smokeping/etc/secrets

+SJHL
display_name=世纪互联
location=北京BGP世纪互联
color=ff0000

+SZQ
display_name=苏州桥
location=北京BGP苏州桥
color=eacc00

+KDQ
display_name=看丹桥
location=北京BGP看丹桥
color=0000ff

+ZW
display_name=兆维
location=北京BGP兆维
color=00cf00

+MXY
display_name=木樨园
location=北京BGP木樨园
color=0d006a

+SDZX
display_name=首都在线
location=北京BGP首都在线Cloud
color=ff00ff

\\ 监控节点配置
*** Targets ***
probe = FPing

menu = Top
title = Network Latency Grapher
remark = Welcome to the SmokePing website of LineKong Company. \
         Here you will learn all about the latency of our network.

+Local_IDC
menu = 本地机房
title = IDC Hosts Monitor NetWork
slaves = SJHL SZQ KDQ MXY SDZX
alerts = 网络中断,中断恢复,丢包严重,丢包报警,延迟较高
nomasterpoll = yes

++SJHL
menu = 世纪互联
title = 世纪互联_39_139
host = 59.151.39.139

++SZQ
menu = 苏州桥
title = 苏州桥_54_16
host = 115.182.54.16

++KDQ
menu = 看丹桥
title = 看丹桥_239_17
host = 118.26.239.17

++ZW
menu = 兆维
title = 兆维_9_17
host = 42.62.9.17

++MXY
menu = 木樨园
title = 木樨园_8_18
host = 118.26.154.18

++SDZX
menu = 首都在线
title = 首都在线_2_132
host = 103.244.235.132

++LingKong_Office
menu = 启明国际大厦
title = 启明国际大厦
host = 113.208.129.8

++LK_HongKong
menu = LK_香港
title = LK_香港
host = 218.213.93.70
alerts =

++LK_Korea_253
menu = 韩国_184_253
title =  韩国_184_253
host = 58.229.184.253
alerts=

++LK_Korea_254
menu = 韩国_184_254
title = 韩国_184_254
host = 58.229.184.254
alerts=

++LK_TaiWan_65
menu = 台湾网关
title = 台湾网关
host = 113.196.89.65
alerts=

+China
menu = 中国网络
title = 中国人民共和国
slaves = SJHL SZQ KDQ ZW MXY SDZX
nomasterpoll = yes

++HuaBei
menu = 华北
title = 华北地区

+++BeiJing
menu = 北京
title = 北京市
host = 210.73.64.10

+++TianJin
menu = 天津
title = 天津市
host = 60.28.81.140

+++HeBei
menu = 河北
title = 河北省
host = 121.28.72.194

+++ShanXi
menu = 山西
title = 山西省
host = 218.26.168.1

+++NeiMengGu
menu = 内蒙古
title = 内蒙古自治区
host = 58.18.164.36

++DongBei
menu = 东北
title = 东北地区

+++HeiLongJiang
menu = 黑龙江
title= 黑龙江省
host = 1.58.26.133

+++JiLin
menu = 吉林
title = 吉林省
host = 218.62.26.196

+++LiaoNing
menu = 辽宁
title = 辽宁省
host = 61.161.141.18

++HuaDong
menu = 华东
title = 华东地区

+++ShangHai
menu =  上海
title = 上海市
host = 61.129.65.58

+++JiangSu
menu = 江苏
title = 江苏省
host = 218.2.208.139

+++ZheJiang
menu = 浙江
title = 浙江省
host = 61.130.1.1

+++AnHui
menu = 安徽
title = 安徽省
host = 218.22.0.147

+++FuJian
menu = 福建
title = 福建省
host = 218.85.65.9

+++JiangXi
menu = 江西
title = 江西省
host = 218.87.32.231

+++ShanDong
menu = 山东
title = 山东省
host = 60.216.89.1

++HuaZhong
menu = 华中
title = 华中地区

+++HeNan
menu = 河南
title = 河南省
host = 218.29.1.1

+++HuBei
menu = 湖北
title = 湖北省
host = 219.140.161.86

+++HuNan
menu = 湖南
title = 湖南省
host = 113.240.233.84

++HuaNan
menu = 华南
title = 华南地区

+++GuangDong
menu = 广东
title = 广东省
host = 202.96.154.5

+++GuangXI
menu = 广西
title = 广西自治区
host = 219.159.83.208 

+++HaiNan
menu = 海南
title = 海南省
host = 202.100.210.107

+++AoMen
menu = 澳门
title = 澳门行政区
host = 202.175.13.200

+++HongKong
menu = 香港
title = 香港行政区
host= 147.8.33.1

++XiBei
menu = 西北
title = 西北地区

+++NingXia
menu = 宁夏
title = 宁夏自治区
host = 218.95.217.226

+++XinJiang
menu = 新疆
title = 新疆自治区
host = 218.202.219.192

+++QingHai
menu = 青海
title = 青海省
host = 223.220.250.13

+++ShanXi
menu = 陕西
title = 陕西省
host = 124.115.8.1

+++GanSu
menu = 甘肃
title = 甘肃省
host = 202.100.65.130

++XiNan
menu = 西南
title = 西南地区

+++SiChuan
menu = 四川
title = 四川省
host = 125.64.4.1


+++ChongQing
menu = 重庆
title = 重庆市
host = 219.153.1.197

+++YunNan
menu = 云南
title = 云南省
host = 61.159.229.1

+++GuiZhou
menu = 贵州
title = 贵州自治区
host = 219.151.7.1

+++XiZang
menu = 西藏
title = 西藏自治区
host = 220.182.3.132

+IDC_Test
menu = IDC网络测试
title = IDC网络测试
slaves = SJHL SZQ KDQ ZW MXY SDZX 
nomasterpoll=yes

++HLGWH5
menu = 互联港湾H5
title = 互联港湾H5_103.243.252.20
host = 103.243.252.20

++SHTech
menu = 上海科技网
title = 上海科技网_210.14.71.126
host = 210.14.71.126

++ShuJuJia
menu = 数据家
title = 数据家
host = 210.14.129.6

++TianTan
menu = 铜牛天坛
title = 铜牛天坛
host = 121.52.212.156

++Wuxi_CTC
menu = 无锡电信
title = 无锡电信
host = 58.215.49.1

++RuiJiang_NB_CTC
menu = 睿江宁波电信
title = 睿江宁波电信
host = 115.238.144.11

++RuiJiang_NB_CNC
menu = 睿江宁波网通
title = 睿江宁波网通
host = 60.12.206.11

++RuiJiang_ZS_BGP
menu = 睿江中山BGP
title = 睿江中山BGP
host = 121.201.1.112

++YunLin_HLG
menu = 云林回龙观
title = 云林回龙观
host = 114.112.171.65

++JinShan_Cloud
menu = 金山云
title = 金山云
host = 101.251.105.26

+ChinaMobile
menu = 中国移动网络
title = 中国移动网络
slaves = SJHL SZQ KDQ ZW MXY SDZX
nomasterpoll=yes

++Mobile_BeiJing
host = 211.136.28.237
menu = 北京移动
title = 北京移动_211.136.28.237

++Mobile_TianJin
host = 211.137.160.5
menu = 天津移动
title = 天津移动_211.137.160.5

++Mobile_HeBei
host = 211.138.13.72
menu = 河北移动
title = 河北移动_211.138.13.72

++Mobile_HeNan
host = 211.142.101.66
menu = 河南移动
title = 河南移动_211.142.101.66

++Mobile_ShanDong
host = 211.137.191.26
menu = 山东移动
title = 山东移动_211.137.191.26

++Mobile_NeiMengGu
host = 211.138.91.1
menu = 内蒙古移动
title = 内蒙古移动_211.138.91.1

++Mobile_JiLin
host = 211.141.16.99
menu = 吉林移动
title = 吉林移动_211.141.16.99

++Mobile_LiaoNing
host = 211.140.197.58
menu = 辽宁移动
title = 辽宁移动-211.140.197.58

++Mobile_NingXia
host = 211.138.91.2
menu = 宁夏移动
title = 宁夏移动-211.138.91.2

++Mobile_AnHui
host = 211.138.180.2
menu = 安徽移动
title = 安徽移动-211.138.180.2

++Mobile_ChongQing
host = 221.130.252.200
menu = 重庆移动
title = 重庆移动-221.130.252.200

++Mobile_SiChuan
host = 211.137.96.205
menu = 四川移动
title = 四川移动-211.137.96.205

++Mobile_ZheJiang
host = 211.140.10.2
menu = 浙江移动
title = 浙江移动-211.140.10.2

++Mobile_HuNan
host = 218.201.17.2
menu = 湖南移动
title = 湖南移动-218.201.17.2

++Mobile_GuangDong
host = 211.136.192.6
menu = 广东移动
title = 广东移动-211.136.192.6

++Mobile_SuZhou
host = 221.130.13.133 
menu = 苏州移动
title = 苏州移动-221.130.13.133 

++Mobile_HuBei
host = 211.137.76.67
menu = 湖北移动
title = 湖北移动-211.137.76.67

++Mobile_HaiNan
host =  211.138.164.6
menu = 海南移动
title = 海南移动-211.138.164.6

++Mobile_GanSu
host = 218.203.160.195
menu = 甘肃移动
title = 甘肃移动-218.203.160.195

++Mobile_TaiYuan
host = 211.138.106.19
menu = 山西移动
title = 太原移动-211.138.106.19

++Mobile_HeiLongJiang
host = 211.137.241.34
menu = 黑龙江移动
title = 黑龙江移动-211.137.241.34

++Mobile_GuiZhou
host = 211.139.1.3
menu = 贵州移动
title = 贵州移动-211.139.1.3

++Mobile_XiAn
host = 211.137.130.3
menu = 陕西西安
title = 西安移动-211.137.130.3

++Mobile_GuangXi
host = 211.138.252.71
menu = 广西移动
title = 广西移动-211.138.252.71

++Mobile_QingHai
host = 211.138.75.123
menu = 青海移动
title = 青海移动-211.138.75.123

++Mobile_YunNan
host = 211.139.29.150
menu = 云南移动
title = 云南移动-211.139.29.150

++Mobile_XinJiang
host = 218.202.152.130
menu = 新疆移动
title = 新疆移动-218.202.152.130

++Mobile_XiZang
host = 211.139.73.34
menu = 西藏移动
title = 西藏移动-211.139.73.34

+Tencent_cloud
menu = 腾讯云平台
title = 腾讯云平台
slaves = SJHL SZQ KDQ ZW MXY SDZX
nomasterpoll = yes

++TC_king
menu = 王者_云平台
title = 王者_云平台

+++king_241
menu = 203.195.180.241
title = 王者_云平台203.195.180.241
host = 203.195.180.241

+++king_89
menu = 203.195.189.89
title = 王者_云平台_203.195.189.89
host = 203.195.189.89

++TC_SZR
menu = 神之刃_云平台
title = 神之刃_云平台

+++szr_211
menu = 203.195.192.211
title = 神之刃_云平台_203.195.192.211
host = 203.195.192.211

+Legend_of_King
menu = 王者之剑
title = 王者之剑
slaves = SJHL SZQ KDQ ZW MXY SDZX
#alerts = 网络中断,中断恢复,丢包严重,丢包报警,延迟较高
nomasterpoll = yes

++King_91
menu = king_91
title = service.sj.91.com

+++91_FJ_CNC
menu = 福建网通
title = 福建网通_58.22.107.136
host = 58.22.107.136

+++91_FJ_CTC
menu = 福建电信
title = 福建电信_121.207.242.72
host = 121.207.242.72

+++91_FJ_Mobile
menu = 福建移动
title = 福建移动_218.207.216.84
host = 218.207.216.84

++king_UC
menu = king_uc
title = sdk.g.uc.cn

+++uc_ZJ_CTC
menu = 浙江电信
title = 浙江电信_115.238.230.122
host = 115.238.230.122

+++uc_GD_CTC
menu = 广东电信
title = 广东电信_119.147.224.158
host = 119.147.224.158

+++uc_GD_Mobile
menu = 广东移动
title = 广东移动_183.233.224.189
host = 183.233.224.189

+++uc_SH_Mobile
menu = 上海移动
title = 上海移动_117.135.151.250
host = 117.135.151.250

++King_MI
menu = king_MI
title = mis.migc.xiaomi.com

+++MI_BJ_Blue
menu = 北京蓝汛
title = 北京蓝汛_223.202.68.53 
host = 223.202.68.53

+++MI_BJ_KDQ
menu = 看丹桥
title = 看丹桥_42.62.48.210
host = 42.62.48.210

++DangLe
menu = king_DangLe
title = connect.d.cn

+++DangLE_BJ_DXT
menu = 北京电信通
title = 北京电信通_118.144.65.115
host = 118.144.65.115

++king_360
menu = king_360
title = openapi.360.cn

+++360_BJ_CTC
menu = 北京电信
title = 北京电信_218.30.118.206
host = 218.30.118.206

+++360_BJ_CNC
menu = 北京网通
title = 北京网通_123.125.82.205
host = 123.125.82.205

++king_QQ
menu = king_QQ
title = openapi.3g.qq.com

+++QQ_HN_CTC
menu = 湖南电信
title = 湖南电信_124.232.132.94
host = 124.232.132.94

+++QQ_GD_CTC
menu = 广东电信
title = 广东电信_218.30.64.194
host = 218.30.64.194

+++QQ_SC_CTC
menu = 四川电信
title= 四川电信_61.139.8.102
host = 61.139.8.102

+++QQ_BJ_CNC
menu = 北京网通
title= 北京网通_220.250.64.19
host = 220.250.64.19

+++QQ_SH_CNC
menu = 上海网通
title = 上海网通_27.115.124.157
host = 27.115.124.157

+++QQ_SH_Mobile
menu = 上海移动
title = 上海移动_120.204.200.45
host = 120.204.200.45

+++QQ_SH_CTC
menu = 上海电信
title = 上海电信_180.153.3.176
host = 180.153.3.176

++king_gfan
menu = king_gfan
title = api.gfan.com

+++gfan_BJ_SanXin
menu = 北京三星
title = 北京三星_117.79.130.165
host = 117.79.130.165

++king_kugou
menu = king_kugou
title = gapi.kugou.com

+++kugou_GD_CTC
menu = 广东电信
title = 广东电信_183.61.119.205
host = 183.61.119.205

+++kugou_GD_CNC
menu = 广东联通
title = 广东联通_122.13.67.141
host = 122.13.67.141

+++kugou_DG_Mobile
menu = 广东移动
title = 广东移动_183.232.70.205 
host = 183.232.70.205

++king_OppO
menu = king_OppO
title = thapi.nearme.com.cn 

+++Oppo_ZJ_CTC
menu = 浙江电信
title = 浙江电信_115.236.98.98
host = 115.236.98.98

+++Oppo_ZJ_CNC
menu = 浙江网通
title = 浙江网通_60.12.231.68
host = 60.12.231.68

+++Oppo_ZJ_Mobile
menu = 浙江移动
title = 浙江移动_120.199.7.218
host = 120.199.7.218

++king_baidu
menu = king_baidu
title = sdk.m.duoku.com 

+++baidu_BJ_Mobile
menu = 北京移动
title = 北京移动_111.13.46.109
host = 111.13.46.109

+alipay
menu = 支付宝
title = Alipay Hosts Monitor
slaves = SJHL SZQ KDQ MXY SDZX
nomasterpoll = yes

++alipay1965
menu = 浙江杭州阿里
title = 浙江杭州阿里_110.76.19.65
host = 110.76.19.65

++alipay2065
menu = 浙江杭州阿里
title = 浙江杭州阿里_110.76.20.65
host = 110.76.20.65

+FZTech
menu = 斧子科技
title =  Hosts Monitor
slaves = SJHL SZQ KDQ MXY SDZX
nomasterpoll = yes

++FZ442
menu = FZ_4.42
title = FZ_114.119.4.42
host = 114.119.4.42

++FZ6246
menu = 斧子科技_114.67.62.46
title = 斧子科技_114.67.62.46
host = 114.67.62.46

++FZ5934
menu = 斧子科技_114.67.59.34
title = 斧子科技_114.67.59.34
host = 114.67.59.34

++FZ058
menu = 斧子科技_121.201.0.58
title = 斧子科技_121.201.0.58
host = 121.201.0.58

++FZ3339
menu = 斧子科技_121.201.33.39
title = 斧子科技_121.201.33.39
host = 121.201.33.39

++FZ382
menu = 斧子科技_180.186.38.2
title = 斧子科技_180.186.38.2
host = 180.186.38.2

++FZ952
menu = 斧子科技_14.152.95.2
title = 斧子科技_14.152.95.2
host = 14.152.95.2

++FZ87254
menu = 斧子科技_58.253.87.254
title = 斧子科技_58.253.87.254
host = 58.253.87.254

++FZ175193
menu = 斧子科技_183.60.175.193
title = 斧子科技_183.60.175.193
host = 183.60.175.193

++FZ162199
menu = 斧子科技_122.13.162.199
title = 斧子科技_122.13.162.199
host = 122.13.162.199

++FZ52
menu = 斧子科技_114.119.5.2
title = 斧子科技_114.119.5.2
host = 114.119.5.2

++FZ6263
menu = 斧子科技_114.67.62.63
title = 斧子科技_114.67.62.63
host = 114.67.62.63

++FZ134217
menu = 斧子科技_118.195.134.217
title = 斧子科技_118.195.134.217
host = 118.195.134.217
```

