#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    开运算：先腐蚀后膨胀, 去除噪声，去除白色小点、空洞
    闭运算：先膨胀后腐蚀, 用来填充前景物体的小黑点
    形态学梯度：膨胀减去腐蚀, 可以得到前景物体的轮廓
    礼帽：原图减去开运算
    黑帽：闭运算减去原图

    使用函数morphologyEx()进行形态学其他操作
    函数原型为：morphologyEx(src, op, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
        op参数：
            cv.MORPH_OPEN：开运算
            cv.MORPH_CLOSE：闭运算
            cv.MORPH_GRADIENT：形态学梯度
            cv.MORPH_TOPHAT：礼帽
            cv.MORPH_BLACKHAT：黑帽
        kernel:内核或结构化内核大小
            使用getStructuringElement(shape, ksize[, anchor]) -> retval获得结构化内核
                shape：
                    cv.MORPH_RECT  矩形结构化核
                    cv.MORPH_ELLIPSE 椭圆结构化核
                    cv.MORPH_CROSS 交叉结构化核
                ksize：
                    指定结构化核大小
                anchor:默认为Point(-1,-1),内核中心点。省略时为默认值
        anchor:默认为Point(-1,-1),内核中心点。省略时为默认值。
        iterations:腐蚀次数。省略时为默认值1。
        borderType:推断边缘类型，具体参见borderInterpolate函数。默认值为BORDER_DEFAULT 边缘值拷贝
        borderValue:边缘值，具体可参见createMorphoogyFilter函数，可省略
"""

'''
结构化元素
# Rectangular Kernel
>>> cv.getStructuringElement(cv.MORPH_RECT,(5,5))
array([[1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1]], dtype=uint8)
# Elliptical Kernel
>>> cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
array([[0, 0, 1, 0, 0],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [0, 0, 1, 0, 0]], dtype=uint8)
# Cross-shaped Kernel
>>> cv.getStructuringElement(cv.MORPH_CROSS,(5,5))
array([[0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0],
       [1, 1, 1, 1, 1],
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0]], dtype=uint8)
'''

import cv2 as cv
import numpy as np

img_path = 'j_open.png'
img = cv.imread(img_path)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def nothing(x):
    pass


cv.namedWindow('OPEN')
# 创建滑动条
cv.createTrackbar('ks', 'OPEN', 2, 25, nothing)

while True:
    ks = cv.getTrackbarPos('ks', 'OPEN')
    if ks <= 1:
        ks += 1
    # Rectangular Kernel
    rectKernel = cv.getStructuringElement(cv.MORPH_RECT, (ks, ks))

    # Elliptical Kernel
    ellKernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (ks, ks))

    # Cross-shaped Kernel
    crossKernel = cv.getStructuringElement(cv.MORPH_CROSS, (ks, ks))

    rect = cv.morphologyEx(gray, cv.MORPH_OPEN, rectKernel)
    ellip = cv.morphologyEx(gray, cv.MORPH_OPEN, ellKernel)
    cross = cv.morphologyEx(gray, cv.MORPH_OPEN, crossKernel)

    cv.putText(rect, 'rect:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)
    cv.putText(ellip, 'ellip:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)
    cv.putText(cross, 'cross:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)
    cv.putText(cross, 'cross:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    h1 = np.hstack((gray, rect))
    h2 = np.hstack((ellip, cross))
    cv.imshow('OPEN', np.vstack((h1, h2)))
    k = cv.waitKey(100) & 0xff
    if chr(k) == 'q':
        break

    if chr(k) == 's':
        cv.imwrite('./outputs/ret_open' + str(ks) + '.jpg', rect)
        cv.imwrite('./outputs/ellip_open' + str(ks) + '.jpg', ellip)
        cv.imwrite('./outputs/cross_open' + str(ks) + '.jpg', cross)
