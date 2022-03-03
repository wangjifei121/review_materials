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
