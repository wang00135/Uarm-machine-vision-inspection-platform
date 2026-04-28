#!/usr/bin/env python3
# -*- coding:UTF8 -*-


"""
#首先是得到SIFT句柄
sift = cv.xfeatures2d.SIFT_create()
#使用函数sift.detect()在图像中找关键点
kp = sift.detect(gray, None)
#返回值kp是一个带有很多属性的结构体，这写属性中包含角点坐标（x, y）,有意义的邻域大小，确定其方向的角度。
# OpenCV提供了一个绘制关键点的函数，cv2.drawKeypoints(),它可以在关键点处绘制一个小圆圈。
"""
import cv2 as cv
import numpy as np

def main():
    img = cv.imread('man.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 创建SIFT对象
    sift = cv.SIFT_create()
    # 查找关键点
    kp = sift.detect(gray, None)
    # 绘制出关键点
    img = cv.drawKeypoints(img, kp, None, (0, 255, 0) , 2)

    # 计算关键点描述符
    # kp是一个关键点列表，des是一个Numpy数组，其大小是kp的数目乘以128
    kp, des = sift.compute(gray, kp)

    cv.imshow('img', img)
    cv.imwrite('./res.jpg',img)
    cv.waitKey(0)
    cv.destroyWindow('img')


if __name__ == '__main__':
    main()