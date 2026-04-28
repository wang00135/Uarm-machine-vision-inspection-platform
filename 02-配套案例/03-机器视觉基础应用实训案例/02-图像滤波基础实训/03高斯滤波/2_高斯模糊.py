#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
低通滤波有模糊图像，消除噪声的作用
        高斯滤波的具体操作是：用一个模板（或称卷积、掩模）扫描图像中的每一个像素，
        用模板确定的邻域内像素的加权平均灰度值去替代模板中心像素点的值。 

    使用函数cv2.GaussianBlur()进行高斯模糊
    函数原型：GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]]) -> dst
        返回值
            dst：高斯模糊后的图像
        参数解析：
                ksize: 高斯内核大小
                    ksize.width和ksize.height可以不相同但是这两个值必须为正奇数
                    如果这两个值为0，他们的值将由sigma计算。

                sigmaX: 高斯核函数在X方向上的标准偏差

                sigmaY: 高斯核函数在Y方向上的标准偏差，如果sigmaY是0，
                        会自动将sigmaY的值设置为与sigmaX相同的值，
                        如果sigmaX和sigmaY都是0，这两个值将由ksize.width和ksize.height计算而来
                borderType:边框模式用于图像外部的像素，默认边缘像素拷贝

"""

import cv2 as cv

img = cv.imread('./test.png')


def nothing(x):
    pass


cv.namedWindow('image')
# 创建滑动条
cv.createTrackbar('ksize.width', 'image', 1, 13, nothing)
cv.createTrackbar('ksize.height', 'image', 1, 13, nothing)
cv.createTrackbar('sigmaX', 'image', 0, 10, nothing)
cv.createTrackbar('sigmaY', 'image', 0, 10, nothing)

cv.imshow('img', img)
while True:

    kw = cv.getTrackbarPos('ksize.width', 'image')
    kh = cv.getTrackbarPos('ksize.height', 'image')
    sx = cv.getTrackbarPos('sigmaX', 'image')
    sy = cv.getTrackbarPos('sigmaY', 'image')
    kw = kw if kw % 2 == 1 else kw + 1
    kh = kh if kh % 2 == 1 else kh + 1

    g_blur = cv.GaussianBlur(img, (kw, kh), sx, sy)

    cv.imshow('image', g_blur)

    k = cv.waitKey(25) & 0XFF
    if chr(k) == 'q':
        break

cv.destroyAllWindows()
