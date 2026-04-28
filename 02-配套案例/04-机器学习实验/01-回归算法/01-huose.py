#！/usr/bin/env python3


"""导包"""
import matplotlib.pyplot as plt  # plt表示matplotlib的pyplot子库,它提供了和matlab类似的绘图API
from sklearn import linear_model  #导入线性回归模型
from sklearn.preprocessing import PolynomialFeatures  # 导入线性模型和多项式特征构造模块
import numpy as np

"""加载训练数据集，建立回归方程"""
datasets_X = []  # 用来储存房屋尺寸数据
datasets_Y = []  # 用来储存房价
fr = open('prices.txt', 'r')  # 以只读的方式读取数据集所在的文件prices.txt
lines = fr.readlines()  # 一次性读取所有的数据集，返回一个列表
for line in lines:  # 逐行遍历
    items = line.strip().split(',')  # 去除数据集中的不可见字符，并用逗号分割数据
    datasets_X.append(int(items[0]))  # 将读取的数据转换为int型，并分别写入datasets_X和datasets_Y
    datasets_Y.append(int(items[1]))

length = len(datasets_X)  # 求数据集的总长度

datasets_X = np.array(datasets_X).reshape([length, 1])  # 将datasets_X转化为数组，并变为二维，以符合线性回归拟合函数输入参数要求
datasets_Y = np.array(datasets_Y)

"""
    以数据datasets_X的最大值和最小值为范围，
    建立等差数列，方便后续画图
"""
minX = min(datasets_X)
maxX = max(datasets_X)
X = np.arange(minX,maxX).reshape([-1,1])

"""
    degree=2表示建立datasets_X的二次多项式特征X_poly。
    然后创建线性回归，使用线性模型学习X_poly和datasets_Y之间的映射关系（即参数）。
"""
poly_reg = PolynomialFeatures(degree = 2)
X_poly = poly_reg.fit_transform(datasets_X)
lin_reg_2 = linear_model.LinearRegression()
lin_reg_2.fit(X_poly, datasets_Y)


"""
    可视化处理
"""
plt.scatter(datasets_X, datasets_Y, color = 'blue')  # 标签数据散点图
plt.plot(X, lin_reg_2.predict(poly_reg.fit_transform(X)),color = 'red')  # 绘制回归拟合的出来的线
plt.xlabel('Area')
plt.ylabel('Price')
plt.show()