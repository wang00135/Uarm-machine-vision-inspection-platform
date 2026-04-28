# 把代码全部放到try中
try:
    # 把try中放置的是有可能出现错误的代码
    print('hello')
    print(10 / 0)
except:
    # except中放置的是出错以后的处理措施
    print("哈哈哈，出错了~~~")

# try...except...else...结构
a_list = ['左正蹬', '右鞭腿', '左刺拳']
while True:
    n = input("请选择出招：")
    try:
        n = int(n)
        print(a_list[n])
    except IndexError:
        print("下标越界或格式不正确，请重新输入出招内容")
    else:
        break

# 带有多个except的try结构
a_list = ['左正蹬', '右鞭腿', '左刺拳']
while True:
    n = input("请选择出招：")
    try:
        n = int(n)
        print(a_list[n])
    except NameError:
        print('NameError')
    except IndexError:
        print("下标越界或格式不正确，请重新输入出招内容")
    except ZeroDivisionError:
        print('ZeroDivisionError')
    else:
        break

# try...except...finally结构
a_list = ['左正蹬', '右鞭腿', '左刺拳']
while True:
    n = input("请选择出招：")
    try:
        n = int(n)
        print(a_list[n])
    except IndexError:
        print("下标越界或格式不正确，请重新输入出招内容")
    finally:
        print("看来是有备而来，来，骗，来，偷袭，我这个69岁的老同志，这好吗？这不好。")
