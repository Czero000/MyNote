在你使用 Python 脚本像终端输出信息时，你可能希望增加一些样式来区分不同的结果。一个方法是通过增加颜色或背景色。Python 允许通过增加颜色或风格使标准输出风格化，例如

```
#!/usr/bin/env python
# encoding: utf-8

class Styles:
    HEADER = '\033[35m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

    @staticmethod
    def log_normal(info):
        print Styles.HEADER + info + Styles.ENDC                                                                                              

    @staticmethod
    def log_warning(info):
        print Styles.WARNING + info + Styles.ENDC

    @staticmethod
    def log_fail(info):
        print Styles.FAIL + info + Styles.ENDC

print Styles.BLUE + "Hello, this is a test string" + Styles.ENDC
print Styles.BOLD + "Hello, this is a test string" + Styles.ENDC
print Styles.UNDERLINE + "Hello, this is a test string" + Styles.ENDC

Styles.log_normal("Hello, this is a test string")
Styles.log_warning("Hello, this is a test string")
Styles.log_fail("Hello, this is a test string")
```
上面这些是通过 ANSI 转义序列定义的一些基本风格，在 Linux、 OS X或者 Window 10 上都可以生效。当然除此之外，还可以通过模块来实现

使用 [colorama](https://pypi.python.org/pypi/coloramahttps://pypi.python.org/pypi/coloramahttps://pypi.python.org/pypi/colorama) 来实现跨平台的风格支持。
```
#!/usr/bin/env python
# encoding: UTF-8

from colorama import Fore, Back, Style                                                                                                        

print Fore.RED + "Hello, This is a test string"
print Back.GREEN + "Hello, This is a test string"
print Style.DIM + "Hello, This is a test string"
print Style.RESET_ALL
print "Hello, This is a test string"
```
还有一些其他库，例如 [termcolor](https://pypi.python.org/pypi/termcolor) 和 [blessings](https://pypi.python.org/pypi/blessings),当然如果你不愿意添加额外库，可以用上面的类创建一个装饰器，这样就可以用来打印特定风格的文本了。

**ansi控制码**
```

\33[0m 关闭所有属性
\33[1m 设置高亮度
\33[4m 下划线
\33[5m 闪烁
\33[7m 反显
\33[8m 消隐
\33[30m -- \33[37m 设置前景色
字颜色:30-----------37
30:黑 
31:红
32:绿
33:黄
34:蓝色
35:紫色
36:深绿
37:白色

\33[40m -- \33[47m 设置背景色
字背景颜色范围:40----47
40:黑
41:深红
42:绿
43:黄色
44:蓝色
45:紫色
46:深绿
47:白色
\33[90m -- \33[97m 黑底彩色
90:黑
91:深红
92:绿
93:黄色
94:蓝色
95:紫色
96:深绿
97:白色

\33[nA 光标上移n行
\33[nB 光标下移n行
\33[nC 光标右移n行
\33[nD 光标左移n行
\33[y;xH设置光标位置
\33[2J 清屏
\33[K 清除从光标到行尾的内容
\33[s 保存光标位置
\33[u 恢复光标位置
\33[?25l 隐藏光标
\33[?25h 显示光标
```
