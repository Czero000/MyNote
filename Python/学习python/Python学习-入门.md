## 运行Python ##

### 交互模式 ###
```python
$ python 
>>> print 'Hello World.'
Hello World.
```

### 脚本模式 ###
```python
$ cat hello.py
#!/usr/bin/env python
print 'hello world'

$ python hello.py 
Hello World.
```

### 编码风格 ###
http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

### 输出 ###
使用`print`加上字符串，就可以像屏幕输出指定字符串
```python
print 'Hello World.'python
```

### 输入 ###
python提供`raw_input`，提供用户输入
```python
>>> name = raw_input()
Charlie.Cui
>>> print name
Charlie.Cui
```


### 源程序编码 ###
在python源文件中可以使用非ASCII编码。通过在`#!`行的后面添加一个特殊的注释来定义源文件的编码
```python
# -*- coding: encoding -*-
// python 支持utf-8 编码
# -*- coding: utf-8 -*-
```

### 标识符 ###
变量是标识符的列子，标识符是用来标识某样东西的名字。在命名标识符的时候，要遵守如下规则

* Python的标识符区分大小写

* 标识符以字母或下划线开头，包括字母、下划线和数字、大小写敏感

* 以下划线开头(_foo)的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用from xx import *导入

* 以双下划线开头的(__foo)代表类的私有成员

* 以双下换线开头和结尾的(__foo__)代表python里特殊方法专用的标识符，如__init__()代表类的构造函数

* 标识符不能是保留字

下面是Python的保留字符，保留字符不能用作常数或变数，或其他标识符名称，所有的Python的标识符只含有小写字母。
```python
// python保留字符
and            elif        global   or    yield
assert         else        if       pass
break          except      import   print
class          exec        in       raise
continue       finally     is       return
def            for         lambda   try
del            from        not      while
```

### 缩进 ###
python函数没有明显的begin和end，没有标明函数的开始和结束的花括号，唯一的分隔符是一个冒号
```python
a = 100;
if a >= 100;
    print a
else;
    print -a
```
注释以`#`开头，每一行都是一个语句，并以`;`结尾，缩进的语句视为代码块，代码块与的使用4个空格机型缩进。

### 多行语句 ###
```python
// 使用\将每行的语句分为多行显示
total = item_one + \
        item_two + \
        item_three
// 语句中包含[]或{}或()不需要多行连字符
days  = ['Monday', 'Tuesday', 'Wendnesday',
        'Thursday', 'Friday']        
```
