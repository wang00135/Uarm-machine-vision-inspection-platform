#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    项目主题：硬币检测和计数的设计与实现
'''
import cv2
import numpy as np


def stackImages(scale, imgArray):
    """
        将多张图像压入同一个窗口显示
        :param scale:float类型，输出图像显示百分比，控制缩放比例，0.5=图像分辨率缩小一半
        :param imgArray:元组嵌套列表，需要排列的图像矩阵
        :return:输出图像
    """
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                 None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

'1. 初始操作'
src = cv2.imread("Resources/coin2.jpg")
img = src.copy()

'2. 图像预处理——灰度化'
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'3. 图像预处理——二值化'
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

'4. 图像预处理——消除特有噪声（形态学变换）'
# kernel = np.ones((3, 3), np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilate = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel, iterations=2)
opening = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel, iterations=3)

'根据距离变换的性质，经过简单的运算，即可用于细化字符的轮廓和查找物体质心（中心）。'
'5. 寻找前景区域——分离连接物体distanceTranform()参数含义：1）二值图像     2）距离变换类型   3）距离变换的掩膜模板'
# DIST_L2：简单欧几里得距离 Δ = sqrt((x1 - x2)² + (y1 - y2)²)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)

'6. 找到未知区域'
ret, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
print(ret)
sure_fg = np.uint8(sure_fg)

'7. 找到硬币中心（轮廓查找）findContours()参数含义：1）8位图像   2）轮廓查找模式    3）查找近似方法'
contours, hierarchy = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

'8. 绘制硬币中心（轮廓绘制）drawContours()参数含义：1）原图     2）轮廓点坐标   3）轮廓索引    4）线条颜色  5）线条粗细'
cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

'9. 完成显示'
'''
    *知识点回顾：
    putText()参数含义：1）图像  2）需显示的文本  3）坐标  4）文本字体  5）文本尺寸百分比   6）文本颜色   7）文本粗细
'''
cv2.putText(img, "count:{}".format(len(contours)), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
cv2.putText(src, "srcImg", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
cv2.putText(gray, "gray", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
cv2.putText(thresh, "thresh", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
cv2.putText(opening, "open", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
cv2.putText(sure_fg, "fg", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

imgStack = stackImages(0.7, ([src, gray, thresh], [opening, sure_fg, img]))
cv2.imshow("imgStack", imgStack)
cv2.waitKey(0)
