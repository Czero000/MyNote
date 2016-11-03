
### Python循环语句 ###

编程语言提供了各种控制结构，允许更为复杂的执行路径。循环语句允许执行一个语句或者语句组，下面是大多数编程语言中的循环语句的一般形式。

 ![loop_architecture](http://ofc9x1ccn.bkt.clouddn.com/python/loop_architecture.jpg)

Python提供了for循环和while循环（Python中没有do--while循环）

| 循环类型    | 描述                       |
| ------- | ------------------------ |
| while循环 | 在给定判断条件为true时执行循环，否则退出循环 |
| for循环   | 重复执行语句                   |
| 嵌套循环    | 在while循环中嵌套执行for循环       |


#### while 循环 ####
python编程中while语句用于循环执行程序，在某个条件下，循环执行某段程序，以处理需要重复处理的相同任务，基本形式如下

```python
while 判断条件:
    执行语句		
```

循环语句可以是单个语句或者是语句块。判断条件可以是任意表达式、任何非零、非空的值均为true。当判断条件false时，循环结束。

 ![python_while_loop](http://ofc9x1ccn.bkt.clouddn.com/python/python_while_loop.jpg)

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

count = 0
while (count <9):
    print 'The count is:', count
    count += 1

print 'Good Bye'

// 输出
The count is: 0
The count is: 1
The count is: 2
The count is: 3
The count is: 4
The count is: 5
The count is: 6
The count is: 7
The count is: 8
Good Bye
```

while语句还有另外两个重要的命令`continue`、`break`来跳过循环，`continue`用于跳过该次循环，`break`则是用于退出循环，此外，判断条件还可以是个常量，表示循环必定成立，如下

```python
//脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
i = 1
while i < 10:
    i += 1
    if i%2 > 0:     // 非双时跳出输出
        continue
    print i        // 输出2、4、6、8、10

i = 1
while 1:            // 循环条件为1必定成立
    print i         //输出1-10
    i += 1
    if i > 10:
        break      // 当大于10跳出循环

```

##### 无限循环 #####

如果条件判断语句永远为true，循环永远为true，循环将无限执行

```Python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
var = 1
while var == 1:
    num = raw_input("Enter a number :")
    print "You entered: ", num
print "GoodBye"     
```

**注意：** 以上的无限循环你可以使用 CTRL+C 来中断循环

##### 循环使用else语句
在 python 中，for … else 表示这样的意思，for 中的语句和普通的没有区别，else 中的语句会在循环正常执行完（即 for 不是通过 break 跳出而中断的）的情况下执行，while … else 也是一样。

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
count = 0
while count < 5:
    print count, " is less than 5"
    count += 1
else:
    print count, " is not less 5"

//输出
0  is less than 5
1  is less than 5
2  is less than 5
3  is less than 5
4  is less than 5
5  is not less 5
```

##### 简单的语句组
类似if语句的语法，如果你的while循环体中只有一条语句，你可以将该语句与while写在同一行

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
flag = 1

while (flag): print "Given flag is really true"
print "GoodBye"
```

---

#### Python for循环

python for循环可以遍历任何序列的项目，如一个列表或者一个字符串。

```python
for iterating_var in sequence:
    statements(s)
```

 ![python_for_loop](http://ofc9x1ccn.bkt.clouddn.com/python/python_for_loop.jpg)

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
for letter in 'Python':                       // 字符串循环
    print '当前字母 :', letter

fruits = ['banana', 'apple', 'mango']         // 列表循环
for fruits in fruits:
    print '当前字母 :', fruits

print "GoodBye"

//输出
前字母 : P
当前字母 : y
当前字母 : t
当前字母 : h
当前字母 : o
当前字母 : n
当前字母 : banana
当前字母 : apple
当前字母 : mango
GoodBye
```

##### 通过序列索引迭代

另外一种执行循环的遍历方式是通过索引

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fruits = ['banana', 'apple', 'mango']

for index in range(len(fruits)):
    print '当前水果 :', fruits[index]

print "GoodBye"

//输出
当前水果 : banana
当前水果 : apple
当前水果 : mango
GoodBye
```

以上实例使用了内置函数 len() 和 range(),函数 len() 返回列表的长度，即元素的个数。 range返回一个序列的数。



##### 循环使用else语句

```python
//脚本
#!/usr/bin/python
# -*- coding: UTF-8 -*-

for num in range(10,20):  # 迭代 10 到 20 之间的数字
   for i in range(2,num): # 根据因子迭代
      if num%i == 0:      # 确定第一个因子
         j=num/i          # 计算第二个因子
         print '%d 等于 %d * %d' % (num,i,j)
         break            # 跳出当前循环
   else:                  # 循环的 else 部分
      print num, '是一个质数'

//输出
10 等于 2 * 5
11 是一个质数
12 等于 2 * 6
13 是一个质数
14 等于 2 * 7
15 等于 3 * 5
16 等于 2 * 8
17 是一个质数
18 等于 2 * 9
19 是一个质数
```

---

#### Python嵌套循环

Python允许在一个循环体中嵌入另外一个循环。

```python
// for循环嵌套
for iterating_var in sequence:
    for iterating_var in sequence:
        statements(s)
    statements(s)

// while循环嵌套
while expression:
    while expression:
        statement(s)
    statement(s)
```

可以在循环体内迁入其他循环体，比如在while循环中嵌入for循环，反之亦可。

例如嵌套循环输出2-100之间的素数

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

i = 2
while(i<100):
    j = 2
    while(j <= (i/j)):
        if not(i%j): break
        j += 1
    if (j > i/j): print i," 是素数"
    i += 1
print "GoodBye"
```



---

### 循环控制语句

循环控制语句可以更改语句执行顺序。Python支持下面循环控制语句

| 控制语句       | 描述                            |
| ---------- | ----------------------------- |
| break语句    | 在语句块执行过程中终止循环，并且跳出整个循环        |
| continue语句 | 在语句块执行过程中终止当前循环，跳出该次循环，执行下次循环 |
| pass语句     | pass是空语句，是为了保持程序结构的完整性        |

#### Python break语句

python `break`语句是用来终止循环语句，即循环条件没有`false`条件或者序列还没有完全递归完，也会停止执行循环语句。`break`语句用在`while`和`for`循环中。如果使用嵌套循环，break语句将停止执行最深层的循环，并执行下一行代码。

 ![cpp_break_statement](http://ofc9x1ccn.bkt.clouddn.com/python/cpp_break_statement.jpg)

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
for letter in 'Python':
    if letter == 'h':
        break
    print 'Current Letter :', letter

var = 10
while var > 0:
    print 'Current variable value :', var
    var -= 1
    if var == 5:
        break

print "GoodBye"

// 输出
Current Letter : P
Current Letter : y
Current Letter : t
Current variable value : 10
Current variable value : 9
Current variable value : 8
Current variable value : 7
Current variable value : 6
GoodBye
```

#### python continue语句

python continue语句跳出本次循环，而break跳出整个循环。`continue`语句用来告诉python跳出当前循环的剩余语句，然后继续进行下一轮循环，`continue`同样可以用在`while`和`for`循环中

 ![cpp_continue_statement](http://ofc9x1ccn.bkt.clouddn.com/python/cpp_continue_statement.jpg)

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

for letter in 'Python':
    if letter == 'h':
        continue
    print '当前字母 :', letter

var = 10
while var > 0:
    var -= 1
    if var == 5:
        continue
    print '当前变量 :', var
print 'GoodBye'

// 输出
当前字母 : P
当前字母 : y
当前字母 : t
当前字母 : o
当前字母 : n
当前变量 : 9
当前变量 : 8
当前变量 : 7
当前变量 : 6
当前变量 : 4
当前变量 : 3
当前变量 : 2
当前变量 : 1
当前变量 : 0
GoodBye
```

#### python pass语句

pass语句是空语句，是为了保持程序结构的完整性，pass 不做任何事情，一般用作占位语句。

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
for letter in 'Python':
    if letter == 'h':
        pass
        print '这是pass 块'
    print '当前字母 :', letter
print "GoodBye"

// 输出
当前字母 : P
当前字母 : y
当前字母 : t
这是pass 块
当前字母 : h
当前字母 : o
当前字母 : n
GoodBye
```
