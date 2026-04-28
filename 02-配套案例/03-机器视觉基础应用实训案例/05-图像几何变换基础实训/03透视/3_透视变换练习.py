#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
透视变换
    对于透视变换 ，我们需要一个 3x3 变换矩 。
    在变换前后直线 是直线。
    构建 个变换矩  你需要在输入图像上找 4 个点， 以及他们在输出图 像上对应的位置。
    四个点中的任意三个都不能共线。这个变换矩阵可以用函数 cv.getPerspectiveTransform() 构建。
    然后把这个矩阵传给函数 cv.warpPerspective
        more help(cv.getPerspectiveTransform)
"""
import cv2 as cv
import numpy as np

img = cv.imread('./plate1.jpg')
h, w, c = img.shape
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

pts1 = np.float32([[54, 109], [70, 204], [454, 320], [460, 219]])
pts2 = np.float32([[0, 0], [0, h], [w, h], [w, 0]])

M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(img, M, (w, h))

# 在原图中标记这些顶点
cv.circle(img, (int(pts1[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[3][0]),int(pts1[3][1])), 1, (0, 0, 255), cv.LINE_AA)

# 在目标图中标记顶点
cv.circle(dst, (int(pts2[0][0]),int(pts2[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[1][0]),int(pts2[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[2][0]),int(pts2[2][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[3][0]),int(pts2[3][1])), 1, (0, 0, 255), cv.LINE_AA)

print(dst.shape)
cv.imshow('img', np.hstack((img, dst, pp)))
cv.waitKey(0)
cv.destroyAllWindows()
