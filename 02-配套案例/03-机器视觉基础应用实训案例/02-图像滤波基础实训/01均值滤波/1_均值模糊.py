#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
低通滤波有模糊图像，消除噪声的作用
    学习CV中的平均模糊函数cv2.blur() ,cv2.boxFilter()
    blur(src, ksize[, dst[, anchor[, borderType]]]) -> dst
    返回值：
        dst：平均模糊后的图像
    参数解析：
        ksize:模糊核大小 （3，3）表示3X3的全一矩阵
            需要传入一个元组，核大小必须是不能是负数，可以为正奇数偶数如（3，4）
        anchor:锚点;默认值Point（-1，-1）表示锚位于内核中央
        borderType:边框模式用于图像外部的像素

    boxFilter(src, ddepth, ksize[, dst[, anchor[, normalize[, borderType]]]]) -> dst
    返回值：
        dst：平均模糊后的图像
    参数解析：
        ksize:模糊核大小 （3，3）表示3X3的全一矩阵
            需要传入一个元组，核大小必须是不能是负数，可以为正奇数偶数如（3，4）
        ddepth：指定输出图像深度，-1表示与src深度保持一致
        anchor:锚点;默认值Point（-1，-1）表示锚位于内核中央
        normalize：normalize flag，指定内核是否按其区域进行规范化
        borderType:边框模式用于图像外部的像素, 默认边缘像素拷贝
"""

"""
    平均模糊示例
    [80, 73, 69]           [1, 1, 1]
    [77, 83, 74]   * 1/9 * [1, 1, 1] ---->>经过归一化矩阵操作之后83变成了76
    [74, 79, 74]           [1, 1, 1]
"""

import cv2 as cv
import numpy as np

img = cv.imread('./test1.png', 0)
# 平均模糊
blur = cv.blur(img, (5, 5))
# 使用cv.boxFilter()可以达到相同的效果
blur_b = cv.boxFilter(img, -1, (9, 9))
# 可视化
cv.imshow('img', np.hstack((img, blur, blur_b)))
ret, thr1 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
ret1, thr2 = cv.threshold(blur_b, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
cv.imshow('thr', np.hstack((thr1, thr2)))
cv.waitKey(0)
cv.destroyAllWindows()

# 加深理解
small = img[10:20, 20:30, 0:1]
print(small.reshape(10, -1))
print('*' * 60)

blur_small_default = cv.blur(small, (3, 3))
print(blur_small_default)
print('*' * 60)
blur_small_change = cv.blur(small, (3, 3), borderType = cv.BORDER_CONSTANT)
print(blur_small_change)

"""
    BORDER_CONSTANT: 使用borderValue值填充边界
    BORDER_REPLICATE: 复制原图中最临近的行或者列
"""
