#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv

def nothing(x):
    pass

cv.namedWindow('Sobel x')
cv.namedWindow('Sobel y')
cv.namedWindow('Sobel_xy')

# 创建滑动条
cv.createTrackbar('xsize', 'Sobel x', 1, 15, nothing)
cv.createTrackbar('ysize', 'Sobel y', 1, 15, nothing)

cap = cv.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    # frame = cv.blur(frame, (5, 5))
    frame = cv.GaussianBlur(frame, (5, 5), -1)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if (not ret):
        break
    kx = cv.getTrackbarPos('xsize', 'Sobel x')
    ky = cv.getTrackbarPos('ysize', 'Sobel y')
    if (kx % 2) == 0:
        kx += 1
    if (ky % 2) == 0:
        ky += 1

    # 参数 1,0 为只在 x 方向求一 导数 最大可以求 2 导数。
    sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize = kx)
    # 参数 0,1 为只在 y 方向求一 导数 最大可以求 2 导数。
    sobely = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize = ky)

    # 计算绝对值，并将结果转换为8位
    # 在输入数组的每个元素上，函数convertScaleAbs。顺序执行三个操作：缩放，取绝对值。值，转换为无符号8位类型
    sobelx = cv.convertScaleAbs(sobelx)
    sobely = cv.convertScaleAbs(sobely)

    sobel_xy = cv.addWeighted(sobelx, .5, sobely, .5, 1)
    k = cv.waitKey(24) & 0xFF
    if chr(k) == 'q':
        break
    cv.imshow('Sobel x', sobelx)
    cv.imshow('Sobel y', sobely)
    ret,img = cv.threshold(sobel_xy,130,255, cv.THRESH_BINARY_INV)
    cv.imshow('Sobel_xy', sobel_xy)

cv.destroyAllWindows()
