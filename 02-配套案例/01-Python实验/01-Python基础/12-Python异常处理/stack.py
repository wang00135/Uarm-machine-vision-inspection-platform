
"""
栈：栈是一种“后进先出”或"先进后出"的数据结构，Python列表本身就可以实现栈结构的基本操作。
例如，列表对象的append()方法是在列表尾部追加元素，类似于入栈操作；pop()方法默认是弹出并返回列表的最后一个元素，类似于出栈操作。
但是直接使用Python列表对象模拟栈操作并不是很方便，
例如，当列表为空时，若再执行pop()出栈操作，则会抛出一个异常；另外也无法限制栈的大小。

下面的代码使用列表模拟栈结构的用法，实现了入栈、出栈、判断栈是否为空、是否已满以及改变栈大小等操作
"""


class Stack:

    def __init__(self, size=10):
        self._content = []  # 使用列表存放栈的元素
        self._size = size  # 初始栈大小
        self._current = 0  # 栈中元素个数初始化为0

    def empty(self):
        self._content = []
        self._current = 0

    def isEmpty(self):
        if not self._content:
            return True
        else:
            return False

    def setSize(self, size):
        # 如果缩小栈空间，则删除指定大小之后的已有元素
        if size < self._current:
            for i in range(size, self._current)[::-1]:
                del self._content[i]
            self._current = size
        self._size = size

    def isFull(self):
        if self._current == self._size:
            return True
        else:
            return False

    def push(self, v):
        if len(self._content) < self._size:
            self._content.append(v)
            self._current = self._current + 1  # 栈中元素个数加1
        else:
            print('Stack Full!')

    def pop(self):
        if self._content:
            self._current = self._current - 1  # 栈中元素个数减1
            return self._content.pop()
        else:
            print('Stack is empty!')

    def show(self):
        print(self._content)

    def showRemainderSpace(self):
        print('Stack can still PUSH ', self._size - self._current, ' elements.')



if __name__ == '__main__':
    # myStack = []
    # myStack.append(3)
    # myStack.append(5)
    # myStack.append(7)
    # print(myStack)  # [3,5,7]
    # myStack.pop()   # 7
    # myStack.pop()   # 5
    # myStack.pop()   # 3
    # myStack.pop()   # IndexError:pop from empty list
    print('Please use me as a module.')
    s = Stack()
    s.isEmpty()     # true
    s.isFull()      # false
    s.push(5)
    s.push(8)
    s.push('a')
    s.pop()
    s.push('b')
    s.push('c')
    s.show()        # [5, 8, 'b', 'c']
    s.showRemainderSpace()  # Stack can still PUSH  6  elements.
    s.setSize(3)
    s.isFull()
    s.show()        # [5, 8, 'b']
    s.setSize(5)
    s.push('d')
    s.push('dddd')
    s.push(3)       # Stack Full!
    s.show()        # [5, 8, 'b', 'd', 'dddd']

