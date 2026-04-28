import random


class MyFriend:
    MyFriendNum = 0
    __weight = 0

    def __init__(self, name, salary, meiLi):
        self.name = name;
        self.salary = salary
        self.meiLi = meiLi
        self.qinMiDu = 0
        self.diffLevel = random.randint(10, 40)
        MyFriend.MyFriendNum += 1

    def wechat(self):
        self.qinMiDu = random.randint(0, 20)

    def biaoBai(self):
        if self.meiLi + self.qinMiDu > self.diffLevel:
            print("%s 表白成功，攻略难度：%d，亲密度：%d" % (self.name, self.diffLevel, self.qinMiDu))
        else:
            print("%s 表白失败，攻略难度：%d，亲密度：%d" % (self.name, self.diffLevel, self.qinMiDu))


'''
    MyFriendNum 变量是一个类变量，它的值将在这个类的所有实例之间共享。你可以在内部类或外部类使用 MyFriend.MyFriendNum 访问。
    第一种方法__init__()方法是一种特殊的方法，被称为类的构造函数或初始化方法，当创建了这个类的实例时就会调用该方法
    self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。
'''

mf1 = MyFriend("诸葛大力", 200, 8)
mf2 = MyFriend("冯宝宝", 100, 8)

print("我的朋友数：%d" % MyFriend.MyFriendNum)

mf1.wechat();
mf1.biaoBai();

mf2.wechat();
mf2.biaoBai();

'''
目前我们可以直接通过 对象.属性 的方式来修改属性的值，这种方式导致对象中的属性可以随意修改，非常的不安全
现在我们就需要一种方式来增强数据的安全性
    1.属性不能随意修改（我让你改你才能改，不让你改你就不能改）
    2.属性不能修改为任意的值（年龄不能是负数）

添加，删除，修改类的属性
'''
mf1.nanYouLi = 50  # 添加一个 'nanYouLi' 属性
mf1.meiLi += mf1.nanYouLi  # 修改 'meiLi' 属性
mf1.biaoBai();

del mf1.meiLi  # 删除 'meiLi' 属性
mf1.biaoBai();