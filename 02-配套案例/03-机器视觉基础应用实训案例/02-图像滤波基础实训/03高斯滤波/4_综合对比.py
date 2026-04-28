#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
对摄像头的每一帧，分别进行多种滤波操作，放在一起显示，以直观的查看滤波函数的差异性
"""

import cv2 as cv
import numpy as np


def nothing(x):
    pass


# 打开系统默认摄像头
cap = cv.VideoCapture(0)

cv.namedWindow('windows')
cv.createTrackbar('ks', 'windows', 3, 31, nothing)
font = cv.FONT_HERSHEY_SIMPLEX

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx = .5, fy = .5, interpolation = cv.INTER_CUBIC)
    if not ret:
        break
    ks = cv.getTrackbarPos('ks', 'windows')
    # 保证kernel为正奇数
    ks = ks if ks % 2 == 1 else ks + 1

    # 2D 卷积
    kernel = np.ones((ks, ks), np.float32) / (ks * ks)
    filter2D = cv.filter2D(frame, -1, kernel)
    filter2D = cv.putText(filter2D, "filter2D", (20, 20), font, .65, (255, 255, 255), 2)

    # 平均模糊
    blur = cv.blur(frame, (ks, ks))
    blur = cv.putText(blur, "blur", (20, 20), font, .65, (255, 255, 255), 2)

    # 高斯滤波
    g_blur = cv.GaussianBlur(frame, (ks, ks), 0)
    g_blur = cv.putText(g_blur, "g_blur", (20, 20), font, .65, (255, 255, 255), 2)

    # 中值滤波
    medianBlur = cv.medianBlur(frame, ks)
    medianBlur = cv.putText(medianBlur, "medianBlur", (20, 20), font, .65, (255, 255, 255), 2)

    # 双边滤波
    b_filter = cv.bilateralFilter(frame, -1, 2 * ks, int(.7 * ks))
    b_filter = cv.putText(b_filter, "b_filter", (20, 20), font, .65, (255, 255, 255), 2)

    hs1 = np.hstack((frame, filter2D, blur))
    hs2 = np.hstack((g_blur, medianBlur, b_filter))
    vs = np.vstack((hs1, hs2))

    cv.imshow('windows', vs)
    k = cv.waitKey(24) & 0xFF
    if chr(k) == 'q':
        break
