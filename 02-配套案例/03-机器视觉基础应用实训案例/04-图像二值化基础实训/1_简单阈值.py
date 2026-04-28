#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    使用函数cv2.threshold()进行简单的阈值处理
    函数原型为：threshold(src, thresh, maxval, type[, dst]) -> retval, dst
        返回值
            retval：当前用来对像素值进行分类的低阈值,默认情况下和参数thresh相等
            dst：二值化处理后的图像,像素值中只存在0或255
        参数解析：
                src:需要二值化的原图像，必须是灰度图,传入一种彩色图没有意义；
                thresh：用来对像素值进行分类的阈值；
                maxval：就是当像素值高于，有时是小于阈值时应该被赋予的新的像素值；

                type：阈值处理方式，OpenCV提供多种阈值处理方法
                        cv2.THRESH_BINARY：超过阈值部分取maxval（最大值），否则取0
                        cv2.THRESH_BINARY_INV ：THRESH_BINARY的反转
                        cv2.THRESH_TRUNC ：大于阈值部分设为阈值，否则不变
                        cv2.THRESH_TOZERO ：大于阈值部分不改变，否则设为0
                        cv2.THRESH_TOZERO_INV ：THRESH_TOZERO的反转

"""

import cv2 as cv
import numpy as np

# 读入灰度图
img = cv.imread('./test.png', 0)
# 查看二值化 阈值处理方法
THRESH_TYPES = [i for i in dir(cv) if 'THRESH_' in i]
print(THRESH_TYPES)
print('*' * 60)
"""
    ['ADAPTIVE_THRESH_GAUSSIAN_C',
     'ADAPTIVE_THRESH_MEAN_C',
     'THRESH_BINARY',
     'THRESH_BINARY_INV',
     'THRESH_MASK',
     'THRESH_OTSU',
     'THRESH_TOZERO',
     'THRESH_TOZERO_INV',
     'THRESH_TRIANGLE',
     'THRESH_TRUNC']
"""

# 使用cv2.THRESH_BINARY方法来二值化
ret, thresh_binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

# cv2.THRESH_BINARY_INV
ret, thresh_binary_inv = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)

# cv2.THRESH_TRUNC
ret, thresh_trunc = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)

# cv2.THRESH_TOZERO
ret, thresh_tozero = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)

# cv2.THRESH_TOZERO_INV
ret, thresh_tozero_inv = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)

hstack1 = np.hstack((img, thresh_binary, thresh_binary_inv))
hstack2 = np.hstack((thresh_trunc, thresh_tozero, thresh_tozero_inv))
img_show = np.vstack((hstack1, hstack2))
cv.imshow('test', img_show)
cv.waitKey(0)
cv.destroyAllWindows()

# 理解提高
small = np.array(range(0, 256), np.uint8).reshape(16, 16)
print(small)
print('*' * 60)
cv.imshow('small', small)
ret, small_thresh = cv.threshold(small, 127, 200, cv.THRESH_TOZERO_INV)
cv.imshow('small_thr', small_thresh)
print(ret)
print('*' * 60)
print(small_thresh)
cv.waitKey(0)
