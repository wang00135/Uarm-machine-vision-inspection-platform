#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
中值模糊，故名思意就是运用卷积框对应像素的中值代替中心像素点的值，
    中值滤波器常常用来处理椒盐噪声，注意它的卷积核必须为正奇数。
    其函数原型为：
        medianBlur(src, ksize[, dst]) -> dst

"""

import cv2 as cv

img = cv.imread('./mouse.jpg')

# 中值滤波
blur = cv.medianBlur(img, 5)

cv.imshow('img', img)
cv.imshow('blur', blur)

cv.waitKey(0)
cv.destroyAllWindows()

# 提高理解
small = img[10:20, 20:30:, :1]
print(small.reshape(10, 10))
print('*' * 60)
small_b = cv.medianBlur(small, 3)
# 边缘填充：复制原图中最临近的行或者列
print(small_b)
