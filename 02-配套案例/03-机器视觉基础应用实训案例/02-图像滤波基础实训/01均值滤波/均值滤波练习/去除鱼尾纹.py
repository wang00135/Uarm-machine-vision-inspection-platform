#!/usr/bin/env python3
# coding=utf8
import cv2 as cv
import numpy as np

img_path = './test2.jpg'

img = cv.imread(img_path)

# 颜色空间通道分离
b, g, r = cv.split(img)

# 对三个通道分别进行不同内核大小的滤波, 过滤掉小尺寸特征
bf = cv.blur(b, (7, 5))
gf = cv.blur(g, (3, 3))
rf = cv.blur(r, (7, 3))

# 通道合并
img_blur = cv.merge((bf, gf, rf))

h1 = np.hstack((img, img_blur))
cv.imwrite('to_crow_feet.jpg', h1)
cv.imshow('mean_filter', h1)
cv.waitKey(0)
cv.destroyAllWindows()
