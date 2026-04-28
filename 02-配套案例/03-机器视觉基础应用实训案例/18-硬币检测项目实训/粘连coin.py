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
src = cv2.imread("Resources/coin1.png")
img = src.copy()

'2. 图像预处理——灰度化'
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'3. 图像预处理——二值化'
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

'4.图像预处理——形态学变换（消除特有噪声）'
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

'5.寻找前景区域——分离粘连物体'
dist_transform = cv2.distanceTransform(open, cv2.DIST_L2, 3)

'6.查找未知区域'
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

'7.找到硬币的中心点（轮廓查找）'
contours, hierarchy = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

'8.绘制硬币中心（轮廓绘制）'
cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

'9.完成显示'
cv2.putText(img, 'count:{}'.format(len(contours)), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
ImgStack = stackImages(0.8, ([src,gray,thresh],[open,sure_fg, img]))

cv2.imshow("Result Image", ImgStack)
cv2.waitKey(0)

