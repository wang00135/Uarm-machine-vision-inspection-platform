#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laplacian(拉普拉斯)算子可以使用二阶导数的形式定义，可假设其离散实现类似于二阶Scharr导数,
事实上OpenCV在算拉普拉斯算子时直接用Sobel算子。
"""
import cv2 as cv

def nothing(x):
    pass

cv.namedWindow('Laplacian')

# 创建滑动条
cv.createTrackbar('ksize', 'Laplacian', 1, 15, nothing)

cap = cv.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if (not ret):
        break
    ksize = cv.getTrackbarPos('ksize', 'Laplacian')
    if (ksize % 2) == 0:
        ksize += 1
    laplacian = cv.Laplacian(gray, cv.CV_64F, ksize = ksize)

    # 计算绝对值，并将结果转换为8位
    # 在输入数组的每个元素上，函数convertScaleAbs。顺序执行三个操作：缩放，取绝对值。值，转换为无符号8位类型
    laplacian = cv.convertScaleAbs(laplacian)

    k = cv.waitKey(24) & 0xFF
    if chr(k) == 'q':
        break
    cv.imshow('Laplacian', laplacian)

cv.destroyAllWindows()
