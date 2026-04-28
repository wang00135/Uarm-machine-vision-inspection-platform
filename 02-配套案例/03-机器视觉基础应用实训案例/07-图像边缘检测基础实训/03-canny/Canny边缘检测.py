#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用函数cv2.Canny()来进行边缘检测
函数原型：
    Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) -> edges
    参数解析：
        threshold1:下阈值，低于下阈值的边界将被抛弃
        threshold2:上阈值，高于上阈值的将视为真边界，位于上下阈值之间的将被保留
more help use help(cv2.Canny)
"""
import cv2 as cv

img = cv.imread('./wall.jpg',0)

def nothing(x):
    pass

cv.namedWindow('Canny')
cv.createTrackbar('threshold1', 'Canny', 0, 255, nothing)
cv.createTrackbar('threshold2', 'Canny', 0, 255, nothing)

while True:
    threshold1 = cv.getTrackbarPos('threshold1', 'Canny')
    threshold2 = cv.getTrackbarPos('threshold2', 'Canny')
    edges = cv.Canny(img, threshold1, threshold2)
    cv.imshow('Canny', edges)
    k = cv.waitKey(25) & 0xFF
    if chr(k) == 'q':
        break

cv.destroyAllWindows()
