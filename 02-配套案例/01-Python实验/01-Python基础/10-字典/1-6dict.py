my_dict = {'Name': 'bkrc', 'Age': 10, 'Site': 'beijing'}

# 访问字典
print("名称：", my_dict['Name'])
print("年龄：", my_dict['Age'])
print("地点：", my_dict['Site'])

# 修改字典
my_dict["Age"] = 20
print("修改后的年龄：", my_dict['Age'])

# 删除字典
del my_dict["Age"]
print(my_dict)