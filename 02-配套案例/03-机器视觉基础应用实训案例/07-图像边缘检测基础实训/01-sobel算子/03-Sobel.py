#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核大小(ksize)。如果ksize=-1,表示使用3X3的Scharr滤波器。
建议在处理速度相同的情况下，尽量使用Scharr滤波器。
"""
import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('Sobel x')
cv.namedWindow('Sobel y')

# 创建滑动条
cv.createTrackbar('xsize', 'Sobel x', 1, 15, nothing)
cv.createTrackbar('ysize', 'Sobel y', 1, 15, nothing)


# def sp_noise(image,prob):
#     '''
#     添加椒盐噪声
#     prob:噪声比例
#     '''
#     output = np.zeros(image.shape,np.uint8)
#     thres = 1 - prob
#     for i in range(image.shape[0]):
#         for j in range(image.shape[1]):
#             rdn = np.random.random()
#             if rdn < prob:
#                 output[i][j] = 0
#             elif rdn > thres:
#                 output[i][j] = 255
#             else:
#                 output[i][j] = image[i][j]
#     return output

img = cv.imread('./sudoku.jpg', 0)
# img = sp_noise(img, 0.009)

cv.imshow("src", img)
while True:
    kx = cv.getTrackbarPos('xsize', 'Sobel x')
    ky = cv.getTrackbarPos('ysize', 'Sobel y')
    if (kx % 2) == 0:
        kx += 1
    if (ky % 2) == 0:
        ky += 1
    # 参数 1,0 为只在 x 方向求一 导数 最大可以求 2 导数。
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize = kx)
    # 参数 0,1 为只在 y 方向求一 导数 最大可以求 2 导数。
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize = ky)

    #求绝对值
    sobelx = cv.convertScaleAbs(sobelx)
    sobely = cv.convertScaleAbs(sobely)

    sobel_xy = cv.addWeighted(sobelx, .5, sobely, .5, 1)
    k = cv.waitKey(24) & 0xFF
    if chr(k) == 'q':
        break
    cv.imshow('Sobel x', sobelx)
    cv.imshow('Sobel y', sobely)
    cv.imshow('sobel_xy', sobel_xy)

cv.destroyAllWindows()
