#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
在仿射变换中 原图中所有的平行线在结果图像中同样平行。
为了创建 这个矩阵，我们需要从原图像中找到三个点以及他们在输出图像中的位置。
然后传递给函数cv2.getAffineTransform创建一个 2x3 的矩，最后将矩转递给函数cv2.warpAffine
    more help(cv2.getAffineTransform)
"""
import cv2 as cv
import numpy as np

img = cv.imread('drawing.png')
rows, cols, ch = img.shape
print(img.shape)

cv.namedWindow('img')

pp = np.ones(img.shape, dtype = np.uint8) * 127


def draw_xy(event, x, y, flags, param):
    if flags == cv.EVENT_FLAG_LBUTTON:
        h, w = img.shape[:2]
        x_ = x if x <= w else x - w
        s = '(x:' + str(x_) + ', y:' + str(y) + ')'
        pp = np.ones(img.shape, dtype = np.uint8) * 127
        if x < w:
            cv.putText(pp, s, (20, 70), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                       cv.LINE_AA)
        else:
            cv.putText(pp, s, (20, 140), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                       cv.LINE_AA)
        cv.imshow('img', np.hstack((img, dst, pp)))


cv.setMouseCallback('img', draw_xy)

# 原图变换的顶点
pts1 = np.float32([[50, 50], [400, 50], [50, 400]])
# 目标图像变换顶点
pts2 = np.float32([[100, 150], [300, 100], [150, 250]])

# 进行仿射变换
M = cv.getAffineTransform(pts1, pts2)
dst = cv.warpAffine(img, M, (cols, rows))

# 在原图中标记这些顶点
cv.circle(img,(int(pts1[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)

# 在目标图中标记顶点
cv.circle(dst, (int(pts2[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)

cv.imshow('img', np.hstack((img, dst, pp)))
cv.waitKey(0)
cv.destroyAllWindows()
