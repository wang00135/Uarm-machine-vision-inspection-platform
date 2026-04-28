#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

# 礼帽 == 原图减开运算
kernel = np.ones((3, 3), np.uint8)

eg = np.array(range(0, 25), np.uint8).reshape(5, 5)
print('原矩阵')
print(eg)
print('*' * 60)

tophat_rect = cv.morphologyEx(eg, cv.MORPH_TOPHAT, kernel)
print('礼帽结果')
print(tophat_rect)
print('*' * 60)

erode = cv.erode(eg, kernel)
print('腐蚀结果')
print(erode)
print('*' * 60)
dilate = cv.dilate(erode, kernel)
print('先腐蚀后膨胀结果==开运算')
print(dilate)

print('原图减开运算结果')
print(eg - dilate)
