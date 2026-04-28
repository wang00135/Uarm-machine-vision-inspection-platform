#!/usr/bin/env python3
# -*- coding:UTF8 -*-

"""
从视频中获取每一帧图像
将图像转换到 HSV 空间
从滑动条获取H的值
显示指定颜色的物体

"""

import cv2 as cv
import numpy as np

cv.namedWindow('color')


def nothing(x):
    pass


# 创建滑动条
cv.createTrackbar('H_MAX_Value', 'color', 0, 180, nothing)
cv.createTrackbar('H_MIN_Value', 'color', 0, 180, nothing)

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        h_upper = cv.getTrackbarPos('H_MAX_Value', 'color')
        h_down = cv.getTrackbarPos('H_MIN_Value', 'color')
        lower = np.array([h_down, 60, 60])
        upper = np.array([h_upper, 255, 255])
        mask = cv.inRange(hsv, lower, upper)
        res1 = cv.bitwise_and(frame, frame, mask = mask)

        cv.imshow('color', res1)

        k = cv.waitKey(25) & 0xFF
        if chr(k) == 'q':
            break
    else:
        break
cap.release()
cv.destroyWindow('color')
