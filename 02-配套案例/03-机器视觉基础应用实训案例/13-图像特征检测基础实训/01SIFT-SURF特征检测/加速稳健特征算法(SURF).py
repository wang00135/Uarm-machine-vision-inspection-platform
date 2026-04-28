#!/usr/bin/env python3
# -*- coding:UTF8 -*-


"""
#首先是得到SURF句柄
surf = cv2.SURF_create()
#使用函数sift.detect()在图像中找关键点
kp = surf.detect(gray, None)
#返回值kp是一个带有很多属性的结构体，这写属性中包含角点坐标（x, y）,有意义的邻域大小，确定其方向的角度。
# OpenCV提供了一个绘制关键点的函数，cv2.drawKeypoints(),它可以在关键点处绘制一个小圆圈。

"""

import cv2 as cv
import numpy as np

def main():
    img = cv.imread('man.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 新建SURF对象
    surf = cv.xfeatures2d.SURF_create()
    print('hessianTHresHold:',surf.getHessianThreshold())
    # 查找关键点
    # kp = surf.detect(gray, None)

    # 查找关键点和计算特征描述符
    kp, des = surf.detectAndCompute(gray, None)
    print(len(kp))

    

    # 关键点太多了
    # 将hessianThreshold值提高以减少关键点
    surf.setHessianThreshold(2000)
    kp, des = surf.detectAndCompute(gray, None)
    print(len(kp))
    # 绘制出关键点    
    img = cv.drawKeypoints(img, kp, None, (0, 255, 0))
    # 计算关键点描述符
    # kp是一个关键点列表，des是一个Numpy数组，其大小是kp的数目乘以128
    kp, des = surf.compute(gray, kp)


    cv.imshow('img', img)
    cv.imwrite('./surfres.jpg',img)
    cv.waitKey(0)
    cv.destroyWindow('img')


if __name__ == '__main__':
    main()