
# 继承
class People:
    # 构造方法
    def __init__(self, n, a):
        self.name = n
        self.age = a

    def info(self):
        print("我叫 %s ，今年 %d 岁" % (self.name, self.age))


'''
单继承
    父类中的所有方法都会被子类继承，包括特殊方法，也可以重写特殊方法
'''


class Student(People):
    def __init__(self, n, a, g):
        super().__init__(n, a)
        self.grade = g

    # 覆写父类的方法
    def info(self):
        print("我叫 %s ，今年 %d 岁，正在读 %s" % (self.name, self.age, self.grade))


s = Student("Ken", 19, "大一")
s.info()

'''
多重继承
    在Python中是支持多重继承的，可以在类名的()后边添加多个类，来实现多重继承
    需要注意圆括号中父类的顺序，若是父类中有相同的方法名，而在子类使用时未指定，python从左至右搜索 即方法在子类中未找到时，从左到右查找父类中是否包含方法。
'''


class DeepLearn:
    def aims(self):
        print("我的目标是学习深度学习")


class BigDate:
    def aims(self):
        print("我的目标是学习大数据")


class AIStudent(People, DeepLearn, BigDate):
    def __init__(self, n, a, g):
        People.__init__(n, a)
        self.grade = g

    # 覆写父类的方法
    def info(self):
        print("我叫 %s ，今年 %d 岁，正在读 %s" % (self.name, self.age, self.grade))


ais = AIStudent("Jim", 20, "大二")
ais.info()
ais.aims()
