import sys

# 我们目前所学习的对象都是Python内置类的对象
a = "10" # 创建一个str类的实例
b = str("hello") # 创建一个str类的实例
print(a, type(a))
print(b, type(b))

'''
对象的创建流程:
    1.声明变量
    2.在内存中创建一个新对象
    3.将对象的id赋值给变量
'''

# id()是python的内置函数，用于返回对象的身份，即对象的内存地址。

c = a
print(id(a))
print(id(c))

'''
变量引用区别
  Python 缓存了整数和字符串，因此每个对象在内存中只存有一份，引用所指对象就是相同的，即使使用赋值语句，也只是创造新的引用，而不是对象本身；
  Python 没有缓存列表及其他对象，可以由多个相同的对象，可以使用赋值语句创建出新的对象。
'''
# 通过is进行引用所指判断，is是用来判断两个引用所指的对象是否相同。
print(a is c)

d = 1
e = 1
print(d is e)

d = "good"
e = "good"
print(d is e)

d = "hello world"
e = "hello world"
print(d is e)

d = []
e = []
print(d is e)

'''
引用计数
    变量：通过变量指针引用对象，变量指针指向具体对象的内存空间，取对象的值。
    对象：类型已知，每个对象都包含一个头部信息（头部信息：类型标识符和引用计数器）
    sys.getrefcount()：每个对象都有指向该对象的引用总数
'''
print(sys.getrefcount(b))
print(sys.getrefcount("hello"))
# ps:当使用某个引用作为参数，传递给getrefcount()时，参数实际上创建了一个临时的引用。因此，getrefcount()所得到的结果，会比期望的多1。
print(b , type(b))
print(b , type(type(b)))
print(b , type(type(type(b))))
print(b , id(b))
print(b , id(type(b)))
print(b , id(type(type(b))))
print(b , id(type(type(type(b)))))
print(b , id(type(type(type(type(b))))))
print(a , id(type(type(type(type(a))))))
