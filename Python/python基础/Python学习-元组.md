### Python元组

Python的元组与列表相似，不同之处在于元组的元素不能修改。元组使用小括号，列表使用中括号。元组创建简单，只要在括号内添加元素，并用逗号隔开即可。

```python
tup1 = ('physics', 'chemistry', 1997, 2000);
tup2 = (1, 2, 3, 4, 5);
tup3 = "a", "b", "c", "d";
tup4 = ();   //空元组
tup5 = (50,) //元组只包含一个元素时，需要在元素后面添加逗号
```

---

### 访问、修改元组

元组与字符串类似，下标索引从0开始，可以进行截取、组合。元组中的元素不允许修改，但是可以通过对元组进行连接组合来实现对元组的修改。

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8
tup1 = ('physics', 'chemistry', 1997, 2000);
tup2 = (1, 2, 3, 4, 5);
tup3 = "a", "b", "c", "d";

print "tup1[0]: ",tup1[0]
print "tup2[1:5]: ",tup2[1:5]
print "tup2[2:]: ",tup2[2:]
print "tup2 + tup3 :", tup2 + tup3
print "double tup2 :", tup2 * 2

// 输出
tup1[0]:  physics
tup2[1:5]:  (2, 3, 4, 5)
tup2[2:]:  (3, 4, 5)
tup2 + tup3 : (1, 2, 3, 4, 5, 'a', 'b', 'c', 'd')
double tup2 : (1, 2, 3, 4, 5, 1, 2, 3, 4, 5)
```

---

#### 删除元组

元组中的元素值不允许删除，可以使用`del`语句来删除整个元组。

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tup = ('physics', 'chemistry', 1997, 2000);

print tup;
del tup;
print "After deleting tup :", tup;
//输出
('physics', 'chemistry', 1997, 2000)
After deleting tup :
Traceback (most recent call last):
  File "tuple_del.py", line 8, in <module>
    print "After deleting tup :", tup;
NameError: name 'tup' is not defined
```

**元组被删除之后，输出变量会有异常信息**

---

#### 元组运算符

与字符串一样，元组之间可以使用`+`和`*`进行运算，通过组合和复制，生成新的元组。

| Python 表达式                   | 结果                           | 描述     |
| ---------------------------- | ---------------------------- | ------ |
| len((1, 2, 3))               | 3                            | 计算元素个数 |
| (1, 2, 3) + (4, 5, 6)        | (1, 2, 3, 4, 5, 6)           | 连接     |
| ['Hi!'] * 4                  | ['Hi!', 'Hi!', 'Hi!', 'Hi!'] | 复制     |
| 3 in (1, 2, 3)               | True                         | 元素是否存在 |
| for x in (1, 2, 3): print x, | 1 2 3                        | 迭代     |

---

#### 元组索引、截取

因为元组也是一个序列，所以可以访问元组中的指定位置的元素，也可以截取索引的一段元素。

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aTuple = ('physics', 'chemistry', 1997, 2000); //元组

print "aTuple :", aTuple;                     //打印整个元组
print "aTuple[2] :", aTuple[2];               // 打印第三个元素
print "aTuple[-2] :", aTuple[-2];             // 反向读取倒数第二个元素
print "aTuple[1:] :", aTuple[1:];            // 截取元素

// 输出
aTuple : ('physics', 'chemistry', 1997, 2000)
aTuple[2] : 1997
aTuple[-2] : 1997
aTuple[1:] : ('chemistry', 1997, 2000)
```

---

#### 无关闭分隔符

任何无符号的对象，以逗号分隔，默认为元组

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8
x = 'abc', -4.24e93, 18+6.6j, 'xyz';
print x
x, y = 1, 2;
print "Value of x, y :", x, y;
// 输出
('abc', -4.24e+93, (18+6.6j), 'xyz')
Value of x, y : 1 2
```

---

#### 元组内置变量

Python元组包含了以下内置函数

| 序号   | 方法及描述                          |
| ---- | ------------------------------ |
| 1    | [cmp(tuple1, tuple2)]比较两个元组元素。 |
| 2    | [len(tuple)计算元组元素个数。           |
| 3    | [max(tuple)]返回元组中元素最大值。        |
| 4    | [min(tuple)]返回元组中元素最小值。        |
| 5    | [tuple(seq)]将列表转换为元组。          |

* 元组cmp()

描述：Python元组cmp()函数用于比较两个元组元素。

语法：cmp(tuple1, tuple2)

返回值：如果比较的元素是同类型的,则比较其值,返回结果。如果两个元素不是同一种类型,则检查它们是否是数字。如果是数字,执行必要的数字强制类型转换,然后比较；如果有一方的元素是数字,则另一方的元素"大"(数字是"最小的")；否则,通过类型名字的字母顺序进行比较；如果有一个列表首先到达末尾,则另一个长一点的列表"大"；如果我们用尽了两个列表的元素而且所 有元素都是相等的,那么结果就是个平局,就是说返回一个 0。

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
tuple1, tuple2 = (123, 'xyz'), (456, 'abc');

print cmp(tuple1, tuple2);
print cmp(tuple2, tuple1);
tuple3 = tuple2 + (768,);
print cmp(tuple2, tuple3);
//输出
-1
1
-1
```

* 元组len()

描述：Python 元组 len() 函数计算元组元素个数。

语法：`len(tuple1, tuple2)

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
tuple1, tuple2 = (123, 'xyz', 'zero'), (456, 'abc');

print 'First tuple length :', len(tuple1);
print 'Second tuple length :', len(tuple2);
//输出
First tuple length : 3
Second tuple length : 2
```

* 元组max()

描述： max()返回元组中元素的最大值

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
tuple1, tuple2 = (123, 'xyz', 'zero', 'abc'), (456, 700, 200)

print "Max value element :", max(tuple1);
print "Max value element :", max(tuple2);
//输出
Max value element : zero
Max value element : 700
```

* 元组min()

描述： min()返回元组中元素的最小值

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
tuple1, tuple2 = (123, 'xyz', 'zero', 'abc'), (456, 700, 200)

print "Min value element :", min(tuple1);
print "Min value element :", min(tuple2);
//输出
Min value element : 123
Min value element : 200
```

* 元组tuple()

描述：tuple()函数将列表转换为元组

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aTuple = tuple([1, 2, 3, 4]);
bTuple = tuple({1:2,3:4});           //针对字典 会返回字典的key组成的tuple
cTuple = tuple((1, 2, 3, 4,));       // 元组会返回元组自身

print aTuple;
print bTuple;
print cTuple;
//输出
(1, 2, 3, 4)
(1, 3)
(1, 2, 3, 4)
```
