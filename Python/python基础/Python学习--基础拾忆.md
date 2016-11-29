# Python 基础学习拾忆

## python编程风格

- 交互模式

```
$python
>>> print 'Hello World'
Hello World
```
- 脚本模式

```
cat hello.py
#!/usr/bin/env python
print 'Hello World'
```

- 编程风格

http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

- 多行打印
使用`\n`输入多行时，可以通过 `'''     '''`单个引号方式进行多行输出
```
>>> print '''
... line one
... line two
... line three
... '''

line one
line two
line three
```

## 内置变量
内置变量类型可以分为“数据”和程序两大类

数据类型：
- 空值：None
- 数字：bool、int、long、float、complex
- 序列：str、unicode、list、tuple
- 字典：dict
- 集合：set、frozentset





## IO文件处理
```
//以写入模式创建文件
f = open('test.txt','w')
//以追加写入模式创建文件
f = open('test.txt','a')
//写入数据
f.write('This is a test\n')
f.write('The winnter is comping/t')
f.write('Today is happy day')
//写入硬盘
f.flush()
//关闭文件，写入磁盘
f.close()
//以读模式打开文件
f = open('test.txt','r')
//读取文件内容
f.read()
//读取一行
f.readline()
//以列表方式，读取多行
f.readlines()
//移动指针
f.seek(num)
//查看指针位置
f.tell()
//


```
