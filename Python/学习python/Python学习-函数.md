### Python函数

函数是组织好的，可以重新使用，用来实现单一或者相关联功能的代码块。函数能提高应用的模块性和代码的重复利用率。

#### 定义一个函数

可以定义一个自己想要功能的函数，下面是简单的规则

- 函数代码以def关键词开头，后接函数标识符名称和圆括号`()`
- 任何传入参数和自变量必须放在圆括号中间，圆括号之间可以用于定义参数
- 函数的第一行语句可以选择性的使用文档字符串--用于存放函数说明
- 函数内容以冒号其实，并且缩进
- Return[expression]结束函数，选择性的返回一个值给调用方。不带表达式的return相当于返回None

##### 语法

```python
def functionname ( parameters ):
    "函数_文档字符串"
    function_suite
    return [expression]
```

默认情况下，参数值和参数名称是按函数声明中定义的顺序匹配

##### 实例

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printme( str ):
    "打印传入的字符串到标准显示设备"
    print str
    return
```

---

#### 函数调用

定义一个函数只给了函数一个名称，指定了函数里包含的参数和代码块结构。函数的基本结构完成之后，可以通过另一个函数调用执行，也可以直接从python提示符执行。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printme( str ):
    "打印传入的字符串到标准显示设备"
    print str
    return

printme("我要调用用户自定义函数!");
printme("再次调用同一函数");

//输出
我要调用用户自定义函数!
再次调用同一函数
```

---

#### 按值传递参数和按引用传递参数

所有参数在python里都是按引用传递。如果在函数中修改了参数，那么调用这个函数的函数里，原始的参数也被改变。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def changeme( mylist ):
    mylist.append([1,2,3,4]);
    print "函数内取值: ", mylist
    return

mylist = [10, 20, 30];
changeme( mylist );
print "函数外取值: ", mylist

//输出
函数内取值:  [10, 20, 30, [1, 2, 3, 4]]
函数外取值:  [10, 20, 30, [1, 2, 3, 4]]
```

---

#### 参数

调用参数时可以使用的正式参数类型：

- 必备参数
- 命名参数
- 缺省参数
- 不定长参数

##### 必备参数

必备参数须以正确的顺从传入函数。调用时的数量必须和声明时一样。调用`printme()`，必须传入一个参数，不认会出现语法错误：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printme( str ):
    "打印传入的字符串到标准显示设备"
    print str
    return

printme("我要调用用户自定义函数!");
printme("再次调用同一函数");
printme();

//输出、
我要调用用户自定义函数!
再次调用同一函数
Traceback (most recent call last):
  File "function_1.py", line 11, in <module>
    printme();
TypeError: printme() takes exactly 1 argument (0 given)
```

命名参数

命名参数和函数调用关系紧密，调用方用参数的命名确认传入的参数值。可以跳过不传的参数或者乱序传参，因为python解释器能够用参数名匹配参数值。用命名参数调用printme()函数：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printme( str ):
    "打印传入的字符串到标准显示设备"
    print str
    return

printme(str= "My string");
//输出
My string
```

```python
//命名参数的顺序不重要
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printinfo(name, age):
    print "Name: ", name;
    print "Age: ", age;
    return;

printinfo(age=50, name="Charlie")
//输出
Name:  Charlie
Age:  50
```

##### 缺省参数

调用参数时，缺省参数的值如果没有传入，则被认为是默认值。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printinfo(name, age=50):
    print "Name: ", name;
    print "Age: ", age;
    return;

printinfo(age=50, name="Charlie")
printinfo(name="Charlie")

//输出
Name:  Charlie
Age:  50
Name:  Charlie
Age:  50
```

##### 不定长参数

如果需要一个函数能处理比当初声明时更多的参数，这样的参数叫做不定长参数。和上面两种不同，声明时不会命名。

```python
def functiononname([formal_args,] *var_args_tuple):
    function_suite
    rerurn [expression]
```

加了`*`的变量名会存放所有未命名的变量参数

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def printinfo(arg1, *vartuple):
    print "输出:"
    print arg1
    for var in vartuple:
        print var
    return;

printinfo(10)
printinfo(70, 60, 50)

//输出
输出:
10
输出:
70
60
50
```

#### 匿名函数

python使用`lambda`来命名匿名函数

- lambda只是一个表达式，函数体比`def`简单
- lambda的主体是一个表达式，而不是一个代码块，仅仅在lambda表达式中封装有限的逻辑进去
- lambda函数有自己的命名空间，且不能访问自有参数列表之外或全局命名空间里的参数
- lambda看起来只能写一行，却不等同于`C`或`C++`内联函数，后者的目的是调小函数时不占用栈内存从而增加运行效率

语法：

```python
lambda [arg1 [,arg2....]]:expression
```

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

sum = lambda arg1, arg2: arg1 + arg2;

print "相加后的值: ", sum(10, 20)
print "相加后的值: ", sum(20, 20)

//输出
相加后的值:  30
相加后的值:  40
```

---

#### return语句

return语句[表到式]退出函数，选择性的向调用方返回一个表达式。不带参数值的retrun语句返回`None`。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
def sum(arg1, arg2):
    total = arg1 + arg2
    print "函数内 :", total
    return total;

total = sum(10, 20);
print "函数外 :", total

// 输出
函数内 : 30
函数外 : 30
```

---

#### 变量作用域

一个程序的所有变量并不是在哪个位置都可以访问。访问权限决定与这个变量是在哪里赋值。变量的作用域决定了在那一部分程序你可以访问哪个特定的变量名称。两种最基本的变量作用域如下：

- 全局变量


- 局部变量

##### 变量和局部变量

定义在函数内部的变量拥有一个局域作用域，定义在函数外的拥于全局作用域。

局部变量只能在其声明的函数内部访问，而全局变量可以在整个程序范围内访问。调用函数时，所有的函数内声明的变量名称都被加到作用域中。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
total = 0                                 \\全局变量
def sum(arg1, arg2):                                    
    total = arg1 + arg2
    print "函数内是局部变量 :", total       \\ 返回两个参数的和，total在这里是局部变量
    return total;

sum(10, 20);                                 \\调用函数
print "函数外是全局变量 :", total

//输出
函数内是局部变量 : 30
函数外是全局变量 : 0
```
