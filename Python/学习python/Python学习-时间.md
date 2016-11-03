### Python 日期和时间

Python程序能用很多方式处理日期和时间。转换日期格式是一个常见的例行琐事。Python有一个 time 和 calendar 模组可以帮忙。

------

#### 什么是Tick？

时间间隔是以秒为单位的浮点小数。

每个时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示。

Python附带的受欢迎的time模块下有很多函数可以转换常见日期格式。如函数time.time()用ticks计时单位返回从12:00am, January 1, 1970(epoch) 开始的记录的当前操作系统时间, 如下实例:

```
#!/usr/bin/python
import time;  # This is required to include time module.

ticks = time.time()
print "Number of ticks since 12:00am, January 1, 1970:", ticks
```

以上实例输出结果：

```
Number of ticks since 12:00am, January 1, 1970: 7186862.73399
```

Tick单位最适于做日期运算。但是1970年之前的日期就无法以此表示了。太遥远的日期也不行，UNIX和Windows只支持到2038年某日。

------

#### 什么是时间元组？

很多Python函数用一个元组装起来的9组数字处理时间:

| 序号   | 字段     | 值                        |
| ---- | ------ | ------------------------ |
| 0    | 4位数年   | 2008                     |
| 1    | 月      | 1 到 12                   |
| 2    | 日      | 1到31                     |
| 3    | 小时     | 0到23                     |
| 4    | 分钟     | 0-59                     |
| 5    | 秒      | 0到61 (60或61 是闰秒)         |
| 6    | 一周的第几日 | 0到6 (0是周一)               |
| 7    | 一年的第几日 | 1到366 (儒略历)              |
| 8    | 夏令时    | -1, 0, 1, -1是决定是否为夏令时的旗帜 |

上述也就是struct_time元组。这种结构具有如下属性：

| 序号   | 属性       | 值                        |
| ---- | -------- | ------------------------ |
| 0    | tm_year  | 2008                     |
| 1    | tm_mon   | 1 到 12                   |
| 2    | tm_mday  | 1 到 31                   |
| 3    | tm_hour  | 0 到 23                   |
| 4    | tm_min   | 0 到 59                   |
| 5    | tm_sec   | 0 到 61 (60或61 是闰秒)       |
| 6    | tm_wday  | 0到6 (0是周一)               |
| 7    | tm_yday  | 1 到 366(儒略历)             |
| 8    | tm_isdst | -1, 0, 1, -1是决定是否为夏令时的旗帜 |

------

#### 获取当前时间

从返回浮点数的时间辍方式向时间元组转换，只要将浮点数传递给如localtime之类的函数。

```
#!/usr/bin/python
import time;

localtime = time.localtime(time.time())
print "Local current time :", localtime
```

以上实例输出结果：

```
Local current time : time.struct_time(tm_year=2013, tm_mon=7,
tm_mday=17, tm_hour=21, tm_min=26, tm_sec=3, tm_wday=2, tm_yday=198, tm_isdst=0)
```

------

#### 获取格式化的时间

你可以根据需求选取各种格式，但是最简单的获取可读的时间模式的函数是asctime():

```
#!/usr/bin/python
import time;

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime
```

以上实例输出结果：

```
Local current time : Tue Jan 13 10:17:09 2009
```

------

#### 获取某月日历

Calendar模块有很广泛的方法用来处理年历和月历，例如打印某月的月历：

```
#!/usr/bin/python
import calendar

cal = calendar.month(2008, 1)
print "Here is the calendar:"
print cal;
```

以上实例输出结果：

```
Here is the calendar:
    January 2008
Mo Tu We Th Fr Sa Su
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31
```

------

#### Time模块

Time模块包含了以下内置函数，既有时间处理相的，也有转换时间格式的：

| 序号   | 函数及描述                                    |
| ---- | ---------------------------------------- |
| 1    | [time.altzone]返回格林威治西部的夏令时地区的偏移秒数。如果该地区在格林威治东部会返回负值（如西欧，包括英国）。对夏令时启用地区才能使用。 |
| 2    | [time.asctime([tupletim\])]接受时间元组并返回一个可读的形式为"Tue Dec 11 18:07:14 2008"（2008年12月11日 周二18时07分14秒）的24个字符的字符串。 |
| 3    | [time.clock( )]用以浮点数计算的秒数返回当前的CPU时间。用来衡量不同程序的耗时，比time.time()更有用。 |
| 4    | [time.ctime([sec\])]作用相当于asctime(localtime(secs))，未给参数相当于asctime() |
| 5    | [time.gmtime([sec\])]接收时间辍（1970纪元后经过的浮点秒数）并返回格林威治天文时间下的时间元组t。注：t.tm_isdst始终为0 |
| 6    | [time.localtime([sec\])]接收时间辍（1970纪元后经过的浮点秒数）并返回当地时间下的时间元组t（t.tm_isdst可取0或1，取决于当地当时是不是夏令时）。 |
| 7    | [time.mktime(tupletime)]接受时间元组并返回时间辍（1970纪元后经过的浮点秒数）。 |
| 8    | [time.sleep(secs)])推迟调用线程的运行，secs指秒数。    |
| 9    | [time.strftime(fmt[,tupletim\])]接收以时间元组，并返回以可读字符串表示的当地时间，格式由fmt决定。 |
| 10   | [time.strptime(str,fmt='%a %b %d %H:%M:%S %Y')]根据fmt的格式把一个时间字符串解析为时间元组。 |
| 11   | [time.time( )]返回当前时间的时间戳（1970纪元后经过的浮点秒数）。 |
| 12   | [time.tzset()]根据环境变量TZ重新初始化时间相关设置。       |

Time模块包含了以下2个非常重要的属性：

| 序号   | 属性及描述                                    |
| ---- | ---------------------------------------- |
| 1    | **time.timezone**属性time.timezone是当地时区（未启动夏令时）距离格林威治的偏移秒数（>0，美洲;<=0大部分欧洲，亚洲，非洲）。 |
| 2    | **time.tzname**属性time.tzname包含一对根据情况的不同而不同的字符串，分别是带夏令时的本地时区名称，和不带的。 |

- time altzone()

描述：[time.altzone]返回格林威治西部的夏令时地区的偏移秒数。如果该地区在格林威治东部会返回负值（如西欧，包括英国）。对夏令时启用地区才能使用。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

print "time.altzone %d" % time.altzone
// 输出
time.altzone -28800
```

- time asctime()

描述：Python time asctime() 函数接受时间元组并返回一个可读的形式为"Tue Dec 11 18:07:14 2008"（2008年12月11日 周二18时07分14秒）的24个字符的字符串。

语法：`time.asctime([t])`

参数：t -- 9个元素的元组或者通过函数 gmtime() 或 localtime() 返回的时间值。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

t1 = time.localtime()
t2 = time.gmtime()
print "time.asctime(t1): %s" % time.asctime(t1)
print "time.asctime(t2): %s" % time.asctime(t2)
//输出
time.asctime(t1): Tue Mar 22 10:23:45 2016
time.asctime(t2): Tue Mar 22 02:23:45 2016
```

- time clock()

描述：Python time clock() 函数以浮点数计算的秒数返回当前的CPU时间。用来衡量不同程序的耗时，比time.time()更有用。这个需要注意，在不同的系统上含义不同。在UNIX系统上，它返回的是"进程时间"，它是用秒表示的浮点数（时间戳）。而在WINDOWS中，第一次调用，返回的是进程运行的实际时间。而第二次之后的调用是自第一次调用以后到现在的运行时间。（实际上是以WIN32上QueryPerformanceCounter()为基础，它比毫秒表示更为精确）

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
def procedure():
    time.sleep(2)

t0 = time.clock()
procedure()
print time.clock() - t0, "Second process time"

t0 = time.time()
procedure()
print time.time() - t0, "Seconds wall time"

// 输出
0.0 Second process time
2.00219511986 Seconds wall time
```

- time ctime()

描述：Python time ctime() 函数把一个时间戳（按秒计算的浮点数）转化为time.asctime()的形式。 如果参数未给或者为None的时候，将会默认time.time()为参数。它的作用相当于 asctime(localtime(secs))。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

print "time.ctime() : %s" % time.ctime()

// 脚本
time.ctime() : Tue Mar 22 10:45:49 2016
```

- time gmtime()

描述：Python time gmtime() 函数将一个时间戳转换为UTC时区（0时区）的struct_time，可选的参数sec表示从1970-1-1以来的秒数。其默认值为time.time()，函数返回time.struct_time类型的对象。（struct_time是在time模块中定义的表示时间的对象）。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
print "time.gmtime() : %s" % time.gmtime()

//输出
time.gmtime() : time.struct_time(tm_year=2016, tm_mon=3, tm_mday=22, tm_hour=6, tm_min=35, tm_sec=37, tm_wday=1, tm_yday=82, tm_isdst=0)
```

- time localtime()

描述：Python time localtime() 函数类似gmtime()，作用是格式化时间戳为本地的时间。 如果sec参数未输入，则以当前时间为转换标准。 DST (Daylight Savings Time) flag (-1, 0 or 1) 是否是夏令时。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
print "time.localtime(): %s" % time.localtime()

//输出
time.localtime(): time.struct_time(tm_year=2016, tm_mon=3, tm_mday=22, tm_hour=14, tm_min=39, tm_sec=8, tm_wday=1, tm_yday=82, tm_isdst=0)
```

- time mktime()

描述：ython time mktime() 函数执行与gmtime(), localtime()相反的操作，它接收struct_time对象作为参数，返回用秒数来表示时间的浮点数。如果输入的值不是一个合法的时间，将触发 OverflowError 或 ValueError。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

t = (2016, 3, 22, 14, 39, 8, 1, 32, 0)
secs = time.mktime( t )
print "time.mktime(t) : %f" %secs
print "asctime(localtime(secs)) : %s " % time.asctime(time.localtime(secs))

//输出
time.mktime(t) : 1458628748.000000
asctime(localtime(secs)) : Tue Mar 22 14:39:08 2016
```

- time sleep()

描述：Python time sleep() 函数推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

print "Start : %s" % time.ctime()
time.sleep(5)
print "End: %s" % time.ctime()
//输出
Start : Tue Mar 22 14:51:44 2016
End: Tue Mar 22 14:51:49 2016
```

- time strftime()

描述：Python time strftime() 函数接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定。

python时间日期格式化符号


|  符号  | 表示日期                    |
| :--: | ----------------------- |
|  %y  | 两位数的年份表示（00-99）         |
|  %Y  | 四位数的年份表示（000-9999）      |
|  %m  | 月份（01-12）               |
|  %d  | 月内中的一天（0-31）            |
|  %H  | 24小时制小时数（0-23）          |
|  %I  | 12小时制小时数（01-12）         |
|  %M  | 分钟数（00=59）              |
|  %S  | 秒（00-59）                |
|  %a  | 本地简化星期名称                |
|  %A  | 本地完整星期名称                |
|  %b  | 本地简化的月份名称               |
|  %B  | 本地完整的月份名称               |
|  %c  | 本地相应的日期表示和时间表示          |
|  %j  | 年内的一天（001-366）          |
|  %p  | 本地A.M.或P.M.的等价符         |
|  %U  | 一年中的星期数（00-53）星期天为星期的开始 |
|  %w  | 星期（0-6），星期天为星期的开始       |
|  %W  | 一年中的星期数（00-53）星期一为星期的开始 |
|  %x  | 本地相应的日期表示               |
|  %X  | 本地相应的时间表示               |
|  %Z  | 当前时区的名称                 |
|  %%  | %号本身                    |

```python

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

t = (2016, 3, 22, 14, 39, 8, 1, 32, 0)
t = time.mktime(t)

print time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t))
//脚本
Mar 22 2016 06:39:08
```

- time strptime()

描述：Python time strptime() 函数根据指定的格式把一个时间字符串解析为时间元组。

```
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

struct_time = time.strptime("22 Mar 16", "%d %b %y")
print "returned tuple: %s" % struct_time
//输出
returned tuple: time.struct_time(tm_year=2016, tm_mon=3, tm_mday=22, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=82, tm_isdst=-1
```

- time time()

描述：Python time time() 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
print "time.time(): %f" % time.time()
print time.localtime(time.time())
print time.asctime(time.localtime(time.time()))
//输出
time.time(): 1458631592.902243
time.struct_time(tm_year=2016, tm_mon=3, tm_mday=22, tm_hour=15, tm_min=26, tm_sec=32, tm_wday=1, tm_yday=82, tm_isdst=0)
Tue Mar 22 15:26:32 2016
```

- time tzset()

描述：Python time tzset() 根据环境变量TZ重新初始化时间相关设置。

标准TZ环境变量格式：`std offset [dst [offset [,start[/time], end[/time]]]]`

参数：

std 和 dst:三个或者多个时间的缩写字母。传递给 time.tzname.

offset: 距UTC的偏移，格式： [+|-]hh[:mm[:ss]] {h=0-23, m/s=0-59}。*

start[/time], end[/time]: DST 开始生效时的日期。格式为 m.w.d — 代表日期的月份、周数和日期。w=1 指月份中的第一周，而 w=5 指月份的最后一周。'start' 和 'end' 可以是以下格式之一：**Jn:** 儒略日 n (1 <= n <= 365)。闰年日（2月29）不计算在内。**n:** 儒略日 (0 <= n <= 365)。 闰年日（2月29）计算在内**Mm.n.d:** 日期的月份、周数和日期。w=1 指月份中的第一周，而 w=5 指月份的最后一周。**time:**（可选）DST 开始生效时的时间（24 小时制）。默认值为 02:00（指定时区的本地时间）。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import os
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()
print time.strftime('%X %x %Z')

os.environ['TZ'] = 'AEST-10AEST,M10.5.0,M3.5.0'
time.tzset()
print time.strftime('%X %x %Z')
// 输出
02:58:47 03/22/16 EST
18:58:47 03/22/16 AEST
```
------

#### 日历（Calendar）模块

此模块的函数都是日历相关的，例如打印某月的字符月历。

星期一是默认的每周第一天，星期天是默认的最后一天。更改设置需调用calendar.setfirstweekday()函数。模块包含了以下内置函数：

| 序号   | 函数及描述                                    |
| ---- | ---------------------------------------- |
| 1    | **calendar.calendar(year,w=2,l=1,c=6)**返回一个多行字符串格式的year年年历，3个月一行，间隔距离为c。 每日宽度间隔为w字符。每行长度为21* W+18+2* C。l是每星期行数。 |
| 2    | **calendar.firstweekday( )**返回当前每周起始日期的设置。默认情况下，首次载入caendar模块时返回0，即星期一。 |
| 3    | **calendar.isleap(year)**是闰年返回True，否则为false。 |
| 4    | **calendar.leapdays(y1,y2)**返回在Y1，Y2两年之间的闰年总数。 |
| 5    | **calendar.month(year,month,w=2,l=1)**返回一个多行字符串格式的year年month月日历，两行标题，一周一行。每日宽度间隔为w字符。每行的长度为7* w+6。l是每星期的行数。 |
| 6    | **calendar.monthcalendar(year,month)**返回一个整数的单层嵌套列表。每个子列表装载代表一个星期的整数。Year年month月外的日期都设为0;范围内的日子都由该月第几日表示，从1开始。 |
| 7    | **calendar.monthrange(year,month)**返回两个整数。第一个是该月的星期几的日期码，第二个是该月的日期码。日从0（星期一）到6（星期日）;月从1到12。 |
| 8    | **calendar.prcal(year,w=2,l=1,c=6)**相当于 print calendar.calendar(year,w,l,c). |
| 9    | **calendar.prmonth(year,month,w=2,l=1)**相当于 print calendar.calendar（year，w，l，c）。 |
| 10   | **calendar.setfirstweekday(weekday)**设置每周的起始日期码。0（星期一）到6（星期日）。 |
| 11   | **calendar.timegm(tupletime)**和time.gmtime相反：接受一个时间元组形式，返回该时刻的时间辍（1970纪元后经过的浮点秒数）。 |
| 12   | **calendar.weekday(year,month,day)**返回给定日期的日期码。0（星期一）到6（星期日）。月份为 1（一月） 到 12（12月）。 |

------

#### 其他相关模块和函数

在Python中，其他处理日期和时间的模块还有：

- [datetime模块](http://docs.python.org/library/datetime.html#module-datetime)
- [pytz模块](http://www.twinsun.com/tz/tz-link.htm)
- [dateutil模块](http://labix.org/python-dateutil)
