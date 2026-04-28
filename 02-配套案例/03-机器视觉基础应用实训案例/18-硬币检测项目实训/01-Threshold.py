#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    使用函数cv2.threshold()进行简单的阈值处理
    函数原型为：threshold(src, thresh, maxval, type[, dst]) -> retval, dst
        返回值
            retval：当前用来对像素值进行分类的低阈值,默认情况下和参数thresh相等
            dst：二值化处理后的图像,像素值中只存在0或255
        参数解析：
                src:需要二值化的原图像，必须是灰度图,传入一种彩色图没有意义；
                thresh：用来对像素值进行分类的阈值；
                maxval：就是当像素值高于，有时是小于阈值时应该被赋予的新的像素值；
                type：阈值处理方式，OpenCV提供多种阈值处理方法
                        cv2.THRESH_BINARY：超过阈值部分取maxval（最大值），否则取0
                        cv2.THRESH_BINARY_INV ：THRESH_BINARY的反转
                        cv2.THRESH_TRUNC ：大于阈值部分设为阈值，否则不变
                        cv2.THRESH_TOZERO ：大于阈值部分不改变，否则设为0
                        cv2.THRESH_TOZERO_INV ：THRESH_TOZERO的反转
"""

import cv2

'1. 初始操作'
src = cv2.imread("Resources/threshold.png", 17)
# src = cv2.imread("Resources/otsu_src.jpg", 17)
img = src.copy()

'2. 灰度化——cvtColor()参数含义：1）原图  2）目标颜色空间,例如 RGB->HSV'
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)

'3. 阈值分割（二值化）——threshold()参数含义：1）8位图像（灰度图）  2）比较阈值  3）输出值   4）分割属性'
'返回值函数： ret=比较阈值   thresh=二值化图像（矩阵数组）'
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
print(ret)

'4. 完成显示'
cv2.imshow("src Image", src)
cv2.imshow("thresh Image", thresh)
cv2.waitKey()
