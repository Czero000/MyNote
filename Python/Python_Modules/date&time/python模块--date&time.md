#time
```python
import time
print time.time()  //当前时间戳
print time.clock()  //返回当前cpu时间
```

time.sleep可以讲程序至于休眠状态，直到某时间间隔后在唤醒程序
```python
import time
print ‘start’
time.sleep(10)
print 'wake up'
```

time包还定义了struct_time对象。该对象实际上是将挂钟时间转换为年、月、日、时、分、秒……等日期信息，存储在该对象的各个属性中(tm_year, tm_mon, tm_mday...)。下面方法可以将挂钟时间转换为struct_time对象:
```
st = time.gmtime()      # 返回struct_time格式的UTC时间
st = time.localtime()   # 返回struct_time格式的当地时间, 当地时区根据系统环境决定。
s  = time.mktime(st)    # 将struct_time格式转换成wall clock time
```
```
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
```

# datetime
datetime是基于time包的一个高级包，datetime可以理解为date和time两个部分，date指日期，time是分秒时组成，可以将两个分开管理(datetime.date和datetime.time)

- 表达时间
```python
import datetime
print datetime.datetime(2016,02,12,23,12)
2016-02-12 23:12:00
```

- 计算时间
```
import datetime
t = datetime.datetime(2016,6,3,21,30)
t_next = datetime.datetime(2016,6,5,23,30)
delta1 = datetime.timedelta(seconds = 600)
delta2 = datetime.timedelta(weeks = 3)
print(t + delta1)
print(t + delta2)
print(t_next - t)
```
- 与字符串转换
```python
form datetime import datetimie
format = "output-%Y-%m-%d-%H%M%S.txt"
str = "output-1997-12-23-030000.txt"
t = datetime.strptime(str, fromat)
```
