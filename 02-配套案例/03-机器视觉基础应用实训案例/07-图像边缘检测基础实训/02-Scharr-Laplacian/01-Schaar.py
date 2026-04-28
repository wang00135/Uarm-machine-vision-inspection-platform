#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scharr算子是高斯平滑与微分操作的结合体，所以它具有很好的抗噪声能力。
"""
import cv2 as cv
import numpy as np

'''
添加椒盐噪声
prob:噪声比例
'''
def sp_noise(image,prob):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

img = cv.imread('./sudoku.jpg', 0)
# img = sp_noise(img, 0.009)


# 参数 1,0 为只在 x 方向求一 导数 最大可以求 2 导数。
Scharrx = cv.Scharr(img, cv.CV_64F, 1, 0)
# 参数 0,1 为只在 y 方向求一 导数 最大可以求 2 导数。
Scharry = cv.Scharr(img, cv.CV_64F, 0, 1)

#求绝对值
Scharrx = cv.convertScaleAbs(Scharrx)
Scharry = cv.convertScaleAbs(Scharry)

Scharr_xy = cv.addWeighted(Scharrx, .5, Scharry, .5,0)
cv.imshow('Scharr x', Scharrx)
cv.imshow('Scharr y', Scharry)
cv.imshow('Scharr_xy', Scharr_xy)
cv.waitKey(0)

cv.destroyAllWindows()
