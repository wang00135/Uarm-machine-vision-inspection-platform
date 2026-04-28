myList = [1, 2, 'a', 'b']

# 访问列表
print("第一个元素", myList[0])
print("第二个元素", myList[1])
print("第三个元素", myList[2])
print("第四个元素", myList[3])

# 更新列表
# 更新把列表中的a元素更新为3
myList[2] = 3
print("更新后的列表",myList)

# 删除列表中元素
# 删除列表中的b元素
del myList[3]
print("删除b元素",myList)

# 过去列表元素个数
print("列表元素个数",len(myList))