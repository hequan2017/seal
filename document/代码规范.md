# python 开发规范

## 代码检查工具
### 工具
* pylint  
* pycharm --> code --> Reformat Code  格式化当前文件代码格式
* pycharm --> 右击项目 --> Inspect Code  根据pep8格式检查当前项目.

### 提交
* 每次提交代码前，自己 Inspect Code检查一遍代码，尽量修改错误格式。
* 禁止直接修改master分支，用子分支去提交，然后合并代码。
* 需要在提交commit里面，写明修改内容。



## 概述
### 编码
* 如无特殊情况, 文件一律使用 UTF-8 编码
* 文件头设置
```
#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
```


### 代码格式

* 统一使用 4 个空格进行缩进(pycharm会自动把tab换成4个空格)
* 编辑器 为pycharm
* 每行代码尽量不超过 80 个字符(在特殊情况下可以略微超过 80 ，但最长不得超过 120)

### 导入
```
import x
from x import y
from x import y as z

禁止import  x,y
```

### 字符格式化
`使用  f'{name}{value}'`


### 异常
* 使用 as 
* 不推荐使用 Exception 抓取报错，尽量缩小报错类型
```
try:
    raise Error
except Exception as error:
    pass
```


### 长语句缩进
编写长语句时，可以使用换行符""换行。在这种情况下，下一行应该与上一行的最后一个“.”句点或“=”对齐，或者是缩进4个空格符。

```
this_is_a_very_long(function_call, 'with many parameters') \
    .that_returns_an_object_with_an_attribute

MyModel.query.filter(MyModel.scalar > 120) \
             .order_by(MyModel.name.desc()) \
             .limit(10)
```

如果你使用括号“()”或花括号“{}”为长语句换行，那么下一行应与括号或花括号对齐：
```
this_is_a_very_long(function_call, 'with many parameters',
                    23, 42, 'and even more')
```
对于元素众多的列表或元组，在第一个“[”或“(”之后马上换行：
```
items = [
    'this is the first', 'set of items', 'with more items',
    'to come in this line', 'like this'
]
```

### 空行
顶层函数与类之间空两行，此外都只空一行。不要在代码中使用太多的空行来区分不同的逻辑模块。

```
def hello(name):
    print('Hello %s!' % name)

class MyClass(object):
    """This is a simple docstring."""

    def __init__(self, name):
        self.name = name

    def get_annoying_name(self):
        return self.name.upper() + '!!!!111'
```

### 空格规则
单目运算符与运算对象之间不空格（例如，-，~等），即使单目运算符位于括号内部也一样。
双目运算符与运算对象之间要空格

```
exp = -1.05
value = (item_value / item_count) * offset / exp
value = my_list[index]
value = my_dict['key']
```


### 比较

* 任意类型之间的比较，使用“isinstance(L, list)”和“not isinstance(L, list)”
* 与单例（singletons）进行比较时，使用 is 和 is not。
* 永远不要与True或False进行比较（例如，不要这样写：foo == False，而应该这样写：if not foo）。
* 否定成员关系检查, 使用 foo not in bar，而不是 not foo in bar。


### 命名约定
* 类名称：采用骆驼拼写法（CamelCase)。
* 类里面的 私有函数在函数前加一个下划线_
* 变量名：小写_以及_下划线（lowercase_with_underscores）。
* 方法与函数名：小写_以及_下划线（lowercase_with_underscores）。
* 常量：大写_以及_下划线（UPPERCASE_WITH_UNDERSCORES）。
* 预编译的正则表达式：name_re。
* 受保护的元素以一个下划线为前缀。双下划线前缀只有定义混入类（mixin classes）时才使用。
* 如果使用关键词（keywords）作为类名称，应在名称后添加后置下划线（trailing underscore）。 允许与内建变量重名，不要在变量名后添加下划线进行区分。如果函数需要访问重名的内建变量，请将内建变量重新绑定为其他名称。
* 命名要有寓意, 不使用拼音,不使用无意义简单字母命名 (循环中计数例外 for i in)
* 命名缩写要谨慎, 尽量是大家认可的缩写
* 尽量 避免使用全局变量, 用类变量来代替


### 函数和方法的参数：
* 类方法：cls 为第一个参数。
* 实例方法：self 为第一个参数。
* property函数中使用匿名函数（lambdas）时，匿名函数的第一个参数可以用 x 替代， 例如：display_name = property(lambda x: x.real_name or x.username)。
* 禁止参数里面 直接写  字符id，用其他替代，例如 asset_id

## 文档
### 文档注释（Docstring，即各方法，类的说明文档注释）
所有文档字符串均以 reStructuredText 格式编写，方便 Sphinx 处理。文档字符串的行数不同，布局也不一样。 如果只有一行，代表字符串结束的三个引号与代表字符串开始的三个引号在同一行。 如果为多行，文档字符串中的文本紧接着代表字符串开始的三个引号编写，代表字符串结束的三个引号则自己独立成一行。 （有能力尽可能用英文, 否则请中文优雅注释）

```

def foo():
    """This is a simple docstring."""


def bar():
    """This is a longer docstring with so much information in there    
    that it spans three lines.  In this case, the closing triple quote    
    is on its own line.    
    """
```

文档字符串应分成简短摘要（尽量一行）和详细介绍。如果必要的话，摘要与详细介绍之间空一行。

### 注释（Comment）类 函数 注释

```
def AvailableZones(self, instance_charge_type, region_id):
    """
    功能: 可用区
    :param instance_charge_type: 计费方式
    :param region_id:    地域
    :return:  ['cn-huhehaote-a', 'cn-huhehaote-b']
    """
```






