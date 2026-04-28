
# 多态
# 定义两个类
class A:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class B:
    def __init__(self, name):
        self._name = name

    def __len__(self):
        return 10

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class C:
    pass


a = A("孙悟空")
b = B("猪八戒")
c = C()


def say_hello(obj):
    print("你好 %s" % obj.name)


say_hello(a)
say_hello(b)
# say_hello(c)

'''
类型检查
    issubclass(obj, sub) - 判断一个类是另一个类的子类或者子孙类。
    isinstance(obj, Class) - 如果obj是Class类的实例对象或者是一个Class子类的实例对象则返回true。
注意：类型检查违反了多态原则，这会导致程序的适应性非常差，注意使用场合。
'''


def say_hello(obj):
    if isinstance(obj, A):
        print("你好 %s" % obj.name)


say_hello(a)
say_hello(b)
