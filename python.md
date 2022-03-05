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
