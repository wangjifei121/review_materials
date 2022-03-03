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
