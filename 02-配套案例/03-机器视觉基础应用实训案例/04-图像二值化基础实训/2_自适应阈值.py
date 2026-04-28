#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
自适应阈值
adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]) -> dst
    参数解析
        maxValue 最大值
        adaptiveMethod
            cv.ADPTIVE_THRESH_MEAN_C  值取自相邻区域的平均值
            cv.ADPTIVE_THRESH_GAUSSIAN_C  值取值相邻区域的加权和 ，权重为一个高斯窗口
        thresholdType  阈值处理方式
            cv2.THRESH_BINARY：超过阈值部分取maxval（最大值），否则取0
            cv2.THRESH_BINARY_INV ：THRESH_BINARY的反转
            cv2.THRESH_TRUNC ：大于阈值部分设为阈值，否则不变
            cv2.THRESH_TOZERO ：大于阈值部分不改变，否则设为0
            cv2.THRESH_TOZERO_INV ：THRESH_TOZERO的反转
        blockSize
            邻域大小 用来计算自适应阈值的区域大小
        C
            常数C，阈值等于平均值或者加权平均值减去这个常数
"""

import cv2 as cv
import numpy as np

# 读入灰度图
img = cv.imread('./test.png', 0)

ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

h1 = np.hstack((img, th1))
h2 = np.hstack((th2, th3))
# 可视化
cv.imshow('threshold', np.vstack((h1, h2)))

cv.waitKey(0)
cv.destroyAllWindows()

# 理解提高
small = np.array(range(0, 256), np.uint8).reshape(16, 16)
print(small)
print('*' * 60)
small_thresh = cv.adaptiveThreshold(small, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, 1)
print(ret)
print('*' * 60)
print(small_thresh)
