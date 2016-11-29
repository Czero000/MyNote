### Python 列表(Lists)

序列是Python中最基本的数据结构。序列中的每个元素都分配一个数字 ,它的位置或索引，以0开头，依此类推。

Python有6个序列的内置类型，但最常见的是列表和元组。序列都可以进行包括索引，切片，加，乘，检查成员等操作。此外，Python已经内置确定序列的长度以及确定最大和最小的元素的方法。列表是最常用的Python数据类型，它可以作为一个方括号内的逗号分隔值出现。列表的数据项不需要具有相同的类型

创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可。

```
list1 = ['physics', 'chemistry', 1997, 2000];
list2 = [1, 2, 3, 4, 5 ];
list3 = ["a", "b", "c", "d"];
```

与字符串的索引一样，列表索引从0开始。列表可以进行截取、组合等。

---

#### 访问列表中的值

使用下标索引来访问列表中的值，同样可以使用方括号的形式截取字符

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7]

print "List1[0] :" , list1[0]
print "List2[1:5] :", list2[1:5]

//输出
List1[0] : physics
List2[1:5] : [2, 3, 4, 5]
```

---

#### 更新列表

可以对`list`的数据项进行修改或更新，也可以使用`append()`方法来添加列表项

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

list = ['physics', 'chemistry', 1997, 2000];
print "Value available at index 2 :"
print list[2];
list[2] = 2001;
print "New value available at index 2: "
print list[2];

// 输出
Value available at index 2 :
1997
New value available at index 2:
2001
```

---

#### 删除列表元素

使用del语句来删除列表元素，也可以通过`remove()`方法操作

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8

list = [ 'physics', 'chemistry', 1997, 2000 ]
print list;
del list[2];
print "After deleting value at index 2:"
print list

// 输出
['physics', 'chemistry', 1997, 2000]
After deleting value at index 2:
['physics', 'chemistry', 2000]
```

---

#### python列表脚本操作符

列表对`+`和`*` 的操作符与字符串相似，`+`用于组合列表，`*`用于重复列表

| Python 表达式                   | 结果                           | 描述         |
| ---------------------------- | ---------------------------- | ---------- |
| len([1, 2, 3])               | 3                            | 长度         |
| [1, 2, 3] + [4, 5, 6]        | [1, 2, 3, 4, 5, 6]           | 组合         |
| ['Hi!'] * 4                  | ['Hi!', 'Hi!', 'Hi!', 'Hi!'] | 重复         |
| 3 in [1, 2, 3]               | True                         | 元素是否存在于列表中 |
| for x in [1, 2, 3]: print x, | 1 2 3                        | 迭代         |

---

#### Python列表截取

Python的列表截取与字符串操作类型，如下所示：

```
L = ['spam', 'Spam', 'SPAM!']
```

操作：

| Python 表达式 | 结果                | 描述           |
| ---------- | ----------------- | ------------ |
| L[2]       | 'SPAM!'           | 读取列表中第三个元素   |
| L[-2]      | 'Spam'            | 读取列表中倒数第二个元素 |
| L[1:]      | ['Spam', 'SPAM!'] | 从第二个元素开始截取列表 |

---

#### Python 列表函数和方法

Python包含下面函数

| 序号   | 函数                           |
| ---- | ---------------------------- |
| 1    | [cmp(list1, list2)]比较两个列表的元素 |
| 2    | [len(list)]列表元素个数            |
| 3    | [max(list)]返回列表元素最大值         |
| 4    | [min(list)]返回列表元素最小值         |
| 5    | [list(seq)]将元组转换为列表          |

- list cmp()

描述：`cmp()`用于比较两个列表的元素

语法： `cmp(list1, list2)`

返回值：如果比较的元素是同类行，则比较其值，返回结构；如果不是同一类型，则检查他们是否是数字；如果是数字，则执行比较的数字强制转换，然后比较；如果一方元素是数字，则另一方的元素大；否则通过类型的名字字母顺序比较。如果由一个列表首先到达末尾，则另一个列表大；如果以上都相同，则返回`0`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
list1, list2 = [123, 'xyz'], [456, 'abc']
print cmp(list1, list2)
print cmp(list2, list1)
list3 = list2 + [786]
print cmp(list2, list3)

//输出
-1
1
-1
```

- list len()

描述：`len()`返回列表元素个数

语法：`len(list)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
list1, list2 = [123, 'xyz', 'zero'],[456, 'abc' ]

print "First list length :", len(list1);
print "Second list lenth :", len(list2);

// 输出
First list length : 3
Second list lenth : 2
```

- list max()

描述：max()返回列表元素的最大值

语法：`max(list)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
list1, list2 = [123, 'xyz', 'zero', 'abc'], [456, 700, 200]

print "Max value element :", max(list1);
print "Max value element :", max(list2);

// 输出
Max value element : zero
Max value element : 700
```

- list min()

描述：`min()`返回列表元素的最小值

语法：`min(list)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
list1, list2 = [123, 'xyz', 'zero', 'abc'], [456, 700, 200]

print "Min value element :", min(list1);
print "Min value element :", min(list2);

// 输出
Max value element : 123
Max value element : 200
```

- list list()

描述：`list()`用于将元组转换为列表。元组与列表非常相似，区别在于元组的元素值不能修改，元组是放在括号中，列表是放于方括号中。

语法：`list(seq)`

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aTuple = ('123', 'xyz', 'zero', 'abc');
aList = list(aTuple);
print "List elements :", aList

//输出
List elements : ['123', 'xyz', 'zero', 'abc']
```

---

Python包含以下方法

| 序号   | 方法                                       |
| ---- | ---------------------------------------- |
| 1    | [list.append(obj)]在列表末尾添加新的对象            |
| 2    | [list.count(obj)]统计某个元素在列表中出现的次数         |
| 3    | [list.extend(seq)]在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表） |
| 4    | [list.index(obj)]从列表中找出某个值第一个匹配项的索引位置    |
| 5    | [list.insert(index, obj)]将对象插入列表         |
| 6    | [list.pop(obj=list[-\])]移除列表中的一个元素（默认最后一个元素），并且返回该元素的值 |
| 7    | [list.remove(obj)]移除列表中某个值的第一个匹配项        |
| 8    | [list.reverse()]反向列表中元素                  |
| 9    | [list.sort([fun\])]对原列表进行排序              |



- list append()

描述：`append()`用于在列表末尾添加新的对象

语法：`list.append(obj)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aList = [123, 'xyz', 'zero', 'abc'];
aList.append(2009);
print "Update List :", aLis

//输出
Update List : [123, 'xyz', 'zero', 'abc', 2009]
```



- list count()

描述：`conut()`用于统计某个元素在列表中出现的次数

语法：`list.count(obj)`

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zero', 'abc', 123];
print "Count for 123 :", aList.count(123);
print "Count for zero :", aList.count('zero');

//输出
Count for 123 : 2
Count for zero : 1
```

- list extend()

描述：`extend()`函数用于在列表末尾一次性追加应一个序列的多个值

语法：`list.extend(seq)`

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zero', 'abc', 123];
bList = [2009, 'mini'];
aList.extend(bList)
print "Extend list :",aList;

//输出
Extend list : [123, 'xyz', 'zero', 'abc', 123, 2009, 'mini']
```

* list index()

描述：`index()`用于从列表中找出某个值第一个匹配项的索引位置

语法：`list.index(obj)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aList = [123, 'xyz', 'zero', 'abc'];
print "Index for xyz :", aList.index('xyz');
print "Index for zero :", aList.index('zero');
//输出
Index for xyz : 1
Index for zero : 2
```

- list insert()

描述：`insert()`用于将指定对象插入列表

语法：`list.insert(index, obj)`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

aList = [123, 'xyz', 'zero', 'abc'];
aList.insert(3, 2009);
print "Final List :", aList
// 输出
Final List : [123, 'xyz', 'zero', 2009, 'abc']
```

- list pop()

描述：`pop()`用于移除列表中的一个元素，默认是最后一个元素，并返回该元素的值

语法：`list.pop(obj=list[-1])`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zero', 'abc'];
print 'A List :', aList.pop();
print 'A list :', aList.pop(2);
print aList
// 输出
A List : abc
A list : zero
[123, 'xyz']
```

- list remove()

描述：`remove()`用于移除列表中某个值的第一个匹配值

语法：`list.remove(obj)`

```
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zero', 'abc', 'xyz'];
aList.remove('xyz');
print "List :", aList;
aList.remove('abc');
print "List :", aList;

// 输出
List : [123, 'zero', 'abc', 'xyz']
List : [123, 'zero', 'xyz']
```

- list reverse()

描述：`reverse()`用于反向列表中的元素

语法：`list.reverse()`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zara', 'abc', 'xyz'];
aList.reverse()
print "List :", aList;

//输出
List : ['xyz', 'abc', 'zara', 'xyz', 123]
```

- list sort()

描述：`sort()`用于对原序列排序，如果指定参数，则使用比较函数指定的比较函数

语法：`list.sort([func])`

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
aList = [123, 'xyz', 'zara', 'abc', 'xyz'];
aList.sort();
print "List: ", aList
//输出
List:  [123, 'abc', 'xyz', 'xyz', 'zara']
```
