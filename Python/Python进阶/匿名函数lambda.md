# 匿名函数 lambda
python 使用 lambda 创建匿名函数，匿名函数就是不适用 `def` 语句定义函数，语法
```
lambda [arg1[, arg2, ... argN]]: expression
```
其中，参数是可选的，如果使用参数，参数通常也会在表达式中


- 无参数

```
// 使用函数定义
def true():
    return true

// 等价表达式
lambda :true

// 保留 lambda 对象到变量中
true = lambda: True
true()
True
```
- 含参数

```
// 使用def定义的函数
def add( x, y ):
    return x + y

// 使用lambda的表达式
lambda x, y: x + y

// lambda也允许有默认值和使用变长参数
lambda x, y = 2: x + y
lambda *z: z

// 调用lambda函数
a = lambda x, y: x + y
a( 1, 3 )
4

b = lambda x, y = 2: x + y
b( 1 )
3
b( 1, 3 )
4

c = lambda *z: z
c( 10, 'test')
(10, 'test')
```
