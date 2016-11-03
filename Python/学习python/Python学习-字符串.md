###  Python字符串 ###
字符串是Python中最为常见的数据类型，通过引号来创建字符串。
```python
var1 = 'Hello World!'
var2 = 'Python Programming'
```

### Python访问字符串的值 ###

Python不支持单字符串类型，单字符串在Python也是作为一个字符串使用。Python访问子字符串，可以使用方括号来截取字符串

```Python
// 脚本
#!/usr/bin/env python
# -*- coding: utf8 -*-
var1 = 'Hello World'
var2 = 'Python Programming'


print "var1[0]: ", var1[0]
print "var2[1:5]: ", var2[1:5]

// 输出
var1[0]:  H
var2[1:5]:  ytho
```

###  Python 字符串更新 ###

你可以对已存在的字符串进行修改，并赋值给另外一个变量

```python
//脚本
#!/usr/bin/env python
# -*- coding: utf8 -*-
var1 = 'Hello World'
var2 = 'Python Programming'

print "Updated String :-", var1[:6] +' Python'*2

//输出
Updated String :- Hello  Python Python
```

### Python转义字符###

需要在字符中使用特殊字符时，python用反斜杠`\`转义字符

| 转义字符   | 描述                       |
| ------ | ------------------------ |
| \（在行尾） | 续航符                      |
| \\\    | 反斜杠                      |
| \'     | 单引号                      |
| \"     | 双引号                      |
| \a     | 响铃                       |
| \b     | 退格                       |
| \e     | 转义                       |
| \000   | 空                        |
| \\n    | 换行                       |
| \v     | 纵向制表符                    |
| \t     | 横向制表符                    |
| \r     | 回车                       |
| \f     | 换页                       |
| \oyy   | 八进制数，yy代表字符，例如：\o12代表换行  |
| \xyy   | 十六进制数，yy代表字符，例如：\x0a代表换行 |
| \other | 其他的字符以普通格式输出             | |



### Python字符串运算符 ###

变量a的值为字符串`hello`,变量b的值为字符串`Python`

| 操作符    | 描述                                       | 实例                                       |
| ------ | ---------------------------------------- | ---------------------------------------- |
| +      | 字符串连接                                    | a + b 输出结果： HelloPython                  |
| *      | 重复输出字符串                                  | a*2 输出结果：HelloHello                      |
| []     | 通过索引获取字符串中的字符                            | a[1] 输出结果 **e**                          |
| [ :]   | 截取字符串中的一部分                               | a[1:4] 输出结果**ell**                       |
| in     | 成员运算符 - 如果字符串中包含给定的字符返回 True             | **H in a** 输出结果 1                        |
| not in | 成员运算符 - 如果字符串中不包含给定的字符返回 True            | **M not in a** 输出结果 1                    |
| r/R    | 原始字符串 - 原始字符串：所有的字符串都是直接按照字面的意思来使用，没有转义特殊或不能打印的字符。 原始字符串除在字符串的第一个引号前加上字母"r"（可以大小写）以外，与普通字符串有着几乎完全相同的语法 | **print r'\n'** prints \n 和 **print R'\n'**prints \n |
| %      | 格式字符串                                    |             后面会讲                         |



### Python字符串格式化 ###

Python支持格式化字符串输出，尽管肯能用到非常复杂的表达式，但最基本的用法是将一个值插入到一个有字符串格式符%s的字符串中，在Python中，字符串格式化使用与C中sprintf函数一样的语法。

```Python
// 脚本
#!/usr/bin/env python
# -*- coding: utf8 -*-
print "My name is %s and weight is %d kg" % (1.0, 21.90)

// 输出
My name is 1.0 and weight is 21 kg
```

python字符串格式化符号、

| 符号   | 描述                 |
| ---- | ------------------ |
| %c   | 格式化字符及ASCII码       |
| %s   | 格式化字符串             |
| %d   | 格式化整数              |
| %u   | 格式化无符号整数           |
| %o   | 格式化无符号八进制数         |
| %x   | 格式化无符号十六进制数        |
| %X   | 格式化无符号十六进制数 大写     |
| %f   | 格式化浮点数字，可以指定小数点后精度 |
| %e   | 用科学计数法格式化浮点数       |
| %E   | 作用同%e，             |
| %g   | %f和%e的简写           |
| %G   | %f 和 %E 的简写        |
| %p   | 用十六进制数格式化变量的地址     |



格式化操作符辅助指令

| 符号    | 功能                                      |
| ----- | --------------------------------------- |
| *     | 定义宽度或者小数点精度                             |
| -     | 用作左对齐                                   |
| +     | 在正数前面显示`+`                              |
| <sp>  | 在正数前面显示空格                               |
| #     | 在八进制数前面显示`0`，在十六进制数前面显示`0X`（取决于用的是x还是X） |
| 0     | 显示的数字前面填充`0`而不是默认的空格                    |
| %     | `%%`输出一个单一的`%`                          |
| (var) | 映射变量(字典)                                |
| m.n.  | m是显示的最小总宽度，n是小数点后的位数                    |



### Python三引号###

Python中三引号可以将复杂的字符串进行赋值，三引号允许一个字符串跨多行，字符串可以包含换行符、制表符以及其他特殊字符。

```python
>>> hi = '''hi
... there'''
>>> print hi
hi
there
```

三引号让程序员从引号和特殊字符串的泥潭里面解脱出来，自始至终保持一小块字符串的格式是所谓的WYSIWYG（所见即所得）格式的。

一个典型的用例是，当你需要一块HTML或者SQL时，这时用字符串组合，特殊字符串转义将会非常的繁琐。

```Python
errHTML = '''
<HTML><HEAD><TITLE>
Friends CGI Demo</TITLE></HEAD>
<BODY><H3>ERROR</H3>
<B>%s</B><P>
<FORM><INPUT TYPE=button VALUE=Back
ONCLICK="window.history.back()"></FORM>
</BODY></HTML>
'''
cursor.execute('''
CREATE TABLE users (  
login VARCHAR(8),
uid INTEGER,
prid INTEGER)
''')
```



### Unicode字符串###

Python中定义一个Unicode字符串和定义一个普通字符串一样简单

```python
>>> u'Hello World !'
u'Hello World !'
```

引号前小写的`u`表示这里创建的是一个Unicode字符串。如果想加入一个特殊字符，使用Python的Unicode-Escape编码

```python
>>> u'Hello\u0020World!'
u'Hello World!'
```

被替换的`\u0020`标识表示在给定位置插入编码值为0x0020的Unicode字符（空格）
