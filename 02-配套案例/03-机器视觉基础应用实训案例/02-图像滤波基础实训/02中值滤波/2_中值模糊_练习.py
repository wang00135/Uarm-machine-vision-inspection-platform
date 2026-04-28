#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
中值模糊，故名思意就是运用卷积框对应像素的中值代替中心像素点的值，
    中值滤波器常常用来处理椒盐噪声，注意它的卷积核必须为正奇数。
    其函数原型为：
        medianBlur(src, ksize[, dst]) -> dst

"""

import cv2 as cv
import numpy as np

# img_path = './images/Fig4.11(a).jpg'
# img_path = './images/Fig5.08(a).jpg'
img_path = './images/Fig5.08(b).jpg'

img = cv.imread(img_path)

# 中值滤波
blur_3 = cv.medianBlur(img, 3)
blur_5 = cv.medianBlur(img, 5)
blur_9 = cv.medianBlur(img, 9)
blur_15 = cv.medianBlur(img, 15)
blur_35 = cv.medianBlur(img, 35)

cv.imwrite('./outputs/blur_src.jpg', img)
cv.imwrite('./outputs/blur_3.jpg', blur_3)
cv.imwrite('./outputs/blur_5.jpg', blur_5)
cv.imwrite('./outputs/blur_9.jpg', blur_9)
cv.imwrite('./outputs/blur_15.jpg', blur_15)
cv.imwrite('./outputs/blur_35.jpg', blur_35)

h1 = np.hstack((img, blur_3, blur_5))
h2 = np.hstack((blur_9, blur_15, blur_35))
cv.imshow('blur_test', np.vstack((h1, h2)))

cv.waitKey(0)
cv.destroyAllWindows()

# 提高理解
small = img[10:20, 20:30:, :1]
print(small.reshape(10, 10))
print('*' * 60)
small_b = cv.medianBlur(small, 3)
# 边缘填充：复制原图中最临近的行或者列
print(small_b)
