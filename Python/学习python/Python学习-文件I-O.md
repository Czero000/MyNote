## Python 文件I/O

---

### 打印到屏幕

最简单的输出方式是用`print`语句，可以给他传递零或者多个用逗号隔开的表达式，此函数把你传递的表达式转换成一个字符串表达式，并将结果写到标准输出中

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
print "Python 是一个非常棒的语言，不是吗？";

// 输出
Python 是一个非常棒的语言，不是吗？
```

---

### 读取键盘输出

Python提供了两个内置函数从标准输入读取一行文本，默认的标准输入是键盘：

- raw_input
- input

#### raw_input函数

`raw_input([prompt])`函数从标准输入读取一个行，并返回一个字符串（去掉结尾的换行符）

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

str = raw_input("请输入：");

print "你的输入是: ", str
// 输出
请输入：Hello Python !!!
你的输入是:  Hello Python !!!
```



#### input函数

`input([prompt])`函数和`raw_input`函数类似，但是input可以接收一个python表达式作为输入，并将运算结果返回。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

str = input("请输入：");

print "你的输入是: ", str

//输出
请输入：[x*5 for x in range(2,10,2)]
你的输入是:  [10, 20, 30, 40]
```

---

### 打开和关闭文件

现在，可以向标准输入和输进行进行读写，python提供了必要的函数和方法进行默认情况下的文件基本操作。可以使用`file`对象做大部分文件操作。

#### open函数

必须现用python内置的open()函数打开一个文件，创建一个file对象，相关的方法才可以调用它进行读写。

```python
file object = open(file_name [, access_mode][, buffering])
```

各个参数细节如下：

- file_name：file_name变量是一个包含了你要访问的文件名称的字符串
- access_mode：access_mode决定了打开文件的模式：只读、写入、追加等。默认为只读
- buffering：如果buffering的值被设定为0，就不会有寄存。如果buffering的值取1，访问文件就会被寄存。如果将buffering值设为大于1的整数，表明了额这就是寄存区的缓冲大写，如果去负值，寄存区的大写则为系统默认。

不同模式打开文件的完全列表：

| 模式   | 描述                                       |
| ---- | ---------------------------------------- |
| r    | 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。         |
| rb   | 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。   |
| r+   | 打开一个文件用于读写。文件指针将会放在文件的开头。                |
| rb+  | 以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。          |
| w    | 打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| wb   | 以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| w+   | 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| wb+  | 以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| a    | 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| ab   | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| a+   | 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。 |
| ab+  | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。 |

---

### File对象的属性

一个文件被打开后，你有一个file对象，你可以得到有关该文件的各种信息。

| 属性             | 描述                                      |
| -------------- | --------------------------------------- |
| file.closed    | 返回true如果文件已被关闭，否则返回false。               |
| file.mode      | 返回被打开文件的访问模式。                           |
| file.name      | 返回文件的名称。                                |
| file.softspace | 如果用print输出后，必须跟一个空格符，则返回false。否则返回true。 |

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fo = open("foo.txt", "wb")

print "文件名: ", fo.name
print "是否关闭: ", fo.closed
print "访问模式: ", fo.mode
print "末尾是否强制加空格: ", fo.softspace

//输出
文件名:  foo.txt
是否关闭:  False
访问模式:  wb
末尾是否强制加空格:  0
```

#### close()方法

file对象的close()方法刷新缓冲区里任何没有写入的信息，并关闭该文件，之后便不能再进行写入。但一个文件对象的引用被重新定义给另外一个文件时，Python会关闭之前的文件，用`close()`方法关闭文件是一个很好的习惯

```python
fileObject.close()
```

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fo = open("foo.txt","wd")

print "文件名: ",fo.name
fo.close()

// 输出
文件名:  foo.txt
```

---

#### write()方法

`write()`方法可以将任何字符串写入一个打开的文件，需要注意的是，python字符串可以是二进制数据，而不仅仅是文字。`write()`方法不在字符串的结尾添加换行符`\n`。

```python
fileObject.write(string)
```

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fo = file("foo.txt","wb")
fo.write("My Blog is \n www.zerounix.com!");

fo.close()

//输出
$ more foo.txt
My Blog is
 www.zerounix.com!
```

---

#### read()方法

read()方法从一个打开的文件中读取一个字符串，同样python字符串可以是二进制数据

```python
fileObject.read([count]);
```

在这里，被传递的参数是要从一打开的文件中读取的字节技术，该方法从文件的开头读入，如果没有传入count，他会尝试尽可能多的多读取内容，知道文件末尾。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fo = open("foo.txt","r+")
str = fo.read(10);

print "读取的字符串是 :", str

fo.close()

// 输出
读取的字符串是 : My Blog is
```

---

### 文件定位

`tell()`方法告诉你文件内的当前位置，以便下一次读写会发生在文件开头这么多字节之后。`seek( offset[,from])`方法改变当前文件的位置。offset变量表示要移动的字节数。from变量指定开始移动自己的参考位置。如果from被设定为0，这意味将文件开头作为移动字节的参考位置；如果设定为1，则使用当前位置作为参考位置；如果他被设定2，那么该文件的末尾将作为参考位置。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

fo = open("foo.txt","r+")
str = fo.read(10);
print "读取的字符串是: ", str

posltion = fo.tell();
print "当前文件位置: ", posltion

posltion = fo.seek(0, 0);
str = fo.read(10);
print "读取的字符串是: ", str

fo.close();

//输出
读取的字符串是:  My Blog is
当前文件位置:  10
读取的字符串是:  My Blog is
```

---

### 重命名和删除文件

Python的`os`模块提供了帮你执行文件处理操作的方法，比如重命名和删除文件。要使用这个模块，要先导入这个模块。才可以调动相关功能。

#### rename()方法

语法：`os.rename(current_file_name, new_file_name)`

创建一个名为`test1.txt`的测试文件

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

os.rename("test1.txt", "test2.txt" )
```

#### remove()方法

语法：`os.remove(file_name)`

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

os.remove(text2.txt)
```

---

### Python里的目录

所有文件都包含在各个不同的目录下，不过Python也能够轻松处理，os模块有许多方法帮你创建，删除和更改目录。

#### mkdir()

可以使用os模块的`mkdir()`方法在当前目录下创建新的目录，`mkdir()`需要提供一个包含创建目录名的参数

```python
# -*- coding: UTF-8 -*-

import os

os.mkdir("test")
```



#### chdir()

可以用`chdir()`方法改变当目录。`chdir()`需要一个参数是你想要设定当前目录的目录名称

```python
# -*- coding: UTF-8 -*-

import os

os.chdir("/opt/python/test")
```



#### getcwd()

`getcwd()`显示当前的工作目录

```python
# -*- coding: UTF-8 -*-

import os

os.getcwd()
```



#### rmdir()

`rmdir()`方法删除目录，目录名称以参数传递，在删除目录之前，它的所有内容应该被清除

```python
# -*- coding: UTF-8 -*-

import os
os.rmdir( "/opt/python/test" )
```

---

### 文件、目录相关方法

三种重要的方法来源能对windows和unix操作系统的文件及目录进行一个广泛且使用的处理及操作。

- File 对象方法: file对象提供了操作文件的一系列方法。
- OS 对象方法: 提供了处理文件及目录的一系列方法。
