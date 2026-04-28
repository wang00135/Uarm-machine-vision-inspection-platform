#!/usr/bin env python3
# -*- coding:UTF8 -*-

import cv2 as cv
import numpy as np

roi = cv.imread('hand.png')
hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
roihist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
# 标准化直方图
cv.normalize(roihist, roihist, 0, 255, cv.NORM_MINMAX)

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    hsvt = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    k = cv.waitKey(24) & 0xff
    if chr(k) == 'q':
        break

    if chr(k) == 's':
        cv.imwrite('save_frame.jpg', frame)

    # 反向投影
    dst = cv.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)

    # 闭操作，使显示效果更好
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    dst = cv.morphologyEx(dst, cv.MORPH_CLOSE, disc, iterations=10)

    # 使用merge变成3通道图像
    ret, thresh = cv.threshold(dst, 30, 255, 0)
    thresh = cv.merge((thresh, thresh, thresh))
    res = cv.bitwise_and(frame, thresh)

    # 矩阵按列合并,就是把target,thresh和res三个图片横着拼在一起
    res = np.hstack((frame,res))
    cv.imshow('res', res)
