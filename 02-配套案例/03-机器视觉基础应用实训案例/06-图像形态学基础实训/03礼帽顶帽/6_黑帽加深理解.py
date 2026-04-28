#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

# 黑帽 == 闭运算减原图
kernel = np.ones((3, 3), np.uint8)

eg = np.array(range(0, 25), np.uint8).reshape(5, 5)
print('原矩阵')
print(eg)
print('*' * 60)

tophat_rect = cv.morphologyEx(eg, cv.MORPH_BLACKHAT, kernel)
print('黑帽结果')
print(tophat_rect)
print('*' * 60)

dilate = cv.dilate(eg, kernel)
print('膨胀结果')
print(dilate)
print('*' * 60)
erode = cv.erode(dilate, kernel)
print('先膨胀后腐蚀结果==闭运算')
print(erode)
print('*' * 60)

print('闭运算减原图结果')
print(erode - eg)
