## python变量和数据类型 ##

### 变量类型 ###
变量是存储在内存中的值，基于变量的类型，解释器会分配指定内存。变量可以指定不同的数据类型，这些变量可以是数字或者字符串。

### 变量赋值 ###
Python中的变量不需要声明，变量的赋值操作既是变量声明和定义的过程
每个变量在内存中创建，包括变量的标识、名称和数据
每个变量只是用钱都必须赋值，变量赋值之后变量才会被创建
等号（=）用来被变量赋值

赋值方法
```python
// 简单赋值 Variable = Value
count = 100       // 整数赋值
miles = 1000.0    // 浮点数赋值 
name = "John"     // 字符串赋值

// 多变量赋值，元组和列表赋值语句
Variable1,Variable2,...=Value1,Value2,...
a = b = c = 1
a, b , c = 1, 2 , "John"


// 多目标赋值 a = b = Variable (多个变量内存中指向同一个对象，对于可变类型的需要，修改一个会对其他影响)
s = h = 'spam'

// 自变赋值 +=、-=、*= 自变赋值会修改原始对象，而不是新创建对象
s += 42
x += y
```

### 数据类型 ###
不同的数据，需要定义为不同的数据类型，在Python中有五中标准数据类型Numbers、String、List、Tuple、Dictionary

#### 数字 ####
数字数据类型用于存储数值，他们是不可改变的数据类型，通常的int、long、folat、complex等都被支持，并且会根据具体数字来定义变量的类型
```python
// stored as int type
num = 1 
// stored as long int type
num = 11111111111
// stored as float type
num = 1.0
// L stands for long type
num = 12L
// j stands for complex type
num = 1 + 12j
// string type
num = '1'
```

#### 字符串 ####
字符串是有数字、字母、下划线组成的一串字符。Python的字串列表有两种取值顺序，从左到右索引从0开始，从右到左索引-1开始。`单引号、双引号和三引号都可以来定义字符串。三引号可以定义特殊格式的字符串。字符串作为一个序列类型，支持索引访问和切片访问。
```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

str = 'Hello world!'

print str                   // 完整字符串
print str[0]                // 输出字符串第一个字符
print str[0] + str [2:5]    // 输出字符串第一个字符和第三-第五的字符
print str[2:5]              // 输出字符串第三到第五之剑的字符串
print str[2:]               // 输出从第三字符开始的字符串
print str[:4]               // 输出到第四个字符的字符串
print str[::2]              // 以2为间隔输出字符串
print str[-1]               // 输出随后一个字符
print str * 2               // 输出2次字符串
print str + "Test"          // 输出连接的字符串

//执行结果
Hello world!
H
Hllo
llo
llo world!
Hell
Hlowrd
!
Hello world!Hello world!
Hello world!Test
```

#### 布尔值 ####
布尔值和布尔代数的表示完全一致，一个布尔值只有`True`、`False`两只值，在Python中，可以直接用Ture、False（注意大小写），也可以通过布尔运算计算出来。
布尔值可以用`and`，`or`和`not`运算

* `and` 运算是与运算，只有所有都为True，and运算符才是`True`

* `or` 运算是或运算，只要其中一个为True，or运算结果就是`True`
* `not` 运算是非运算，他是一个单目运算符，把True变成`False`

```python
// 三种布尔表达式运算符
x and y
x or y
not x
```

```python
\\真值表
对象/常量 值
""       假
"string" 真 
2>=1     真
-2 ()空元组  假
[]空列表  假
{}空字典  假
None     假
```

#### 空值 ####
空值是Python里一个特殊的值，用`None`表示，None不能理解为0，因为0是有意义的，而None是一个特殊的空值

#### Python 列表 ####
List 可以完成大多数集合类型的数据结构实现，它支持字符、数组、字符串甚至可以嵌套列表
列表使用[]标示，是Python最通用的复合数据类型
```python
// 脚
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

list = [ 'abcd', 786, 2.33, 'John', 70.2 ]
tinylist = [ 123, 'john' ]

print list                  // 输出完整列表
print list[0]               // 输出列表的第一个元素
print list[1:3]             // 输出列表第二至第三的元素
print list[2:]              // 输出从第三个开始至末尾的所有元素
print tinylist *2           // 输出列表两次
print list + tinylist       // 输出组合列表

// 执行结果
['abcd', 786, 2.33, 'John', 70.2]
abcd
[786, 2.33]
[2.33, 'John', 70.2]
[123, 'john', 123, 'john']
['abcd', 786, 2.33, 'John', 70.2, 123, 'john']
```


#### Python元组 ####
元组是另一个数据类型，类似与List
元组用`()`标示。内部元素用逗号相隔，元素不能二次赋值，相当于只读列表
```python
// 脚本内容
#!/usr/bin/env python
# -*- coding: UTF-8
tuple = ( 'abcd', 768, 2.23, 'john', 70.2 )
tinytuple = ( 123, 'john' )

print tuple                   //输出完整元组
print tuple[0]                //元组的第一个元素
print tuple[1:3]              //元组的第二个到二三个元素
print tuple[2:]               //元第三个到最后一个元素
print tinytuple*2             //输出两次元组
print tuple + tinytuple       //打印两个元组的组合


// 执行结果
python tuple.py 
('abcd', 768, 2.23, 'john', 70.2)
abcd
(768, 2.23)
(2.23, 'john', 70.2)
(123, 'john', 123, 'john')
('abcd', 768, 2.23, 'john', 70.2, 123, 'john')
```

#### Python 元字典#### 
字典dictionary是除列表以外python中最为灵活的内置数据结构类型。列表是有序的对象结合，字典是无序的对象集合。两者之间的区别在于:字典当中的元素是通过键来存取，而不是通过偏移存取，字典用`{}`标识，字典由索引eky和对应的值value组成
```python
// 脚本内容
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
dict = {}                             
dict['one'] = "This is on"                                
dict[2] = "This is two"                                   
tinydict = {'name': 'john', 'code':6734, 'dept': 'sales'} 

print dict['one']           //输出key为one的值                                     
print dict[2]               //输出key为2的值
print tinydict              //输出完整字典
print tinydict.keys()       // 输出所有key
print tinydict.values()     //输出所有value

// 输出结果
This is on 
This is two
{'dept': 'sales', 'code': 6734, 'name': 'john'}
['dept', 'code', 'name']
['sales', 6734, 'john']
```

#### 数据类型转换 ####
有时候，需要对数据内置的类型进行转换，数据类型的转换，只需要将数据类型作为函数名即可，下面是几个内置函数可以执行数据类型转换，这些函数返回一个新的对象，表示转换的值。

| 函数                    | 描述                              |
| --------------------- | ------------------------------- |
| int(x [,base])        | 将x转换为一个整数                       |
| long(x [,base] )      | 将x转换为一个长整数                      |
| float(x)              | 将x转换到一个浮点数                      |
| complex(real [,imag]) | 创建一个复数                          |
| str(x)                | 将对象 x 转换为字符串                    |
| repr(x)               | 将对象 x 转换为表达式字符串                 |
| eval(str)             | 用来计算在字符串中的有效Python表达式,并返回一个对象   |
| tuple(s)              | 将序列 s 转换为一个元组                   |
| list(s)               | 将序列 s 转换为一个列表                   |
| set(s)                | 转换为可变集合                         |
| dict(d)               | 创建一个字典。d 必须是一个序列 (key,value)元组。 |
| frozenset(s)          | 转换为不可变集合                        |
| chr(x)                | 将一个整数转换为一个字符                    |
| unichr(x)             | 将一个整数转换为Unicode字符               |
| ord(x)                | 将一个字符转换为它的整数值                   |
| hex(x)                | 将一个整数转换为一个十六进制字符串               |
| oct(x)                | 将一个整数转换为一个八进制字符串                |
