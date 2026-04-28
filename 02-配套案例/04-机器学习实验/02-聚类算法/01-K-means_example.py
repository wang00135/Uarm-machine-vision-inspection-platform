#!/usr/bin/env python3

import numpy as np

# 使用sklearn.cluster.KMeans可以调用K-means算法进行聚类
from sklearn.cluster import KMeans
 
"""
    从指定文件路径中加载城镇居民家庭全年消费水平
    返回值：返回城市名称，以及该城市的各项消费信息
"""
def loadData(filePath):
    fr = open(filePath,'r+')
    lines = fr.readlines()
    retData = []
    retCityName = []
    for line in lines:
        items = line.strip().split(",")
        retCityName.append(items[0])
        retData.append([float(items[i]) for i in range(1,len(items))])
    #  retCityName：用来存储城市名称 retData：用来存储城市的各项消费信息 
    return retData,retCityName
 
     
if __name__ == '__main__':
    data,cityName = loadData('city.txt')  # 加载数据集
    km = KMeans(n_clusters=4)  # 创建K-means实例，n_clusters 用于指定聚类中心的个数 
    label = km.fit_predict(data)  #计算簇中心以及为簇分配序号
    expenses = np.sum(km.cluster_centers_,axis=1) # 聚类中心点的数值加和，也就是平均消费水平

    print(expenses)
    CityCluster = [[],[],[],[]]  # 四档消费水平
    for i in range(len(cityName)):
        CityCluster[label[i]].append(cityName[i])  # 将城市按label分成设定的簇
    for i in range(len(CityCluster)):  # 将每个簇的城市输出 将每个簇的平均花费输出
        print("Expenses:%.2f" % expenses[i])
        print(CityCluster[i])