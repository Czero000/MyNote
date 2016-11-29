## Python面向对象

Python从设计之初就已经是一门面向对象的语言，正如此，在Python中创建一个类和对象是很容易的

### 面向对象技术简介

- **类(Class):** 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。
- **类变量：** 类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。
- **数据成员：** 类变量或者实例变量用于处理类及其实例对象的相关的数据。
- **方法重写：** 如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。
- **实例变量：** 定义在方法中的变量，只作用于当前实例的类。
- **继承：** 即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）
- **实例化：** 创建一个类的实例，类的具体对象
- **方法：** 类中定义的函数。
- **对象：** 通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法

---

### 创建类

使用class语句创建一个新类，class之后为类的名称并以冒号结尾

```python
class ClassName:
    'class help info'
    class_suite  //类体
```

类的帮助信息可以通过`ClassName.__doc__`查看,`class_suite`由类成员，方法，数据属性组成。
```
#!/usr/bin/python
# -*- coding: UTF-8 -×-

class Employee:
    '所有员工的基类'
    empCount = 0

    def __int__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print "Total Employee %d" % Employee.empCount

    def displayEmployee(self):
        print "Name: ", self.name, ", Salary: ", self,salary
```
- empCount变量是一个类变量，它的值将在这个类的所有实例之间共享，可以在内部类或者使用Employee.empCount访问。
- 第一种方法`__int__()`是一种特殊的方法，被称为累的构造函数或初始化方法，当创建了这个类的实例就会调用该方法。

### 创建实例对象
要创建实例对象，可以使用类的名称，并通过`__int__`方法接受函数
```python
"创建 Employee类的第一个对象"
emp1 = Employee("Zero", 2000)
"创建 Employee类的第二个对象"
emp2 = Employee("Manni", 5000)
```
### 访问属性
可以使用`(.)`来访问对象的属性，使用如下类的名称方位类变量
```
emp1.displayEmployee()
emp2.displayEmployee()
print "Total Employee %d" % Employee.empCount
```
实例
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Employee:
   '所有员工的基类'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary

"创建 Employee 类的第一个对象"
emp1 = Employee("Zara", 2000)
"创建 Employee 类的第二个对象"
emp2 = Employee("Manni", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print "Total Employee %d" % Employee.empCount

//输出
Name :  Zara , Salary:  2000
Name :  Manni , Salary:  5000
Total Employee 2

//添加、删除、修改类的属性
emp1.age = 7
emp1.age = 8
del emp1.age
```
可以使用函数方式来访问属性
- `getattr(obj.name[,default])`: 访问对象属性
- `hasattr(obj.name)`: 检查是否存在一个属性
- `setattr(obj, name, value)` : 设置一个属性。如果属性不存在，会创建一个新属性
- `delattr(obj, name)` : 删除属性

```
hasattr(emp1, 'age')       //如果存在‘age’属性返回True
getattr(emp1, 'age')       //返回‘age’属性的值
setattr(emp1, 'age', 8)    //添加属性'age'值为8
delattr(emp1, 'age')       //删除属性‘age’
```
---

### Python内置属性
- `__dict__`: 类的属性（包含一个字典，有类的数据属性组成）
- `__doc__`: 类的文档字符串
- `__name__`: 类名
- `__module__`: 类定义所在的模块（类的全名是'__main__.ClassName'，如果类唯一一个导入模块mymod中，那么ClassName.__module__ 等于mymod）
- `__bases__`: 类的所有父类构成元素(包含了以个由所有父类组成的元组)

python内置类属性调用实例如下

```python
#!/usr/bin/python
# -*- coding: UTF-8 -×-

class Employee:
    '所有员工的基类'
    empCount = 0

    def __int__(self, name, salary):
        self.name = Name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print "Total Employee %d" % Employee.empCount

    def displayEmployee(self):
        print "Name: ",self.name, ", Salary: ", self.salary

print "Employee.__doc__ :", Employee.__doc__
print "Employee.__name__ :", Employee.__name__
print "Employee.__module__ :", Employee.__module__
print "Employee.__bases__ :", Employee.__bases__
print "Employee.__dict__ :", Employee.__dict__

// 输出
Employee.__doc__ : 所有员工的基类
Employee.__name__ : Employee
Employee.__module__ : __main__
Employee.__bases__ : ()
Employee.__dict__ : {'__int__': <function __int__ at 0x7f0f065b3668>, '__module__': '__main__', 'displayCount': <function displayCount at 0x7f0f065b36e0>, 'empCount': 0, 'displayEmployee': <function displayEmployee at 0x7f0f065b3758>, '__doc__': '\xe6\x89\x80\xe6\x9c\x89\xe5\x91\x98\xe5\xb7\xa5\xe7\x9a\x84\xe5\x9f\xba\xe7\xb1\xbb'}
```
---

### Python对象销毁(垃圾回收)
同JAVA语言一样，Python使用引用计数这一简单技术来追踪内存中的对象。在python内部基类着所有使用中的对象各有多少引用。一个内部追踪表里，称为一个引用计数器。当对象被创建时，就创建了一个引用计数，当这个对象不需要时，即对象的引用计数变为0时，它被垃圾回收。但是回收不是立即的，有解释器在适当的时机，将对象占用的内存空间回收。
```
a = 40          //创建对象 <40>
b = a           //增加对象,<40>的计数
c = [b]         //增加引用，<40>的计数

del a           //减少引用，<40>的计数
b = 100         //减少引用，<40>的计数
c[0] = -1       //减少引用，<40>的计数
```
垃圾回收机制不仅针对引用计数为0的对象，同样也可以处理循环引用的情况。循环引用指的是，两个对象相互引用，但是没有其他变量引用他们。这种情况下，仅使用引用计数是不够的。Python 的垃圾收集器实际上是一个引用计数器和一个循环垃圾收集器。作为引用计数的补充， 垃圾收集器也会留心被分配的总量很大（及未通过引用计数销毁的那些）的对象。 在这种情况下， 解释器会暂停下来， 试图清理所有未引用的循环。

- 实例
  析构函数`__del__`,`__del__`在对象销毁的时候被调用，当对象不在被使用时，`__del__`运行

```
#!/usr/bin/python
# -*- coding: UTF-8 -×-

class Point:
    def __init__(self, x=0, y=0):
      self.x = x
      self.y = y

    def  __del__(self):
      class_name = self.__class__.__name__
      print class_name, "销毁"

pt1 = Point()
pt2 = pt1
pt3 = pt1
print id(pt1), id(pt2), id(pt3) ##打印对象ID

del pt1
del pt2
del pt3

//输出
140248542263848 140248542263848 140248542263848
Point 销毁
```
通常需要在单独的文件中定义一个类

### 类的继承
面向对象的编程带来的好处之一是代码的重用，实现这种重用的方法之一是通过继承机制。继承完全可以理解成类之间的类型和子类型关系。
注意：继承语句`class`派生类名（基类名）://...基类名写作括号里，基本类实在类定义的时候，在元组之间指明的。
在python中继承中的一些特定：
- 在继承中基类的构造(__init__()方法)不会被自动调用，它需要在起派生累的构造中亲自专门调用
- 在调用基类的方法时，需要加上基类的类名前缀，且需要带上self参数变量。区别于在类中调用普通函数时并不需要带上self参数
- python总是首先查找对应类型方法，如果它不能在派生类中找到对应的方法，它才开始到基类中逐个查找。（先在本类中查抄调用方法，找不到才去基类中找）

语法：派生类的声明与它们的父类类似，继承的基类列表跟在类名之后
```
class SubClassName (ParentClass1[, ParentClass2, ....])
  'Optional class documentation string'
  class_suite
```

```
#!/usr/bin/python env
# -*- coding: UTF-8 -×-

class Parent:      ##定义父类
  parentAttr = 100
  def __init__(self):
      print "调用父类构造函数"

  def parentMethod(self):
     print "调用父类方法"

  def setAttr(self, attr):
      Parent.parentAttr = attr

  def getAttr(self):
      print "父类属性 :",Parent.parentAttr

class Child(Parent):  ##定义子类
  def __init__(self):
      print "调用子类构造方法"

  def childMethod(self):
      print '调用子类方法 childMethod'

c = Child()
c.childMethod()
c.parentMethod()
c.setAttr(200)
c.getAttr()

//输出
调用子类构造方法
调用子类方法 childMethod
调用父类方法
父类属性 : 200
```
可以使用issubclass()或者isinstance()方法来检测
- issubclass() - 布尔函数判断一个类是另一个类的子类或者孙类，语法 `issubclass(sub,sup)`
- isinstance() - 布尔函数如果obj是Class类的实例对象或者是一个class子类的石磊对象返回true。

### 方法重写
如果父类方法的功能不能满足需求，可以在子类重写父类方法
```
#!/usr/bin/python env
# -*- coding: UTF-8 -×-

class Parent:
    def myMethod(self):
        print "调用父类方法"

class Child(Parent):
    def myMethod(self):
        print '调用子类方法'

c = Child()
c.myMethod()
//输出
调用子类方法
```

## 基础重载方法

下表列出了一些通用的功能，你可以在自己的类重写：

| 序号   | 方法, 描述 & 简单的调用                           |
| ---- | ---------------------------------------- |
| 1    | ``__init__ ( self [,args...] )``构造函数简单的调用方法: *obj = className(args)* |
| 2    | ``__del__( self )``析构方法, 删除一个对象简单的调用方法 : *dell obj* |
| 3    | ``__repr__( self )``转化为供解释器读取的形式简单的调用方法 : *repr(obj)* |
| 4    | ``__str__( self )``用于将值转化为适于人阅读的形式简单的调用方法 : *str(obj)* |
| 5    | ``__cmp__ ( self, x )``对象比较简单的调用方法 : *cmp(obj, x)* |

------

## 运算符重载

Python同样支持运算符重载，实例如下：

```
#!/usr/bin/python

class Vector:
   def __init__(self, a, b):
      self.a = a
      self.b = b

   def __str__(self):
      return 'Vector (%d, %d)' % (self.a, self.b)

   def __add__(self,other):
      return Vector(self.a + other.a, self.b + other.b)

v1 = Vector(2,10)
v2 = Vector(5,-2)
print v1 + v2
```

以上代码执行结果如下所示:

```
Vector(7,8)
```

## 类属性与方法

### 类的私有属性

**__private_attrs**：两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时 **self.__private_attrs**。

### 类的方法

在类地内部，使用def关键字可以为类定义一个方法，与一般函数定义不同，类方法必须包含参数self,且为第一个参数

### 类的私有方法

**__private_method**：两个下划线开头，声明该方法为私有方法，不能在类地外部调用。在类的内部调用 **self.__private_methods**

### 实例

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

class JustCounter:
	__secretCount = 0  # 私有变量
	publicCount = 0    # 公开变量

	def count(self):
		self.__secretCount += 1
		self.publicCount += 1
		print self.__secretCount

counter = JustCounter()
counter.count()
counter.count()
print counter.publicCount
print counter.__secretCount  # 报错，实例不能访问私有变量
```

Python 通过改变名称来包含类名:

```
1
2
2
Traceback (most recent call last):
  File "test.py", line 17, in <module>
    print counter.__secretCount  # 报错，实例不能访问私有变量
AttributeError: JustCounter instance has no attribute '__secretCount'
```

Python不允许实例化的类访问私有数据，但你可以使用 **object._className__attrName** 访问属性，将如下代码替换以上代码的最后一行代码：

```
.........................
print counter._JustCounter__secretCount
```
