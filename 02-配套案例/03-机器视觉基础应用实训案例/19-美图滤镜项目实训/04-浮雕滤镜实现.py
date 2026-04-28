#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
浮雕滤镜实现
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# '1. 初始操作'，图片读取与显示
img = cv2.imread('Resources/bilater_out.png')
b, g, r = cv2.split(img)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()

imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# newP = gray0-gray1+150
dst = np.zeros((height, width, 1), np.uint8)

# '2. 灰度值更换'
for i in range(0, height):
    for j in range(0, width - 1):
        grayP0 = int(gray[i, j])
        grayP1 = int(gray[i, j + 1])
        newP = grayP0 - grayP1 + 150
        if newP > 255:
            newP = 255
        if newP < 0:
            newP = 0
        dst[i, j] = newP

# '3. 完成显示'
plt.imshow(dst,cmap='Greys')
plt.show()