## 装饰器执行流程
```
def deco_1(func):
    print('enter func deco 1')

    def wrapper(a, b):
        print('enter into deco 1 wrapper')
        func(a, b)
        print('over deco 1')

    return wrapper


def deco_2(func):
    print('enter func deco 2')

    def wrapper(a, b):
        print('enter into deco 2 wrapper')
        func(a, b)
        print('over deco 2')

    return wrapper


@deco_1
@deco_2
def add_func(a, b):
    print('result = %d' % (a + b))


add_func(3, 4)

```
## python数据结构
 - dict：字典通常也被称为映射、散列表、查找表或关联数组。字典能够高效查找、插入和删除任何与给定键关联的对象O(1)。解决hash碰撞的方式常见的有开放寻址法、再哈希法、链地址法等
 - list：可变动态数组
 - tuple：不可变容器
 - set：实现方式类似于dict

## filter
```
nums = range(2, 20)
for i in nums:
    nums = filter(lambda x: x == i or x % i, nums)
print(list(nums))

```
## 类的静态方法、普通方法和类方法
- 静态方法: 用 @staticmethod 装饰的不带 self 参数的方法叫做静态方法，类的静态方法可以没有参数，可以直接使用类名调用。
- 实例化方法: 默认有个self参数，且只能被实例化对象调用。
- 类方法: 默认有个 cls 参数，可以被类对象和实例化对象调用，需要加上 @classmethod 装饰器
```
class Person:
    _country = 'China'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 普通方法
    # 只能被实例化对象调用
    def get_age(self):
        print(self.age)

    # 类方法（通常作用为修改类内部属性使用）
    # 类对象或实例化对象都可调用
    @classmethod
    def set_country(cls, country):
        cls._country = country
        print(cls._country)

    # 静态方法
    # 类对象或实例化对象都可调用
    @staticmethod
    def show_help():
        h = '''
            - init Person 
            - get age by func get_age
            - set country by func set_country
            - show help by func show_help
        
        '''
        print(h)

# 类的初始化
p = Person('wangjifei', 18)

# 实例化对象调用静态方法
p.show_help()
# 类对象调用静态方法
Person.show_help()

# 实例化对象调用普通方法
p.get_age()
# 类对象调用普通方法（需要传入类实例对象）
Person.get_age(p)

# 实例化对象调用类方法
p.set_country('Singapore')
# 类对象调用类方法
Person.set_country('Singapore')

```
## python类的私有变量和方法
- `__`双下划线开头的类属性或方法为私有方法，在类的内部，python使用一种 name mangling 技术，将私有方法替换成 _classname__membername格式
```
class Person:
    __money = 10000000  # 私有属性 - 资产
    __private_money = 100000  # 私有属性 - 私房钱

    def __init__(self, name):
        self.name = name

    # 私有方法 - 总私产
    def __all_money(self):
        all_money = self.__money + self.__private_money
        print(f'{self.name} 总资产={all_money}')


# 实例化
p = Person('wangjifei')

# 获取普通属性
print(p.name)
# 获取私有属性 - 报错
# print(p.__money)
# 获取私有属性方法(__money -> _Person__money)
print(p._Person__money)

# 调用私有方法(__all_money -> _Person__all_money)
p._Person__all_money()
```

## python上下文管理
- 可以以一种更加优雅的方式，操作（创建/获取/释放）资源，如文件操作、数据库连接
- 可以以一种更加优雅的方式，处理异常
```
class Resource():
    def __enter__(self):
        print('enter to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exception handling')
        print(exc_type)  # 异常类型
        print(exc_val)  # 异常值
        print(exc_tb)  # 异常的错误栈信息
        return False  # True 异常已经被捕获 False 抛出异常

    def operate(self):
        li = []
        print(li[2])


with Resource() as res:
    res.operate()
```
- contextlib第三方扩展包
```
import contextlib

@contextlib.contextmanager
def my_opener(file_name):
    # __enter__方法
    print('__enter__')
    file_handler = open(file_name, 'r')

    # 【重点】：yield
    yield file_handler

    # __exit__方法
    print('__exit__')
    file_handler.close()
    return

with my_opener('/Users/wangjifei/Desktop/NLP/CWTAP_FD/cwtap/asgi.py') as file_in:
    for line in file_in:
        print(line)
```
```
# 异常处理方式
import contextlib

@contextlib.contextmanager
def my_opener(file_name):
    # __enter__方法
    print(' __enter__')
    file_handler = open(file_name, 'r')

    try:
        yield file_handler
    except Exception as exc:
        # deal with exception
        print('the exception was {0}'.format(str(exc)))
    finally:
        print('__exit__')
        file_handler.close()

        return

with my_opener('/Users/wangjifei/Desktop/NLP/CWTAP_FD/cwtap/asgi.py') as file_in:
    for line in file_in:
        line += 100

```
