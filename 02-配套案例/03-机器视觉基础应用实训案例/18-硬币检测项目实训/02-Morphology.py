#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
 腐蚀操作：
    原理：
        比如使用一个3X3的全一矩阵去腐蚀一张灰度图，中心锚点的值就会被替换为对应核中最小的值
        原始数据：
         [[100 127 127 127 127]
         [127 127 127 127 127]
         [127 127 127 127 127]
         [127 127 127 100 127]
         [127 127 127 127 127]]
        ************************************************************
        腐蚀之后的数据
         [[100 100 127 127 127]
         [100 100 127 127 127]
         [127 127 100 100 100]
         [127 127 100 100 100]
         [127 127 100 100 100]]

    erode(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
    参数解析：
        kernel:腐蚀操作的内核。 可以使用函数getStructuringElement()。
        anchor:默认为-1表示内核中心点，省略时为默认值
        iterations:腐蚀次数。省略时为默认值1
        borderType:推断边缘类型，具体参见borderInterpolate函数。默认值为边缘值拷贝
        borderValue:边缘填充值，具体可参见createMorphoogyFilter函数，可省略,默认为0

    dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
    参数解析：
        anchor:默认为Point(-1,-1),内核中心点。省略时为默认值。
        iterations:膨胀次数。省略时为默认值1。
        borderType:推断边缘类型，具体参见borderInterpolate函数。默认为BORDER_DEFAULT, 边缘拷贝
        borderValue:边缘值，具体可参见createMorphoogyFilter函数。可省略。
"""

'''
    腐蚀与膨胀
'''
import cv2

'1. 初始操作'
src = cv2.imread("Resources/bkrc.png", 17)

'2. 获得形态学变换的【结构元】——ELLIPSE=椭圆形  RECT=矩形   CROSS=交叉形'
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

'3. 腐蚀——erode()参数含义：1）原图    2）结构元   iterations=次数'
er = cv2.erode(src, kernel, iterations=1)

'4. 膨胀——dilate()参数含义：1）原图   3）结构元   iterations=次数'
di = cv2.dilate(er, kernel, iterations=1)

'5. 完成显示'
cv2.imshow("src Image", src)
cv2.imshow("erode Image", er)
cv2.imshow("dilate Image", di)
cv2.waitKey(0)

######################################################

'''
    开操作与闭操作
    开操作 = 腐蚀 + 膨胀       消除部分高亮区域（二值化中的白色区域）OPEN
    闭操作 = 膨胀 + 腐蚀       消除高亮区域的内部黑洞（二值化中的黑色区域）CLOSE
    
'''
# import cv2
#
# '1. 初始操作'
# src = cv2.imread("Resources/open.png", 0)
# img = src.copy()
#
# '2. 二值化——threshold'
# ret, thresh = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY)
# cv2.imshow('thresh', thresh)
#
# '3. 获取形态学变换结构元——RECT=矩形'
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#
# '4. 形态学变换函数——morphologyEx()参数含义：1）原图    2）变换属性（开/关操作、礼帽、梯度等）    3）结构元 '
# open = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel, iterations=2)
# # op_erode = cv2.erode(src, kernel, iterations=1)
# # open = cv2.dilate(op_erode, kernel, iterations=1)
#
# '5. 完成显示'
# cv2.imshow("Src Image ", img)
# cv2.imshow("MORPH_OPEN Image", open)
# cv2.waitKey(0)
