## 什么是运算符 ##
Python语言支持以下类型的运算符

- 算术运算符
- 比较（关系）运算符
- 赋值运算符
- 逻辑运算符
- 位运算符
- 成员运算符
- 身份运算符
- 运算符优先级

接下来让我们一个个来学习Python的运算符。

### Python 算术运算符 ###

以下假设变量a为10，变量b为20：

| 运算符  | 描述                        |
| ---- | ------------------------- |
| +    | 加 - 两个对象相加                |
| -    | 减 - 得到负数或是一个数减去另一个数       |
| *    | 乘 - 两个数相乘或是返回一个被重复若干次的字符串 |
| /    | 除 - x除以y                  |
| %    | 取模 - 返回除法的余数              |
| **   | 幂 - 返回x的y次幂               |
| //   | 取整除 - 返回商的整数部分            |

```python
// 脚本内容
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
a = 21
b = 10
c = 0

c = a + b
print "Line 1 - Value of c is", c

c = a - b
print "Line 2 - Value of c is", c

c = a * b
print "Line 3 - Value of c is", c

c = a / b
print "Line 4 - Value of c is", c

c = a % b
print "Line 5 - Value of c is", c

a = 2
b = 3
c = a**b
print "Line 6 - Value of c is", c

a = 10
b = 5
c = a//b
print "Line 7 - Value of c is", c

//结果输出
Line 1 - Value of c is 31
Line 2 - Value of c is 11
Line 3 - Value of c is 210
Line 4 - Value of c is 2
Line 5 - Value of c is 1
Line 6 - Value of c is 8
Line 7 - Value of c is 2
```

### Python比较运算符 ###
假设a为10，b为20

| 运算符  | 描述                 | 实例                                |
| ---- | ------------------ | --------------------------------- |
| ==   | 等于 - 比较对象是否相等      | (a == b) 返回 False                 |
| !=   | 不等于 - 比较两个对象是否不相等  | (a != b) 返回 true                  |
| <>   | 不等于 - 比较两个对象是否不相等  | (a    <>    b) 返回 true 这个运算符类似 != |
| >    | 大于 - 返回x是否大于y      | (a > b) 返回 False。                 |
| >=   | 大于等于 - 返回x是否大于等于y。 | (a >= b) 返回 False                 |


```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
a = 21
b = 10
c = 0

if ( a == b ):
    print "Line 1 - a is equal to b"
else:
    print "Line 1 - a is not equal to b"

if ( a != b ):
    print "Line 2 - a is not equal to b"
else:
    print "Line 2 - a is equal to b"

if ( a    <>     b ):
    print "Line 3 - a is not equal to b"
else:
    print "Line 3 - a is equal to b"


if ( a      print "Line 4 - a is  less than b"
else:
    print "Line 4 - a is  not less than b"

if ( a > b ):
    print "Line 5 - a is  greater than b"
else:
    print "Line 5 - a is  not greater than b"

a = 5
b = 20
if ( a     print "Line 6 - a is either less than or equal to  b"
else:
   print "Line 6 - a is neither less than nor equal to  b"

if ( b >= a ):
   print "Line 7 - b is either greater than  or equal to b"
else:
   print "Line 7 - b is neither greater than  nor equal to b"

// 输出
Line 1 - a is not equal to b
Line 2 - a is not equal to b
Line 3 - a is not equal to b
Line 4 - a is  not less than b
Line 5 - a is  greater than b
Line 6 - a is either less than or equal to  b
Line 7 - b is either greater than  or equal to b
```


### Python赋值运算符 ###
以下假设变量a为10，变量b为20：


| 运算符  | 描述       | 实例                           |
| ---- | -------- | ---------------------------- |
| =    | 简单的赋值运算符 | c = a + b 将 a + b 的运算结果赋值为 c |
| +=   | 加法赋值运算符  | c += a 等效于 c = c + a         |
| -=   | 减法赋值运算符  | c -= a 等效于 c = c - a         |
| *=   | 乘法赋值运算符  | c *= a 等效于 c = c * a         |
| /=   | 除法赋值运算符  | c /= a 等效于 c = c / a         |
| %=   | 取模赋值运算符  | c %= a 等效于 c = c % a         |
| \**= | 幂赋值运算符   | c\*\*= a 等效于 c = c \*\* a    |
| //=  | 取整除赋值运算符 | c //= a 等效于 c = c // a       |

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

a = 21
b = 10
c = 0

c = a + b
print "Line 1 - Value of c is ", c

c += a
print "Line 2 - Value of c is ", c

c *= a
print "Line 3 - Value of c is ", c

c /= a
print "Line 4 - Value of c is ", c

c  = 2
c %= a
print "Line 5 - Value of c is ", c

c **= a
print "Line 6 - Value of c is ", c

c //= a
print "Line 7 - Value of c is ", c

// 结果
Line 1 - Value of c is  31
Line 2 - Value of c is  52
Line 3 - Value of c is  1092
Line 4 - Value of c is  52
Line 5 - Value of c is  2
Line 6 - Value of c is  2097152
Line 7 - Value of c is  99864
```


### Python位运算符 ###
按位运算符是把数字看作二进制来进行计算的。Python中的按位运算法则如下：
下表中变量 a 为 60，b 为 13。

| 运算符  | 描述                                       | 实例                                       |
| ---- | ---------------------------------------- | ---------------------------------------- |
| &    | 按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0 | (a & b) 输出结果 12 ，二进制解释： 0000 1100        |
| 1    | 按位或运算符：只要对应的二个二进位有一个为1时，结果位就为1。          | (a 1 b) 输出结果 61 ，二进制解释： 0011 1101        |
| ^    | 按位异或运算符：当两对应的二进位相异时，结果为1                 | (a ^ b) 输出结果 49 ，二进制解释： 0011 0001        |
| ~    | 按位取反运算符：对数据的每个二进制位取反,即把1变为0,把0变为1        | (~a ) 输出结果 -61 ，二进制解释： 1100 0011， 在一个有符号二进制数的补码形式 |
| >>   | 右移动运算符：把">>"左边的运算数的各二进位全部右移若干位，">>"右边的数指定移动的位数 | a >> 2 输出结果 15 ，二进制解释： 0000 1111         |

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

a = 60    // 60 = 0011 1100
b = 13    // 13 = 0000 1101
c = 0

c = a & b     // 12 = 0000 1100
print "Line 1 - Value of c is", c

c = a | b       // 61 = 0011 1101
print "Line 2 - Value of c is", c

c = a ^ b       // 49 = 0011 0001
print "Line 3 - Value of c is", c

c = ~a           // -61 = 1100 0011
print "Line 4 - Value of c is", c

c = a  print "Line 5 - Value of c is", c

c = a >> b      // 15 = 0000 1111
print "Line 6 - Value of c is", c

// 结果
Line 1 - Value of c is 12
Line 2 - Value of c is 61
Line 3 - Value of c is 49
Line 4 - Value of c is -61
Line 5 - Value of c is 491520
Line 6 - Value of c is 0
```

### Python逻辑运算符 ###
Python语言支持逻辑运算符，以下假设变量a为10，变量b为20：

| 运算符  | 描述                                       | 实例                    |
| ---- | ---------------------------------------- | --------------------- |
| and  | 布尔"与" - 如果x为False，x and y返回False，否则它返回y的计算值 | (a and b) 返回 true     |
| or   | 布尔"或" - 如果x是True，它返回True，否则它返回y的计算值      | (a or b) 返回 true      |
| not  | 布尔"非" - 如果x为True，返回False。如果x为False，它返回True | not(a and b) 返回 false |

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

a = 10
b = 20
c = 0

if ( a and b ):
   print "Line 1 - a and b are true"
else:
   print "Line 1 - Either a is not true or b is not true"

if ( a or b ):
   print "Line 2 - Either a is true or b is true or both are true"
else:
   print "Line 2 - Neither a is true nor b is true"


a = 0
if ( a and b ):
   print "Line 3 - a and b are true"
else:
   print "Line 3 - Either a is not true or b is not true"

if ( a or b ):
   print "Line 4 - Either a is true or b is true or both are true"
else:
   print "Line 4 - Neither a is true nor b is true"

if not( a and b ):
   print "Line 5 - Either a is not true or b is  not true or both are not true"
else:
   print "Line 5 - a and b are true"

// 输出
Line 1 - a and b are true
Line 2 - Either a is true or b is true or both are true
Line 3 - Either a is not true or b is not true
Line 4 - Either a is true or b is true or both are true
Line 5 - Either a is not true or b is  not true or both are not true
```


### Python成员运算符 ###

除了以上的一些运算符之外，Python还支持成员运算符，测试实例中包含了一系列的成员，包括字符串，列表或元组。

| 运算符    | 描述                             | 实例                          |
| ------ | ------------------------------ | --------------------------- |
| in     | 如果在指定的序列中找到值返回True，否则返回False   | x 在 y序列中 , 如果x在y序列中返回True   |
| not in | 如果在指定的序列中没有找到值返回True，否则返回False | x 不在 y序列中 , 如果x不在y序列中返回True |

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

a = 10
b = 20
list = [1, 2, 3, 4, 5 ];

if ( a in list ):
   print "Line 1 - a is available in the given list"
else:
   print "Line 1 - a is not available in the given list"

if ( b not in list ):
   print "Line 2 - b is not available in the given list"
else:
   print "Line 2 - b is available in the given list"

a = 2
if ( a in list ):
   print "Line 3 - a is available in the given list"
else:
   print "Line 3 - a is not available in the given list"

// 输出
Line 1 - a is not available in the given list
Line 2 - b is not available in the given list
Line 3 - a is available in the given list
```

### Python身份运算符 ###
身份运算符用于比较两个对象的存储单元

| 运算符      | 描述                       | 实例                                       |
| -------- | ------------------------ | ---------------------------------------- |
| is     | is 是判断两个标识符是不是引用自一个对象       | x is y, 如果 id(x) 等于 id(y) , is 返回结果 1    |
| is not   | is not是判断两个标识符是不是引用自不同对象 | x is not y, 如果 id(x) 不等于 id(y). is not 返回结果 1 |

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
a = 20
b = 20

if ( a is b ):
   print "Line 1 - a and b have same identity"
else:
   print "Line 1 - a and b do not have same identity"

if ( id(a) == id(b) ):
   print "Line 2 - a and b have same identity"
else:
   print "Line 2 - a and b do not have same identity"

b = 30
if ( a is b ):
   print "Line 3 - a and b have same identity"
else:
   print "Line 3 - a and b do not have same identity"

if ( a is not b ):
   print "Line 4 - a and b do not have same identity"
else:
   print "Line 4 - a and b have same identity"
   
// 输出
Line 1 - a and b have same identity
Line 2 - a and b have same identity
Line 3 - a and b do not have same identity
Line 4 - a and b do not have same identity
```

### Python运算符优先级 ### 
以下表格列出了从最高到最低优先级的所有运算符

| 运算符                      | 描述                                |
| ------------------------ | --------------------------------- |
| **                       | 指数 (最高优先级)                        |
| ~ + -                    | 按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@) |
| * / % //                 | 乘，除，取模和取整除                        |
| + -                      | 加法减法                              |
| \>\> <<                  | 右移，左移运算符                          |
| &                        | 位 'AND'                           |
| ^1                       | 位运算符                              |
| <= <> >=                 | 比较运算符                             |
| <>  == !=                | 等于运算符                             |
| = %= /= //= -= += *= **= | 赋值运算符                             |
| is is not                | 身份运算符                             |
| in not in                | 成员运算符                             |
| not or and               | 逻辑运算符                             |

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

a = 20
b = 10
c = 15
d = 5
e = 0

e = (a + b) * c / d       #( 30 * 15 ) / 5
print "Value of (a + b) * c / d is ",  e

e = ((a + b) * c) / d     # (30 * 15 ) / 5
print "Value of ((a + b) * c) / d is ",  e

e = (a + b) * (c / d);    # (30) * (15/5)
print "Value of (a + b) * (c / d) is ",  e

e = a + (b * c) / d;      #  20 + (150/5)
print "Value of a + (b * c) / d is ",  e


//输出
Value of (a + b) * c / d is  90
Value of ((a + b) * c) / d is  90
Value of (a + b) * (c / d) is  90
Value of a + (b * c) / d is  50
```

---
** [DigitalOcean的VPS，稳定、便宜，用于搭建自己的站点和梯子，现在注册即得10$,免费玩2个月](https://www.digitalocean.com/?refcode=9e4ab85e22ec) **
