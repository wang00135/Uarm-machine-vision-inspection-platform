#!/usr/bin/env python3

a = True
b = False
if a and b:
    print("1 - 变量 a 和 b 都为 true")
else:
    print("1 - 变量 a 和 b 至少有一个不为 true")

if a or b:
    print("2 - 变量 a 和 b 至少有一个为 True")
else:
    print("2 - 变量 a 和 b 都为 false")

if not a:
    print("3 - 变量 a 为 false")
else:
    print("3 - 变量 a 为 true")


# 短路规则
# 1 在计算 a and b 时，如果 a 是 False，则根据与运算法则，整个结果必定为 False，因此返回 a；如果 a 是 True，则整个计算结果必定取决与 b，因此返回 b。

# 2. 在计算 a or b 时，如果 a 是 True，则根据或运算法则，整个计算结果必定为 True，因此返回 a；如果 a 是 False，则整个计算结果必定取决于 b，因此返回 b。

# 短路计算 提高
if 1 and 0 or 5:
    print("?")  # 会打印吗？

if 'b' and None or 'k' and 0 or 'r' and 'c':
    print("??")  # 会打印吗？


flage = 0 and 'bkrc'
print(flage)  # 0

flage = -1 and 'bkrc'
print(flage)  # bkrc

flage = 0 or 'python3'
print(flage)  # python3

flage = -1 or 'bkrc'
print(flage)  # bkrc

