#!/usr/bin/env python3
# -*- coding:UTF8 -*-

"""
函数cv2.findContours()是用来在一副二值图像中查找轮廓的，
其函数原型如下：findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy
    重点参数解析：
        mode：轮廓检查模式，有四个可选的值，
            cv::RETR_EXTERNAL：表示只提取最外面的轮廓；
            cv::RETR_LIST：表示提取所有轮廓并将其放入列表；
            cv::RETR_CCOMP:表示提取所有轮廓并将组织成一个两层结构，其中顶层轮廓是外部轮廓，第二层轮廓是“洞”的轮廓；
            cv::RETR_TREE：表示提取所有轮廓并组织成轮廓嵌套的完整层级结构。
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

import cv2 as cv
import numpy as np

if __name__ == "__main__":
    # 生成一张黑色背景的图像
    img = np.zeros((512, 512, 3), np.uint8)

    # 添加一个矩形
    img[100:400, 100:400, :3] = 255

    # 添加一条直线
    img[100:400, 450:451, :3] = 255

    # 显示
    cv.imshow('img', img)
    cv.imwrite('outputs/img_src.png', img)

    # 灰度
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 大津法二值化
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 查找轮廓
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, \
                                          cv.CHAIN_APPROX_SIMPLE)[-2:]

    # 绘制所有轮廓
    # cv.drawContours(img, contours, -1, (0, 255, 0), 2, 8, hierarchy)
    print('cv.CHAIN_APPROX_SIMPLE')
    # print(contours)

    cv.circle(img, tuple(contours[0][0][0]), 1, (0, 0, 255), cv.LINE_AA)
    cv.circle(img, tuple(contours[0][1][0]), 1, (0, 0, 255), cv.LINE_AA)

    cv.circle(img, tuple(contours[1][0][0]), 1, (0, 0, 255), cv.LINE_AA)
    cv.circle(img, tuple(contours[1][1][0]), 1, (0, 0, 255), cv.LINE_AA)
    cv.circle(img, tuple(contours[1][2][0]), 1, (0, 0, 255), cv.LINE_AA)
    cv.circle(img, tuple(contours[1][3][0]), 1, (0, 0, 255), cv.LINE_AA)

    # 查找轮廓
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, \
                                          cv.CHAIN_APPROX_NONE)

    print('cv.CHAIN_APPROX_NONE')
    # print(contours)
    # 绘制所有轮廓
    # cv.drawContours(img, contours, -1, (0, 255, 0), 2, 8, hierarchy)
    # 遍历所有的轮廓点集，将该点像素变成绿色
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            img[contours[i][j][0][1], contours[i][j][0][0]] = (0, 255, 0)

    cv.imshow("Output", img)
    cv.imwrite('outputs/img_dst.png', img)

cv.waitKey(0)
cv.destroyAllWindows()
