### split 初始化和类型强制 
awk的内建函数split允许你把一个字符串分隔为单词并存储在数组中。你可以自己定义域分隔符或者使用现在FS(域分隔符)的值。

格式

```shell
split (string, array, field separator)
split (string, array)  -->如果第三个参数没有提供，awk就默认使用当前FS值。
```
* 替换分隔符

```shell
time="12:34:56"
out=`echo $time | awk '{split($0,a,":");print a[1],a[2],a[3]}'`
echo $out
```

```shell
// 计算指定范围内的和(计算每个人1月份的工资之和)
cat test.txt
Tom　　  2012-12-11      car     53000
John　　 2013-01-13      bike    41000
vivi    2013-01-18      car     42800
Tom　　  2013-01-20      car     32500
John　　 2013-01-28      bike    63500

awk '{split($2,a,"-");if(a[2]==01){b[$1]+=$4}}END{for(i in b)print i,b[i]}' test.txt  
vivi 2800
Tom2500
John4500
```

### substr 截取字符串 ###

返回从起始位置起，指定长度之子字符串；若未指定长度，则返回从起始位置到字符串末尾的子字符串。

格式：
substr(s,p) 返回字符串s中从p开始的后缀部分
substr(s,p,n) 返回字符串s中从p开始长度为n的后缀部分

```shell
echo "123" | awk '{print substr($0,1,1)}'
\\ awk -F ',' '{print substr($3,6)}'    --->  表示是从第3个字段里的第6个字符开始，一直到设定的分隔符","结束.
\\ substr($3,10,8)  --->  表示是从第3个字段里的第10个字符开始，截取8个字符结束.
\\ substr($3,6)     --->  表示是从第3个字段里的第6个字符开始，一直到结尾
```

### length 字符串长度 ###
length函数返回没有参数的字符串的长度。length函数返回整个记录中的字符数。
```
echo "123" | awk '{print length}'
```

### gsub函数

gsub函数则使得在所有正则表达式被匹配的时候都发生替换。`gsub(regular expression, subsitution string, target string)`;简称`gsub（r,s,t)`

举例：把一个文件里面所有包含 abc 的行里面的 abc 替换成 def，然后输出第一列和第三列

```
awk '$0 ~ /abc/ {gsub("abc", "def", $0); print $1, $3}' abc.txt
```