#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

# img_path = 'bkrc.jpg'
img_path = 'shape.png'

img = cv.imread(img_path)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def nothing(x):
    pass


cv.namedWindow('image')
cv.createTrackbar('th', 'image', 127, 255, nothing)
cv.createTrackbar('ks', 'image', 2, 25, nothing)

while True:
    ks = cv.getTrackbarPos('ks', 'image')
    th = cv.getTrackbarPos('th', 'image')
    ret, threash = cv.threshold(gray, th, 255, cv.THRESH_BINARY_INV)
    temp = threash
    kernel = np.ones((ks, ks), np.uint8)
    key = cv.waitKey(100) & 0xFF
    if chr(key) == 'q':
        break
    # 开运算：先腐蚀再膨胀就叫做开运算，用来去噪声。
    opening = cv.morphologyEx(threash, cv.MORPH_OPEN, kernel)
    cv.putText(opening, 'open:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    # 先膨胀再腐蚀，它经常用来填充前景物体中的小洞 或者前景物体上的小黑点。
    close = cv.morphologyEx(threash, cv.MORPH_CLOSE, kernel)
    cv.putText(close, 'close:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    # 形态学梯度
    # 其实就是一幅图像膨胀与腐的差别。
    # 结果看上去就像前景物体的轮廓。
    gradient = cv.morphologyEx(threash, cv.MORPH_GRADIENT, kernel)
    cv.putText(gradient, 'grad:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    # 礼帽
    # 原始图像与开运算之后得到的图像的差。
    tophat = cv.morphologyEx(threash, cv.MORPH_TOPHAT, kernel)
    cv.putText(tophat, 'tophat:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    # 黑帽  进行闭运算之后得到的图像与原始图像的差
    blackhat = cv.morphologyEx(threash, cv.MORPH_BLACKHAT, kernel)
    cv.putText(blackhat, 'bkhat:' + str(ks), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    cv.putText(threash, 'th:' + str(th), (80, 20), cv.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2)

    h1 = np.hstack((threash, opening, close))
    h2 = np.hstack((gradient, tophat, blackhat))
    v = np.vstack((h1, h2))

    cv.imshow('image', v)

cv.destroyWindow('image')
