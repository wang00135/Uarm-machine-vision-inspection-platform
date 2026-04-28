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
import numpy as np

# img_path = './images/Fig4.11(a).jpg'
# img_path = './images/Fig5.08(a).jpg'
# img_path = './images/Fig5.08(b).jpg'

# img_path = './images/fig_nasa.tif'
# img_path = './images/Fig5.26a.jpg'

img_path = './images/noisy2.png'

img = cv.imread(img_path, 0)

# 中值滤波
g_blur_3 = cv.GaussianBlur(img, (3, 3), 3, 3)
g_blur_5 = cv.GaussianBlur(img, (5, 5), 3, 3)
g_blur_9 = cv.GaussianBlur(img, (9, 9), 3, 3)
g_blur_15 = cv.GaussianBlur(img, (15, 15), 3, 3)
g_blur_35 = cv.GaussianBlur(img, (35, 35), 3, 3)

_, g_blur_src_thr = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
_, g_blur_3_thr = cv.threshold(g_blur_3, 127, 255, cv.THRESH_BINARY)
_, g_blur_5_thr = cv.threshold(g_blur_5, 127, 255, cv.THRESH_BINARY)
_, g_blur_9_thr = cv.threshold(g_blur_9, 127, 255, cv.THRESH_BINARY)
_, g_blur_15_thr = cv.threshold(g_blur_15, 127, 255, cv.THRESH_BINARY)
_, g_blur_35_thr = cv.threshold(g_blur_35, 127, 255, cv.THRESH_BINARY)

cv.imwrite('./outputs/g_blur_src.jpg', img)
cv.imwrite('./outputs/g_blur_3.jpg', g_blur_3)
cv.imwrite('./outputs/g_blur_5.jpg', g_blur_5)
cv.imwrite('./outputs/g_blur_9.jpg', g_blur_9)
cv.imwrite('./outputs/g_blur_15.jpg', g_blur_15)
cv.imwrite('./outputs/g_blur_35.jpg', g_blur_35)

cv.imwrite('./outputs/g_blur_src_thr.jpg', g_blur_src_thr)
cv.imwrite('./outputs/g_blur_3_thr.jpg', g_blur_3_thr)
cv.imwrite('./outputs/g_blur_5_thr.jpg', g_blur_5_thr)
cv.imwrite('./outputs/g_blur_9_thr.jpg', g_blur_9_thr)
cv.imwrite('./outputs/g_blur_15_thr.jpg', g_blur_15_thr)
cv.imwrite('./outputs/g_blur_35_thr.jpg', g_blur_35_thr)

h1 = np.hstack((img, g_blur_3, g_blur_5))
h2 = np.hstack((g_blur_9, g_blur_15, g_blur_35))
cv.imshow('g_blur_test', np.vstack((h1, h2)))

cv.waitKey(0)
cv.destroyAllWindows()
