#!/usr/bin env python3
# -*- coding:UTF8 -*-

import cv2 as cv
import numpy as np

roi = cv.imread('rgbCirclemd.png')
hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

target = cv.imread('rgbcircle.png')
# 转换HSV颜色空间
hsvt = cv.cvtColor(target, cv.COLOR_BGR2HSV)

roihist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

# 归一化直方图
# cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)
#
# 反向投影
# dst = cv.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)
# 通过归一化该直方图可以得到一个函数，它给出了一个给定强度的像素属于imgROI区域的概率
cv.normalize(roihist,        # 输入直方图
             roihist,        # 输出直方图（可以原图计算）
             0.0,            # 缩放的最小值
             255.0,          # 缩放的最大值
             cv.NORM_MINMAX  # 缩放类型
             )
# 反向投影的作用是替换输入图像中的每个像素值，使其变成归一化直方图中对应的概率值
dst = cv.calcBackProject([hsvt],
                         [0, 1],            # 通道数量  H 和 S
                         roihist,           # 进行反向投影的直方图
                         [0, 180, 0, 256],  # 生成的反向投影图像
                         1                  # 每个维度的值域
                         )
# 获得核
disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

cv.morphologyEx(dst, cv.MORPH_CLOSE, disc, iterations=50)
ret, thresh = cv.threshold(dst, 20, 255, 0)

thresh = cv.merge((thresh, thresh, thresh))
res = cv.bitwise_and(target, thresh)

res = np.hstack((target, res))
cv.imshow('res', res)
cv.waitKey(0)
cv.destroyAllWindows()
