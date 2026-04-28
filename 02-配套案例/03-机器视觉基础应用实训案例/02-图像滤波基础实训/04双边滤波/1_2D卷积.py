#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
使用自定义卷积核进行图像2D卷积操作
    函数原型：
        filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]]) -> dst
        函数返回值：dst：2d卷积操作后的结果

        函数解析：
            ddepth：指定输出图像深度，-1表示与src深度保持一致
            kernel：卷积内核大小, 需大于零，可以不同，如核大小（4，5）
            anchor:锚点;默认值Point（-1，-1）表示锚位于内核中央
            delta：在将它们存储在dst中之前，将delta可选值添加到已过滤的像素中，默认为None
            borderType:边框模式用于图像外部的像素， 默认边缘像素拷贝
"""

import cv2 as cv
import numpy as np

img = cv.imread('./test.png')

# 自定义的一些卷积核
kernel = np.ones((5, 5), np.float32) / 25

kernel_user_1 = np.array([[0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [1, 1, 1, 1, 1],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0]]) / 9

kernel_user_2 = np.array([[1, 0, 0, 0, 1],
                          [0, 1, 0, 1, 0],
                          [0, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [1, 0, 0, 0, 1]]) / 9

kernel_user_3 = np.array([[0, 0, 0, 0, 0],
                          [0, 1, 1, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0]]) / 9

kernel_user_4 = np.array([[1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 1],
                          [1, 0, 0, 0, 1],
                          [1, 0, 0, 0, 1],
                          [1, 1, 1, 1, 1]]) / 16

dst = cv.filter2D(img, -1, kernel)
dst1 = cv.filter2D(img, -1, kernel_user_1)
dst2 = cv.filter2D(img, -1, kernel_user_2)
dst3 = cv.filter2D(img, -1, kernel_user_3)
dst4 = cv.filter2D(img, -1, kernel_user_4)

h1 = np.hstack((img, dst, dst1))
h2 = np.hstack((dst2, dst3, dst4))
cv.imshow('show', np.vstack((h1, h2)))

cv.waitKey(0)
cv.destroyAllWindows()

# 理解提高
small = np.array(range(10, 55, 5), np.uint8).reshape(3, -1)
print(small)
print('*' * 60)

small_filter = cv.filter2D(small, -1, (np.ones((3, 3), np.float32) / (3 * 3)))
print(small_filter)
