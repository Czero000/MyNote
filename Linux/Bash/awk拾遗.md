title: awk拾遗
date: 2016/12/09 10:41:32
updated: 2016/12/09 10:41:32
categories:
- Linux系统
- Basic
- Bash
---
#awk的工作原理
一次读取一行文本，按输入分隔符进行切片，切成多个组成部分，将每片直接保存在内建的变量中，$1,$2,$3….，引用指定的变量，可以显示指定断，或者多个断。如果需要显示全部的，需要使用$0来引用。可以对单个片断进行判断，也可以对所有断进行循环判断。其默认分隔符为空格

#awk的基本用法格式
```
awk [options] ‘program’ FILE
```
语句之间用分号分隔
```
[options]
-F  : 指明输入时用到的字段分隔符
-v var=VALUE  : 自定义变量
```
在awk中变量的引用不需要加 $ ，而是直接引用

# awk用法的简要介绍
第一种模式
```
awk [options] ‘scripts’ file1,file2…..
```
在这种模式中，scripts主要是命令的堆砌，对输入的文本行进行处理，通过命令print,printf或是输出重定向的方式显示出来，这里经常用到的知识点是：awk的内置变量，以及命令print和printf的使用

第二种模式
```
awk [options] ‘PATTERN{action}’ file,file2…..
```
在这种模式中，最重要的是5种模式和5种action的使用，以及awk的数组的使用和内置函数

### print
1. 各项目之间使用逗号隔开，而输出时则以空白字符分隔
2. 输出的Item可以为字符串或数值，当前记录的字段（如$1）、变量或awk的表达式，数值会先转换为字符串，而后再输出
3. print命令后面的Item可以省略，此时其功能相当于print $0,因此，如果想输出空白行，则需要使用print””
4. 如果引用变量$1或其他的，是不能使用引号引起来


### 内置变量
- FS  : input field seperator,输入的分隔符，默认为空白字符
- OFS : output field seperator,输出的分隔符，默认为空白字符
- RS  : input record seperator,输入的换行符
- ORS : output record seperator,输出时的换行符
- NF  : number of field ,字段个数
  - awk ‘{print NF}’ /etc/fstab :打印每行的最后一个字段为第几个字段，这里是数量引用，不是对应的值引用
  - awk ‘{print $NF}’ /etc/fstab : 打印每行中的最后一个字段
- NR : number of record,文件中的行数
  - awk ‘{print NR}’ /etc/fstab: 打印行号，其会个行号都显示
  - awk ‘END{print NR}’ /etc/fstab: 显示文本的总行数，其只是在文本处理完成后，只显示一次行号
  - awk ‘{print NR}’ file1 file2 : 会每把所有文档进行总的编号，而不是单独对文件进行编号

- FNR : 对每个文件进行行数单独编号
  - awk ‘{print FNR}’ file1 file2 : 会对每个文件的行数进行单独的编号显示

- FILENAME  : awk命令所处理的文件的名称
  - awk ‘{print FILENAME}’ file1 : 显示当前文件名，但会每行显示一次
  - awk ‘END{print FILENAME}’ file1 : 显示当前文件名，但只会显示一次
- ARGC  : 命令行中参数的个数，其awk命令也算一个参数
  - awk ‘END{print ARGC}’ /etc/fstab : 显示共有几个参数
- ARGV  : 其是一个数组，保存的是命令行所给定的各参数
  - awk ‘END{print ARGV[0]}’ /etc/fstab : 显示第一个参数，默认第一个参数个awk命令本身

### 自定义变量
-v var=VALUE  : 在选项位置定义
awk 'BEGIN{test="hello";print test}' : 在program中定义
  变量在program中定义时，需要使用引号引起来

### printf命令
其格式化输出：`printf FORMAT,item1,item2….`
要点：
1.其与print命令最大不同是，printf需要指定format
2.printf后面的字串定义内容需要使用双引号引起来
3.字串定义后的内容需要使用”,”分隔，后面直接跟Item1,item2….
4.format用于指定后面的每个item的输出格式
5.printf语句不会自动打印换行符，\n

格式符
```
%c : 显示字符的ASCII码
%d , %i  : 显示十进制整数
%e , %E : 科学计数法数值显示
%f  : 显示为浮点数
%g , %G : 以科学数法或浮点形式显示数值
%s : 显示字符串
%u : 无符号整数
%% : 显示%号自身，相当于转义
修饰符
N  : 显示宽度
-  : 左对齐（默认为右对齐）
+ : 显示数值符号
```
示例：
```
awk -F: ‘{printf “%s\n”,$1}’ /etc/fstab
awk -F: ‘{printf “username: %s,UID:%d\n”,3}’ /etc/passwd
awk -F: ‘{printf “username: %-20s shell: %s\n”,NF}’ /etc/passwd
```

### 输出重定向
```
print items > “output-file”
print items >> “output-file”

print items | command
```
```
  特殊文件描述符：
  /dev/stdin :标准输入
  /dev/stdout:标准输出
  /dev/stderr:错误输出
  /dev/fd/N : 某特定文件描述符，如/dev/stdin就相当于/dev/fd/0
```
示例

`awk -F: '{printf "%-15s %i\n",$1,$3 > "/dev/stderr"}' /etc/passwd`