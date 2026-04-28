#!/usr/bin/env python3
# -*- coding:UTF8 -*-

"""
函数cv2.findContours()是用来在一副二值图像中查找轮廓的，
其函数原型如下：findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy
    重点参数解析：
        mode：轮廓检查模式，有四个可选的值，
            cv2.RETR_EXTERNAL：表示只提取最外面的轮廓；
            cv2.RETR_LIST：表示提取所有轮廓并将其放入列表,不建立参层级结构；
            cv2.RETR_CCOMP:表示提取所有轮廓并将组织成一个两层结构，其中顶层轮廓是外部轮廓，第二层轮廓是“洞”的轮廓；
            cv2.RETR_TREE：表示提取所有轮廓并组织成轮廓嵌套的完整层级结构。
        method：轮廓的近似方法，有四个可选择值
            cv2.CHAIN_APPROX_NONE：获取每个轮廓的每个像素，相邻的两个点的像素位置差不超过1； 
            cv2.CHAIN_APPROX_SIMPLE：压缩水平方向，垂直方向，对角线方向的元素，值保留该方向的重点坐标，
                如果一个矩形轮廓只需4个点来保存轮廓信息；
            cv2.CHAIN_APPROX_TC89_L1和cv2.CHAIN_APPROX_TC89_KCOS使用Teh-Chinl链逼近算法中的一种。

在OpenCV中使用函数cv2.drawContours()来绘制轮廓，该函数可以依据所传入的边界点参数绘制任何形状。
其函数原型如下：
    drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) -> image
    重点参数解析：
        contours：轮廓，它是一个python列表
        contourIdx：轮廓的索引，为-1时表示绘制contours里的所有。

"""

import sys

import cv2 as cv
import numpy as np

if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        file_path = "sample.jpg"
    else:
        file_path = sys.argv[1]

    # 读图像
    src = cv.imread(file_path, 1)
    src = cv.resize(src, None, fx = .5, fy = .5, interpolation = cv.INTER_AREA)

    # 将原图像灰度化
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 平均滤波
    blur = cv.blur(gray, (5, 5))

    # 简单阈值的二值化
    ret, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # 查找轮廓
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, \
                                          cv.CHAIN_APPROX_SIMPLE)[-2:]

    # 创建灰色背景图
    drawing = np.ones((thresh.shape[0], thresh.shape[1], 3), np.uint8) * 127
    cv.imwrite('./outputs/lvs.png', drawing)

    # 绘制所有轮廓
    cv.drawContours(drawing, contours, -1, (0, 255, 0), -1, lineType = cv.LINE_AA)

    # 找最大面积轮廓
    area_max = 0
    _cnt = None
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > area_max:
            area_max = area
            _cnt = cnt

    drawing1 = cv.drawContours(src.copy(), [_cnt], -1, (0, 255, 0), 2, 8)

    cv.imshow("Output", np.vstack((src, drawing, drawing1)))

    cv.imwrite('./outputs/drawing.png', drawing)
    cv.imwrite('./outputs/drawing1.png', drawing1)

    cv.waitKey(0)
    cv.destroyAllWindows()
