#Python正则表达式

正则表达式是一个特殊的字符序列，他能够帮助方便的检查一个字符串是否与某种模式匹配。python在1.5版本之后增加了`re`模块，他提供了perl风格的正则表达式。

`re`模块使python语言拥有全部正则表达式模式。`compile`函数根据一个模式字符串和可以选的标志参数生成一个正则表达式对象。该对象拥有一系列方法用于正则表达式匹配和替换。`re`模块也提供了与这些方法功能完全一直的函数，这些函数使用一个模式字符串作为他们的第一个参数。

正则表达式使用反斜杠`\`来转义特殊字符，使其可以匹配字符本身，而不是指定其特殊的含义，可能会和python字面意义上的字符串转义相冲突。例如要匹配一个反斜杠本身，你要使用`\\\\`来作为正则表达式的字符串，以为正则表达式要是`\\`,而字符串里，每个反斜杠要写成`\\`，当然也可以在字符串前加上`r`这个前缀避免疑惑，因为`r`开头的python是`raw`字符串，里面的所有字符都不会被转义，例如`r'/n'`这个字符串就是一个反斜杠加上字幕n，而`\n`是换行符。因此上面的`\\\\`，可以写成`r'\\'`这样，看下面例子：

```python
>>> import re                                           \\导入re模块
>>> s = '\x5c'                                          \\定义要匹配的字符串
>>> print s                      
\
>>> re.match('\\\\',s)                                   \\ 匹配模式
<_sre.SRE_Match object at 0x7f160df5c988>
>>> re.match(r'\\',s)                                    \\匹配模式
<_sre.SRE_Match object at 0x7f160df5c9f0>
>>> re.match('\\',s)                                     \\ 不可以这样匹配
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.7/re.py", line 137, in match
    return _compile(pattern, flags).match(string)
  File "/usr/lib64/python2.7/re.py", line 242, in _compile
    raise error, v # invalid expression
sre_constants.error: bogus escape (end of line)
```



## 正则表达式语法

正则表达式(RE)指定一个与之匹配的字符合集；

正则表达式可以被连接，从而形成新的正则表达式；例如A和B都是正则表达式，那么AB也是正则表达式。一般地，如果字符串p与A匹配，q与B匹配的话，那么字符串pq也会与AB匹配，但A或者B里含有边界限定条件或者命名组操作的情况除外。也就是说，复杂的正则表达式可以用简单的连接而成。

正则表达式可以被连接，从而形成新的正则表达式；例如A和B都是正则表达式，那么AB也是正则表达式。一般地，如果字符串*p*与A匹配，q与B匹配的话，那么字符串pq也会与AB匹配，但A或者B里含有边界限定条件或者命名组操作的情况除外。也就是说，复杂的正则表达式可以用简单的连接而成。
正则表达式可以包含特殊字符和普通字符，大部分字符比如`'A'`，`'a'`和`'0'`都是普通字符，如果做为正则表达式，它们将匹配它们本身。由于正则表达式可以连接，所以连接多个普通字符而成的正则表达式`last`也将匹配`'last'`。（后面将用不带引号的表示正则表达式，带引号的表示字符串）

下面就来介绍正则表达式的特殊字符：

- `.` :  点，在普通模式，他匹配除换行符以外的任意一个字符；如果指定了`DOTALL`标记，匹配包括换行符以内的任意一个字符
- `^`:  匹配一个字符串的开始，在`MULTILINE`模式下，也匹配任意一个新行的开始。
- `$` : 匹配一个字符串的结尾或者字符串最后的换行符，在`MULTILINE`模式，也匹配任意一行的行尾，在普通模式下`foo.$`匹配搜索`foo1\nfoo2\n`只会找到`foo2`，但是在`MULTILINE`模式，还能找到`foo1`，而且就用一个`$`去搜索`foo\n`，会找到两个空的匹配：一个最后的换行符，一个字符串的结尾

```python
>>> re.findall('(foo.$)','foo1\nfoo2\n')
['foo2']
>>> re.findall('(foo.$)','foo1\nfoo2\n',re.MULTILINE)
['foo1', 'foo2']
>>> re.findall('($)','foo\n')                        
['', '']
```

- `*`: 指定将前面的RE重复0或者任意多次，而且总是试图尽量多次的匹配
- `+`:指定将前面的RE重复1次或者任意多次，而且总是尽量多次的匹配
- `?`: 指定将前面的RE重复0次或者1次，如果有的话，尽量匹配1次
- `*?,+? ??`:从前面介绍看到`*`,`+`,`?`都是贪婪的，但这也许并不是我们需要的，所以在后面加上个`?`，将策略改为非贪婪，只匹配尽量少的RE

```python
>>> re.findall('<(.*)>','<H1>title</H1>')
['H1>title</H1']
>>> re.findall('<(.*?)>','<H1>title</H1>')
['H1', '/H1']
```

- `{m}`: m是一个数字，指定将前面的RE重复N次
- `{m,n}`: m和n都是数字，指定将前面的RE重复m到n次，例如`a{3,5}`匹配3到5个连续的a，注意，如果省略m，将匹配0到n个前面的RE；如果省略n，将匹配n到无穷多个前面的RE；当然中间的逗号是不能省略的，不然就变成前面的形式了。
- `{m,n}?` :前面说的`{m,n}`，也是贪婪的，`a{3,5}`如果有5个以上连续a的话，会匹配5个，这个也可以通过加问号改变。`a{3,5}?`如果可能的话，将只匹配3个a。


- `\`: 反斜杠转义特殊字符，或者指定一个特殊的序列，强烈建议用raw字符串来表述正则。

- `[]`: 用于指定一个字符的集合。可以单独列出字符，也可以用`'-'`连接起止字符以表示一个范围。特殊字符在中括号里将失效，比如`[akm$]`就表示字符`'a'`，`'k'`，`'m'`，或`'$'`，在这里$也变身为普通字符了。`[a-z]`匹配任意一个小写字母，`[a-zA-Z0-9]`匹配任意一个字母或数字。如果你要匹配`']'`或`'-'`本身，你需要加反斜杆转义，或者是将其置于中括号的最前面，比如`[]]`可以匹配`']'`

  你还可以对一个字符集合*取反*，以匹配任意不在这个字符集合里的字符，`取反`操作用一个`'^'`放在集合的最前面表示，放在其他地方的`'^'`将不会起特殊作用。例如`[^5]`将匹配任意不是`'5'`的字符；`[^^]`将匹配任意不是`'^'`的字符。

  注意：在中括号里，`+`、`*`、`(`、`)`这类字符将会失去特殊含义，仅作为普通字符。反向引用也不能在中括号内使用。

- `|`: 管道符号，A和B是任意的RE，那么`A|B`就是匹配A或者B的新的RE。任意个数的RE都可以像这样用管道符号间隔连接起来。这种形式可以被用于组中。对于目标字符串，被`|`分割的RE将自左至右一一被测试，一旦测试成功，后面的将不再被测试，即使后面的RE可能匹配更长的串，换句话说，`|`操作符是非贪婪的，要匹配字面意义的`|`，可以用反斜杠转义或者包含在方括号内：`[|]`


- `(...)`:匹配圆括号里的RE匹配的内容，并指定组的开始和结束位置。组里面的内容可以被提取，也可以采用`\number`这样的特殊序列，被用于后续的匹配。雅培匹配字面意义的`(`和`)`，可以使用反斜杠转义`\(、\)`或者抱在方括号中`[(]、[)]`。

- `(?...)`:这是个表达式的扩展符号。`?`后的第一个字符决定了整个表达式的语法和含义，除了`(?P...)`以为，表达式不会产生一个新的组。

  - `(?iLmsux)`: `i`、`L`、`m`、`s`、`u`、`x`里的一个或多个。表达式不匹配任何字符。但是指定相应的标志。**re.I**(忽略大小写)、**re.L**(依赖locale)、**re.M**(多行模式)、**re.S**(.匹配所有字符)、**re.U**(依赖Unicode)、**re.X**(详细模式)。关于各个模式的区别，下面会有专门的一节来介绍的。使用这个语法可以代替在`re.compile()`的时候或者调用的时候指定*flag*参数。

  - | 修饰符  | 描述                                      |
    | ---- | --------------------------------------- |
    | re.I | 使匹配对大小写不敏感                              |
    | re.L | 做本地化识别（locale-aware）匹配                  |
    | re.M | 多行匹配，影响 ^ 和 $                           |
    | re.S | 使 . 匹配包括换行在内的所有字符                       |
    | re.U | 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B. |
    | re.X | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。         |

  - ```python
    >>> re.findall('(?m)(foo.$)','foo1\nfoo2\n')  \\与re.MULTILINE一样效果
    ['foo1', 'foo2']
    ```


- `(?:...)`: 匹配内部的RE所批评的内容，但不建立组
- `(?P<name>...)`: 和普通圆括号类似，但是字串匹配到内容将可以用命名*name*参数来提取。组的name必须是有效的python标识符，而且杂本表达式内不重名。命名了的组和普通组一样，也用数字来提取，也就是说名字是一个额外的属性

```python
>>> re.findall('(?m)(foo.$)','foo1\nfoo2\n')
['foo1', 'foo2']
>>> m=re.match('(?P<var>[a-zA-Z_]\w*)','abc=123')
>>> m.group('var')
'abc'
>>> m.group(1)
'abc'
```

- `\number`: 匹配number所指的组相同的字符串。组的序号从1开始。例如：`(.+) \1`可以匹配`'the the'`和`'55 55'`，但不匹配`'the end'`。这种序列在一个正则表达式里最多可以有99个，如果*number*以0开头，或是有3位以上的数字，就会被当做八进制表示的字符了。同时，这个也不能用于方括号内。


- `\A`: 只匹配字符串的开始。


- `\b`: 匹配单词边界（包括开始和结束），这里的“单词”，是指连续的字母、数字和下划线组成的字符串。注意，`\b`的定义是`\w`和`\W`的交界，所以精确的定义有赖于`UNICODE`和`LOCALE`这两个标志位。


- `\B`: 和`\b`相反，`\B`匹配非单词边界。也依赖于`UNICODE`和`LOCALE`这两个标志位。


- `\d`: 未指定`UNICODE`标志时，匹配数字，等效于：`[0-9]`。指定了`UNICODE`标志时，还会匹配其他Unicode库里描述为字符串的符号。便于理解，举个例子（好不容易找的例子啊，呵呵）：


- `\D`:和`\d`相反，不多说了。


- `\s`: 当未指定`UNICODE`和`LOCALE`这两个标志位时，匹配任何空白字符，等效于`[ \t\n\r\f\v]`。如果指定了`LOCALE`，则还要加LOCALE相关的空白字符；如果指定了`UNICODE`，还要加上UNICODE空白字符，如较常见的空宽度连接空格（\uFEFF）、零宽度非连接空格(\u200B)等。


- `\S`: 和`\s`相反，也不多说。


- `\w`: 当未指定`UNICODE`和`LOCALE`这两个标志位时，等效于`[a-zA-Z0-9_]`。当指定了`LOCALE`时，为`[0-9_]`加上当前LOCAL指定的字母。当指定了`UNICODE`时，为`[0-9_]`加上UNICODE库里的所有字母。
- `\W`: 和`\w`相反，不多说。


- `\Z`:只匹配字符串的结尾。

## 匹配和搜索

python提供了两种基于正则表达式的操作：匹配(match)从字符串的开始检查字符串是否符合正则匹配。而搜索(search)检查字符串任意位置是否有匹配的子串。

### re.math函数

`re.match`尝试从字符串的起始位置匹配一个模式，如果不是其实位置匹配成功的话，`match()`就返回一个none。
函数语法：
```python
re.match(pattern, string, flags=0)
```
函数参数说明：

| 参数      | 描述                                   |
| ------- | ------------------------------------ |
| pattern | 匹配的正则表达式                             |
| string  | 要匹配的字符串。                             |
| flags   | 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。 |

匹配成功`re.match()`返回一个匹配的对象，否则返回None。可以使用`group(num)`或者`groups()`匹配对象函数来获取匹配表达式。

| 匹配对象方法       | 描述                                       |
| ------------ | ---------------------------------------- |
| group(num=0) | 匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。 |
| groups()     | 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。           |

实例：

```python
#!/usr/bin/env python   
# encoding: utf-8       

import re               
// 方法1                        
str = 'Hello , my name is Charlie!'
p = re.compile('Hello')
match = p.match(str)    
print match.group()     

//方法2
p = re.compile('Hello')
m=p.match(str)          
print m.group()         

//方法3
print re.match('Hello',str).group()        \\首字母匹配
print re.search('Charlie',str).group()      \\查找
//其他
print re.match('Hello',str).span()
print re.match('Charlie',str)


//输出结果
Hello
Hello
Hello
Charlie
(0, 5)
None
```

实例二：

```python
#!/usr/bin/env python
# encoding: utf-8

import re

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

if matchObj:
       print "matchObj.group() : ", matchObj.group()
       print "matchObj.group(1) : ", matchObj.group(1)
       print "matchObj.group(2) : ", matchObj.group(2)
else:   
       print "No match!!"


// 输出
matchObj.group() :  Cats are smarter than dogs
matchObj.group(1) :  Cats
matchObj.group(2) :  smarter
```

### re.search

re.search扫描整个字符串并返回第一个成功的匹配

函数语法：

```
re.search(pattern, string, flags=0)
```

函数参数说明：

| 参数      | 描述                                   |
| ------- | ------------------------------------ |
| pattern | 匹配的正则表达式                             |
| string  | 要匹配的字符串。                             |
| flags   | 标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。 |

匹配成功re.search方法返回一个匹配的对象，否则返回None。

我们可以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式。

| 匹配对象方法       | 描述                                       |
| ------------ | ---------------------------------------- |
| group(num=0) | 匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。 |
| groups()     | 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。           |

实例：

```python
>>> print re.search('www','www.zerounix.com').span()
(0, 3)
>>> print re.search('com','www.zerounix.com').span()
(13, 16)
```

### re.match与re.sreach的区别

`re.match`只匹配字符串开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None。而`re.search`匹配整个字符串，直到找到匹配项。

实例

```python
#!/usr/bin/env python                                    
# encoding: utf-8  
import re          

line = "Cats are smarter than dogs"                      
matchObj = re.match(r'dogs', line, re.M|re.I)            
if matchObj:       
    print "Match --> match.Obj.group(): ",matchObj.group()
else:              
    print 'No match'                                     

matchObj = re.search(r'dogs',line , re.M|re.I)           
if matchObj:       
    print  "Match --> match.Obj.group(): ",matchObj.group()
else:              
    print 'No match'

//输出
No match
Match --> match.Obj.group():  dogs
```

## 模块的属性和方法

- re.compile(pattern[, flags])

把正则表达式pattern编译成正则对象，以便可以用正则对象的match和search方法。得到的正则对象的行为可以用flags来指定，值可以有下面的值or得到

```python
prog = re.compile(pattern)
result = prog.match(string)
等同于
result = re.match(pattern,string)
```

区别是，用了**re.compile**以后，正则对象会得到保留，这样在需要多次运用这个正则对象的时候，效率会有较大的提升。使用相同的正则匹配相同的字符串，执行100W次，就会体现出compile的效率了
```python
>>> import timeit
>>> timeit.timeit(
...     setup='''import re; reg = re.compile('<(?P<tagname>\w*)>.*</(?P=tagname)>')''',
...     stmt='''reg.match('<h1>xxx</h1>')''',
...     number=1000000)
0.8764979839324951
>>> timeit.timeit(
...     setup='''import re''',
...     stmt='''re.match('<(?P<tagname>\w*)>.*</(?P=tagname)>', '<h1>xxx</h1>')''',
...     number=1000000)
3.3436989784240723
```

- re.search(pattern,string[, flags])

扫描string，看是否有位置可以匹配正则表达式pattern，如果找到，就返回一个MatchObject的实例，否则返回None。注意这个和找到长度为0的字串航意不一样，搜索过程受flags影响。

- re.match(pattern,strintg[, flags])

如果字符串string的开头和正则表达式pattern匹配的话，返回一个相应的MatchObject的实例，否则返回None。

- re.split(pattern,string[ ,maxsplit=0])

用匹配pattern的子串分隔字符串，如果pattern里使用了括号，那么pattern匹配到的串也作为返回值列表的一部分，如果maxsplit不为0，则最多被分割为maxsplit个子串，剩余部分将整个返回。

```python
>>> re.split('\W+','Words,words,words.')
['Words', 'words', 'words', '']
>>> re.split('(\W+)','Words,words,words.')
['Words', ',', 'words', ',', 'words', '.', '']
>>> re.split('(\W+)','Words,words,words.',1)
['Words', ',', 'words,words.']
```

如果正则有圆括号，并且可以匹配到字符串的开始位置的时候，返回值的第一项，会多出一个空字符串，匹配到字符结尾也是同样的道理：

```python
>>> re.split('(\W+)','...words, words...')  
['', '...', 'words', ', ', 'words', '...', '']
```

split不会被零长度的正则所分割：

```python
>>> re.split('x*','foo')
['foo']
>>> re.split("(?m)^$","foo\n\nbar\n")
['foo\n\nbar\n']
```

- re.findall(pattern, string[, flags])

以列表的形式返回string里匹配pattern的不重叠的子串。string会被从左到右一次扫描，返回的列表也是从左到右一次匹配到的。如果pattern里含有组的话，那么会返回匹配到的组的列表；如果pattern里有多个组，那么各组会先组成一个元组，然后返回值将是一个元组的列表。

```
// 简单的findall
>>> re.findall('\w+','hello,world!')
['hello', 'world']
>>> re.findall('(\d+)\.(\d+)\.(\d+)\.(\d+)', 'My IP is 192.168.1.19,and you is 192.168.1.29')
[('192', '168', '1', '19'), ('192', '168', '1', '29')]
```

- re.finditer(pattern, string [, flags])

与findall()类似，但是返回的是MatchObject的实例迭代器。

```python
>>> for m in re.finditer('\w+','Hello World'):
...     print m.group()
...
Hello
World
```

- re.sub(pattern,repl,string[, count])

替换，将string里匹配pattern的部分，用repl替换掉，最多替换count次，然后返回替换后的字符串。如果string里没有匹配pattern的串，将被原封不动的返回。repl可以是一个字符串，也可以是一个函数。如果repl是个字符串，则其中的反斜杠会被处理，比如`\n`会吧转换成换行符，反斜杠加数字会被替换成相应的组，比如`\6`表示pattern匹配到的第六个组的内容。

```python
>>> re.sub(r'def\s+([a-zA-Z][a-zA-Z_0-9]*)\s*\(\s*\):',r'static PyObject*\npy_\1(void)\n{',
...     'def muyfunc():')
'static PyObject*\npy_muyfunc(void)\n{'
>>> re.sub('abc','bcd','123abc')
'123bcd'
```

零长度的匹配也会被替换：

```
>>> re.sub('x*','-','abcxxd')
'-a-b-c-d-'
```

- re.subn(pattern,repl,string[, count])

跟sub()函数一样，他返回的是一个元组（新字符串，匹配到的次数）

```python
>>> re.subn('-(\d+)-','-\g<1>0\g<0>', 'a-11-b-22-c')
('a-110-11-b-220-22-c', 2)
```

- re.escape(string)

把string中，处理字母数字以为的字符，都加上反斜杠。

```python
>>> print re.escape('abc123_@#$')
abc123\_\@\#\$
```

*exception* `re`.**error**
如果字符串不能被成功编译成正则表达式或者正则表达式在匹配过程中出错了，都会抛出此异常。但是如果正则表达式没有匹配到任何文本，是不会抛出这个异常的

## 正则对象

正则对象有re.compile()返回，它有如下属性和方法

- match(string[, pos[, endpos]])

作用和模块的match()函数类似。区别就是后面两个参数。

pos是开始的搜索的位置，默认为0，endpos是搜索的结束的位置，如果endpos比pos还笑的话，结果为空。

```
>>> pattern=re.compile('o')
>>> pattern.match('dog')
>>> pattern.match('dog',1)
<_sre.SRE_Match object at 0x2729e68>
```

- search(string[, pos[, endpos]])

作用和模块search()函数类似，pos和endpos参数和上面match()函数类似

- split(string[, maxsplit=0])
- findall(string[, pos[, endpos]])
- finditer(string[, pos[, endpos]])
- sub(repl,string[, count=0])
- subn(repl, string[, count=0])

这几个函数都和模块相对应的函数一样



- flags
  编译本RE时，指定的标志位，如果未指定任何标志位，则为0。
  ```
  >>> pattern = re.compile("o", re.S|re.U)
  >>> pattern.flags
  >>> 48
  >>> groups
  >>> RE所含有的组的个数。
  ```
- groupindex
  一个字典，定义了命名组的名字和序号之间的关系。
  例子：
  这个正则有3个组，如果匹配到，第一个叫区号，最后一个叫分机号，中间的那个未命名
  ```
  >>> pattern = re.compile("(?P<quhao>\d+)-(\d+)-(?P<fenjihao>\d+)")
  >>> pattern.groups
  >>> 3
  >>> pattern.groupindex
  >>> {'fenjihao': 3, 'quhao': 1}
  >>> pattern
  ```
  建立本RE的原始字符串，相当于源代码了，呵呵。
  还是上面这个正则，可以看到，会原样返回：

```
>>> print pattern.pattern
>>> (?P<quhao>\d+)-(\d+)-(?P<fenjihao>\d+)
>>> Match对象
```
- re.MatchObject被用于布尔判断的时候，始终返回True，所以你用 if 语句来判断某个 match() 是否成功是安全的。
  它有以下方法和属性：
  ```
  expand(template)
  用template做为模板，将MatchObject展开，就像sub()里的行为一样，看例子：
  m = re.match('a=(\d+)', 'a=100')
  m.expand('above a is \g<1>')'above a is 100'
  m.expand(r'above a is \1')'above a is 100'group([group1, ...])
  ```

返回一个或多个子组。如果参数为一个，就返回一个子串；如果参数有多个，就返回多个子串注册的元组。如果不传任何参数，效果和传入一个0一样，将返回整个匹配。如果某个groupN未匹配到，相应位置会返回None。如果某个groupN是负数或者大于group的总数，则会抛出IndexError异常。

```
>>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
>>> m.group(0)       # 整个匹配
>>> 'Isaac Newton'
>>> m.group(1)       # 第一个子串
>>> 'Isaac'
>>> m.group(2)       # 第二个子串
>>> 'Newton'
>>> m.group(1, 2)    # 多个子串组成的元组
>>> ('Isaac', 'Newton')
```

如果有其中有用(?P...)这种语法命名过的子串的话，相应的groupN也可以是名字字符串。例如：
```
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.group('first_name')
>>> 'Malcolm'
>>> m.group('last_name')
>>> 'Reynolds'
```
如果某个组被匹配到多次，那么只有最后一次的数据，可以被提取到：
```
>>> m = re.match(r"(..)+", "a1b2c3")  # 匹配到3次
>>> m.group(1)                        # 返回的是最后一次
>>> 'c3'
>>> groups([default])
```
返回一个由所有匹配到的子串组成的元组。default参数，用于给那些没有匹配到的组做默认值，它的默认值是None
例如

```
>>> m = re.match(r"(\d+)\.(\d+)", "24.1632")
>>> m.groups()
>>> ('24', '1632')
```
default的作用

```
>>> m = re.match(r"(\d+)\.?(\d+)?", "24")
>>> m.groups()      # 第二个默认是None
>>> ('24', None)
>>> m.groups('0')   # 现在默认是0了
>>> ('24', '0')
>>> groupdict([default])
```

返回一个包含所有命名组的名字和子串的字典，default参数，用于给那些没有匹配到的组做默认值，它的默认值是None，例如

```
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.groupdict()
>>> {'first_name': 'Malcolm', 'last_name': 'Reynolds'}
>>> start([group])
>>> end([group])
```
返回的是：被组group匹配到的子串在原字符串中的位置。如果不指定group或group指定为0，则代表整个匹配。如果group未匹配到，则返回 -1。
对于指定的m和g，m.group(g)和m.string[m.start(g):m.end(g)]等效。
注意：如果group匹配到空字符串，m.start(group)和m.end(group)将相等。
例如
```
m = re.search('b(c?)', 'cba')
m.start(0)
1
m.end(0)
2
m.start(1)
2
m.end(1)
```

下面是一个把email地址里的“remove_this”去掉的例子：
```
email = "tony@tiremove_thisger.net"
m = re.search("remove_this", email)
email[:m.start()] + email[m.end():]
'tony@tiger.net'
span([group])
```
返回一个元组： (m.start(group), m.end(group))
- pos就是传给RE对象的search()或match()方法的参数pos，代表RE开始搜索字符串的位置。


- endpos
  就是传给RE对象的search()或match()方法的参数endpos，代表RE搜索字符串的结束位置。

- lastindex
  最后一次匹配到的组的数字序号，如果没有匹配到，将得到None。
  例如：(a)b、((a)(b))和((ab))正则去匹配'ab'的话，得到的lastindex为1。而用(a)(b)去匹配'ab'的话，得到的

- lastindex为2。

- lastgroup
  最后一次匹配到的组的名字，如果没有匹配到或者最后的组没有名字，将得到None。

- re
  得到本Match对象的正则表达式对象，也就是执行search()或match()的对象。

- string
  传给search()或match()的字符串。

## 正则表达式模式

模式字符串使用特殊的语法来表示一个正则表达式：

字母和数字表示他们自身。一个正则表达式模式中的字母和数字匹配同样的字符串。

多数字母和数字前加一个反斜杠时会拥有不同的含义。

标点符号只有被转义时才匹配自身，否则它们表示特殊的含义。

反斜杠本身需要使用反斜杠转义。

由于正则表达式通常都包含反斜杠，所以你最好使用原始字符串来表示它们。模式元素(如 r'/t'，等价于'//t')匹配相应的特殊字符。

下表列出了正则表达式模式语法中的特殊元素。如果你使用模式的同时提供了可选的标志参数，某些模式元素的含义会改变。

| 模式          | 描述                                       |
| ----------- | ---------------------------------------- |
| ^           | 匹配字符串的开头                                 |
| $           | 匹配字符串的末尾。                                |
| .           | 匹配任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。 |
| [...]       | 用来表示一组字符,单独列出：[amk] 匹配 'a'，'m'或'k'       |
| [^...]      | 不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。          |
| re*         | 匹配0个或多个的表达式。                             |
| re+         | 匹配1个或多个的表达式。                             |
| re?         | 匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式              |
| re{ n}      |                                          |
| re{ n,}     | 精确匹配n个前面表达式。                             |
| re{ n, m}   | 匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式            |
| a\| b       | 匹配a或b                                    |
| (re)        | G匹配括号内的表达式，也表示一个组                        |
| (?imx)      | 正则表达式包含三种可选标志：i, m, 或 x 。只影响括号中的区域。      |
| (?-imx)     | 正则表达式关闭 i, m, 或 x 可选标志。只影响括号中的区域。        |
| (?: re)     | 类似 (...), 但是不表示一个组                       |
| (?imx: re)  | 在括号中使用i, m, 或 x 可选标志                     |
| (?-imx: re) | 在括号中不使用i, m, 或 x 可选标志                    |
| (?#...)     | 注释.                                      |
| (?= re)     | 前向肯定界定符。如果所含正则表达式，以 ... 表示，在当前位置成功匹配时成功，否则失败。但一旦所含表达式已经尝试，匹配引擎根本没有提高；模式的剩余部分还要尝试界定符的右边。 |
| (?! re)     | 前向否定界定符。与肯定界定符相反；当所含表达式不能在字符串当前位置匹配时成功   |
| (?> re)     | 匹配的独立模式，省去回溯。                            |
| \w          | 匹配字母数字                                   |
| \W          | 匹配非字母数字                                  |
| \s          | 匹配任意空白字符，等价于 [\t\n\r\f].                 |
| \S          | 匹配任意非空字符                                 |
| \d          | 匹配任意数字，等价于 [0-9].                        |
| \D          | 匹配任意非数字                                  |
| \A          | 匹配字符串开始                                  |
| \Z          | 匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。c          |
| \z          | 匹配字符串结束                                  |
| \G          | 匹配最后匹配完成的位置。                             |
| \b          | 匹配一个单词边界，也就是指单词和空格间的位置。例如， 'er\b' 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。 |
| \B          | 匹配非单词边界。'er\B' 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。 |
| \n, \t, 等.  | 匹配一个换行符。匹配一个制表符。等                        |
| \1...\9     | 匹配第n个分组的子表达式。                            |
| \10         | 匹配第n个分组的子表达式，如果它经匹配。否则指的是八进制字符码的表达式。     |

------

## 正则表达式实例

#### 字符匹配

| 实例     | 描述           |
| ------ | ------------ |
| python | 匹配 "python". |

#### 字符类

| 实例          | 描述                      |
| ----------- | ----------------------- |
| [Pp]ython   | 匹配 "Python" 或 "python"  |
| rub[ye]     | 匹配 "ruby" 或 "rube"      |
| [aeiou]     | 匹配中括号内的任意一个字母           |
| [0-9]       | 匹配任何数字。类似于 [0123456789] |
| [a-z]       | 匹配任何小写字母                |
| [A-Z]       | 匹配任何大写字母                |
| [a-zA-Z0-9] | 匹配任何字母及数字               |
| [^aeiou]    | 除了aeiou字母以外的所有字符        |
| [^0-9]      | 匹配除了数字外的字符              |

#### 特殊字符类

| 实例   | 描述                                       |
| ---- | ---------------------------------------- |
| .    | 匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用象 '[.\n]' 的模式。 |
| \d   | 匹配一个数字字符。等价于 [0-9]。                      |
| \D   | 匹配一个非数字字符。等价于 [^0-9]。                    |
| \s   | 匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。 |
| \S   | 匹配任何非空白字符。等价于 [^ \f\n\r\t\v]。            |
| \w   | 匹配包括下划线的任何单词字符。等价于'[A-Za-z0-9_]'。        |
| \W   | 匹配任何非单词字符。等价于 '[^A-Za-z0-9_]'。           |
