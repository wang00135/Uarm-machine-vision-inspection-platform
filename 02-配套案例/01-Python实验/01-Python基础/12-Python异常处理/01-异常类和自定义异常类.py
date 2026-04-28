class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr("111" + self.value)


def add(a, b):
    # 如果a和b中有负数，就向调用处抛出异常
    if a < 0 or b < 0:
        # raise用于向外部抛出异常，后边可以跟一个异常类，或异常类的实例
        # raise Exception
        # 抛出异常的目的，告诉调用者这里调用时出现问题，希望你自己处理一下
        # raise Exception('两个参数中不能有负数！')
        raise MyError('自定义的异常')

        # 也可以通过if else来代替异常的处理
        # return None
    r = a + b
    return r


print(add(-123, 456))

'''
如果自己编写的某个模块需要抛出多个不同但相关的异常，
可以先创建一个基类，然后创建多个派生类分别表示不同的异常。
'''
class HerError(MyError):
    pass

class HisError(MyError):
    pass