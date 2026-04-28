# 定义一个简单的类
class MyObject:

    def info(self):
        print(" This is My Object ")

    def __init__(self, c):
        self.type = c  # 定义实例属性
        print(" init ")


mo1 = MyObject("男生")  # 实例化对象
mo1.info()
print(mo1.type)

mo2 = MyObject("女生")
print(mo1)
print(mo2)
print(type(mo1) == type(mo2))

'''
创建类对象的流程
    1.创建一个变量
    2.在内存中创建一个新对象
    3.__init__(self)方法执行
    4.将对象的id赋值给变量
'''


class MyFriend:
    MyFriendNum = 0  # 定义类属性(变量),它的值将在这个类的所有实例之间共享。你可以在内部类或外部类使用 MyFriend.MyFriendNum 访问

    def __init__(self, name, salary):
        self.name = name;
        self.salary = salary
        MyFriend.MyFriendNum += 1


mf1 = MyFriend("诸葛大力", 200)
mf2 = MyFriend("冯宝宝", 100)
print("我的朋友数：%d" % MyFriend.MyFriendNum)

'''
匿名类
    type(object)：返回对象的类型
    type(name, bases, dict)：返回新的类型对象
        name：类的名称。
        bases：基类的元组。
        dict：字典，类内定义的命名空间变量。
'''
X = type('XObject', (object,), dict(a=1))  # 产生一个新的类型 X
print(X)
print(type(X))
