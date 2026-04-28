#!/usr/bin env python3
# -*- coding:UTF8 -*-


"""
    自定义函数实现灰度直方图计算
"""
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

'''
    安装matplotlib指令：
    pip install matplotlib -i https://pypi.doubanio.com/simple
'''


def calcGrayHist(image):
    # 灰度图像矩阵的高、宽
    rows, cols = image.shape
    # 存储灰度直方图
    grayHist = np.zeros([256], np.uint64)
    for r in range(rows):
        for c in range(cols):
            grayHist[image[r][c]] += 1
    return grayHist


src = cv.imread('test.jpg', cv.IMREAD_GRAYSCALE)

cv.imshow("src", src)
# 计算灰度直方图
gray = calcGrayHist(src)
# 画出灰度直方图
x_range = range(256)
plt.plot(x_range, gray, 'r', linewidth=2, c='black')
# 设置坐标轴的范围
y_maxValue = np.max(gray)
plt.axis([0, 255, 0, y_maxValue])
# 设置坐标轴的标签
plt.xlabel('gray Level')
plt.ylabel('number of pixels')
# 显示灰度直方图
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
