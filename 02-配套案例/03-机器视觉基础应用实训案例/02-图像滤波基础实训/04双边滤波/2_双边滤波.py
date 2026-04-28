#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    双边滤波器可以很好的保存图像边缘细节并滤除掉低频分量的噪音，
    但是双边滤波器的效率不是太高，花费的时间相较于其他滤波器而言也比较长。
    函数原型：
        bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst
        重点参数解析：
            d：表示在过滤过程中每个像素邻域的直径范围。如果该值是非正数，则将由sigmaSpace计算
            sigmaColor：颜色空间过滤器的sigma值，值越大表示有越宽广的颜色混合到一起
            sigmaSpace: 坐标空间中滤波器的sigma值，如果该值较大，则意味着越远的像素将相互影响
            borderType:边框模式用于图像外部的像素， 默认边缘像素拷贝
"""

import cv2 as cv
import numpy as np

# img_path = './images/Fig4.11(a).jpg'
# img_path = './images/Fig5.08(b).jpg'
# img_path = './images/Fig0519(a)(florida_satellite_original).tif'
img_path = 'noisy2.png'

img = cv.imread(img_path)


def nothing(x):
    pass


cv.namedWindow('image')

# 创建滑动条
cv.createTrackbar('d', 'image', 0, 100, nothing)
cv.createTrackbar('sigmaColor', 'image', 0, 200, nothing)
cv.createTrackbar('sigmaSpace', 'image', 0, 200, nothing)

cv.imshow('img', img)
cv.imshow('image', img)

while True:
    k = cv.waitKey(25) & 0XFF
    if chr(k) == 'q':
        break
    if chr(k) == 'k':
        d = cv.getTrackbarPos('d', 'image')
        sigmaColor = cv.getTrackbarPos('sigmaColor', 'image')
        sigmaSpace = cv.getTrackbarPos('sigmaSpace', 'image')
        b_filter = cv.bilateralFilter(img, d, sigmaColor, sigmaSpace)
        ret, thresh = cv.threshold(b_filter, 127, 255, cv.THRESH_BINARY)
        sava_name = ''.join(('outputs/', 'b_filter', str(d), '_', str(sigmaColor), '_', str(sigmaColor)))
        cv.imshow('image', np.hstack((b_filter, thresh)))
        cv.imwrite(sava_name + '.jpg', b_filter)
        cv.imwrite(sava_name + '_thr.jpg', thresh)

cv.destroyAllWindows()
