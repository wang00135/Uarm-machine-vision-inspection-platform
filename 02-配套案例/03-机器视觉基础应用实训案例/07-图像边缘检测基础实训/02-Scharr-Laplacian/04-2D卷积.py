#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用自定义卷积核进行图像2D卷积操作
    cv2.filter2D()
"""
import cv2 as cv
import numpy as np

img = cv.imread('./test.png',0)

# 自己进行垂直边缘提取
kernel = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)

dst = cv.filter2D(img, -1, kernel)

cv.imshow('img', img)
cv.imshow('dst', dst)

cv.waitKey(0)
cv.destroyAllWindows()