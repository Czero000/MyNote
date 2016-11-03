### Python字典

字典是一个可变容器模型， 可以存储任意类型对象。字典的每个键值(Key=>value)对用冒号`:`分隔，每对之剑用逗号`,`分隔，整个字典包括在花括号`{}`中。

```
dictionary =  {key1 : value1, key2 : value2}
```

键必须是唯一的，但是键值则不必。键可以取任意数据类型，但键必须是不可变的，如字符串、数字、元组。

```
dict1 = {'Alice': '2341', 'Beth': '9192', 'Cecil'： '3258'}
dict2 = {'abc': 456}
dict3 = {'abc': 123, 98.6: 37}
```

---

#### 访问字典的值

把相应的键放到方括号中即可

```Python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

dict = {'Name': 'Zero', 'Age': 17, 'Class': 'First'};

print "dict['Name']: ", dict['Name'];
print "dict['Age']: ", dict['Age'];
print "dict['Ages']: ", dict['Ages'];
// 输出
dict['Name']:  Zero
dict['Age']:  17
dict['Ages']:
Traceback (most recent call last):
  File "dict_1.py", line 8, in <module>
    print "dict['Ages']: ", dict['Ages'];
KeyError: 'Ages'
```

如果用字典没有的键访问数据，会报错

---

#### 修改字典

向字段添加新内容的方法是增加新的`key-value`，修改或者删除已有`key-value`

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
dict = {'Name': 'Zero', 'Age': 17, 'Class': 'First'};

dict['Age'] = 8;
dict ['School'] = 'DPS School';

print "dict[Age]:" , dict['Age'];
print "dict[School] :", dict['School'];
// 输出
dict[Age]: 8
dict[School] : DPS School
```

---

#### 删除字典元素

可以删除单一的元素也可以清空字典

```python
// 脚本
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
dict = {'Name': 'Zero', 'Age': 17, 'Class': 'First'};

del dict['Name']; //删除‘Name’键
dict.clear()       // 清空字典
del dict           // 删除字典

print "dict[Age]:" , dict['Age'];
print "dict[School] :", dict['School'];
//输出
dict[Age]:
Traceback (most recent call last):
  File "dict_del.py", line 9, in <module>
    print "dict[Age]:" , dict['Age'];
TypeError: 'type' object has no attribute '__getitem__'
[root@comp python]#
```
