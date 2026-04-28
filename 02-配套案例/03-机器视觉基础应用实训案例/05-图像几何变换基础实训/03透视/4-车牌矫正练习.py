#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cv2 as cv
import numpy as np


def getXY_min_max(A, B, C, D):
    x_min = min(A[0], C[0])
    y_min = min(A[1], B[1])
    x_max = max(B[0], D[0])
    y_max = max(C[1], D[1])
    return x_min, y_min, x_max, y_max


img_path = './plate.jpg'
img_path = './plate1.jpg'
img = cv.imread(img_path)
h, w = img.shape[:2]

A = (51, 109)
B = (66, 202)
C = (460, 320)
D = (454, 221)

pts1 = np.float32([A, B, C, D])
x_min, y_min, x_max, y_max = getXY_min_max(A, B, C, D)
w = x_max - x_min + 400
h = y_max - y_min - 50
A_ = (0, 0)
B_ = (0, h)
C_ = (w, h)
D_ = (w, 0)
pts2 = np.float32([A_, B_, C_, D_])

M = cv.getPerspectiveTransform(pts1, pts2)
# dst = cv.warpPerspective(img, M, (w, h))
dst = cv.warpPerspective(img, M, (w, h),
                         flags = cv.INTER_CUBIC,
                         borderMode = cv.BORDER_CONSTANT,
                         borderValue = (255, 255, 255))

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

cv.imwrite('./outputs/plate_src.jpg', img)
cv.imwrite('./outputs/plate_dst.jpg', dst)

cv.imshow('img', img)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()
