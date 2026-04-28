#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

# 形态学梯度 == 膨胀减腐蚀
kernel = np.ones((3, 3), np.uint8)

eg = np.array(range(0, 25), np.uint8).reshape(5, 5)
print('原矩阵')
print(eg)
print('*' * 60)

open_rect = cv.morphologyEx(eg, cv.MORPH_GRADIENT, kernel)
print('形态学梯度结果')
print(open_rect)
print('*' * 60)

erode = cv.erode(eg, kernel)
print('腐蚀结果')
print(erode)
print('*' * 60)
dilate = cv.dilate(eg, kernel)
print('膨胀结果')
print(dilate)
print('*' * 60)

print('膨胀减腐蚀结果')
print(dilate - erode)
