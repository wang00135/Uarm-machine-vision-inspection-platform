#!/usr/bin/env python3
# coding=utf8

import cv2 as cv
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# 设定绿色阈值
lower_green = np.array([41, 120, 100])
upper_green = np.array([77, 255, 255])

# 设定红色阈值 红色有两种阈值，H[0:10] or H[156, 180]
lower_red = np.array([0, 120, 100])
upper_red = np.array([10, 255, 255])

# 设定黄色阈值
lower_yellow = np.array([16, 60, 60])
upper_yellow = np.array([40, 255, 255])

# 设定橙色阈值
lower_orange = np.array([11, 120, 100])
upper_orange = np.array([25, 255, 255])

# 设定青色阈值
lower_cyan = np.array([78, 120, 100])
upper_cyan = np.array([99, 255, 255])

# 设定蓝色阈值
lower_blue = np.array([100, 120, 100])
upper_blue = np.array([124, 255, 255])

# 设定紫色阈值
lower_purple = np.array([125, 120, 100])
upper_purple = np.array([155, 255, 255])

# 设定黑色阈值
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 45])


def calculating_angle(p1, p2, p0):
    # 从三个坐标点中计算角度
    # p0 是交点
    x1 = p1[0] - p0[0]
    y1 = p1[1] - p0[1]
    x2 = p2[0] - p0[0]
    y2 = p2[1] - p0[1]
    """
    记各顶点坐标A（x1，y1）、B（x2，y2）、C（x3，y3），以求∠A为例：
	向量AB=（x2-x1，y2-y1），|AB|=c=√[(x2-x1)²+(y2-y1)²]
	向量AC=（x3-x1，y3-y1），|AC|=b=√[(x3-x1)²+(y3-y1)²]
	AB · AC=(x2-x1)(x3-x1)+(y2-y1)(y3-y1)
	cosA = (AB · AC)/(|AB||AC|) =[(x2-x1)(x3-x1)+(y2-y1)(y3-y1)]/√[(x2-x1)²+(y2-y1)²][(x3-x1)²+(y3-y1)²]
    """
    angle = (x1*x2 + y1*y2)/math.sqrt((x1**2  + y1**2)*(x2**2 + y2**2))
    return int(math.acos(angle) * 180/math.pi)


def calculating_distance(p0, p1):
    # 从已知道的两个点计算两点之间距离
    x1 = p1[0] - p0[0]
    y1 = p1[1] - p0[1]
    dis = int(math.sqrt(x1**2 + y1**2))
    return dis


def getShape(cnt):
    area = cv.contourArea(cnt)
    # 计算弧长
    arcLength = cv.arcLength(cnt, True)
    # 以指定的精度近似多边形曲线
    approxCurve = cv.approxPolyDP(cnt, 0.03 * arcLength, True)
    count = len(approxCurve)
    print("count", count)

    # 三角形判断
    if count == 3:

        # 三个顶点，返回结果是[[507 408]]
        a = approxCurve[0][0]
        b = approxCurve[1][0]
        c = approxCurve[2][0]

        # 三个顶点对应的角度 （单位：度）
        angle_a = calculating_angle(b, c, a)
        angle_b = calculating_angle(a, c, b)
        angle_c = calculating_angle(a, b, c)

        # 最大角
        angle_max = max(angle_a, angle_b, angle_c)
        # 若cosA>0 或 tanA>0（A为最大角），则为锐角三角形，84-96
        # python的cos函数是以弧度作为参数
        if math.cos(math.radians(angle_max)) > 0.05:
            return "锐角三角形"
        elif math.cos(math.radians(angle_max)) < -0.05:
            return "钝角三角形"
        else:
            return "直角三角形"
     # 四边形判断
    elif count == 4:
        # 四个顶点
        a = approxCurve[0][0]
        b = approxCurve[1][0]
        c = approxCurve[2][0]
        d = approxCurve[3][0]

        # 四个顶点对应的角度 （单位：度）
        angle_a = calculating_angle(b, d, a)
        angle_b = calculating_angle(a, c, b)
        angle_c = calculating_angle(b, d, c)
        angle_d = calculating_angle(a, c, d)

        # 直线ab边长 （单位：像素）
        ab = calculating_distance(a, b)
        # 直线bc边长 （单位：像素）
        bc = calculating_distance(b, c)

        # 最大角
        angle_max = max(angle_a, angle_b, angle_c, angle_d)
        if (math.cos(math.radians(angle_max)) > 0.07 or math.cos(math.radians(angle_max)) < -0.07) and abs(ab - bc) < 5:
            return "菱形"
        elif abs(ab - bc) < 5:
            return "正方形"
        else:
            return "长方形"
    # 五角星
    elif count == 10:
        return "五角星"
    else:
        # TODO 弧长和面积的比值
        # 筛选出圆形
        # 圆半径
        r = arcLength / (2*math.pi)
        pi = area / (r**2)
        if abs(pi - math.pi) < 1.:
            # 满足圆的条件
            return "圆形"
        else:
            # n边形
            print('shape', str(count) + "边形", '面积', area)
            return None
            # return str(count) + "边形"


def cv2ImgAddText(img, shapes, textColor=(255, 0, 0)):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    font = ImageFont.truetype('zh.ttf', 10)
    # 绘制文本
    for shape in shapes:
        color, name, x, y, w, h = shape
        print(color, name, x, y, w, h)
        if shape[1] is not None:
            draw.text((x,y), color+name, fill=textColor, font=font)
    # 转换回OpenCV格式
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)


def cv2ImgAddRect(img, shapes):
    for shape in shapes:
        color, name, x, y, w, h = shape
        if shape[1] is not None:
            cv.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 1)
    return img


def colorDivision(name, roi_bgr, lowerb, upperb):
    roi_hsv = cv.cvtColor(roi_bgr, cv.COLOR_BGR2HSV)
    mask = cv.inRange(roi_hsv, lowerb, upperb)
    if lowerb is lower_red:
        lower_red_2 = np.array([156, 120, 100])
        upper_red_2 = np.array([180, 255, 255])
        mask_1 = cv.inRange(roi_hsv, lower_red_2, upper_red_2)
        mask = cv.add(mask, mask_1)
    cv.imshow("mask2", mask)
    # 黑白图
    ret, threshed = cv.threshold(mask, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    tx, ty, tw, th = cv.boundingRect(threshed)
    print("区域：", name, tx, ty, tw, th)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # eroded = cv.erode(threshed,kernel)        #腐蚀图像
    # dilated = cv.dilate(threshed,kernel)      #膨胀图像
    # cv.imshow("Eroded Image",eroded)           #显示腐蚀后的图像
    # cv.imshow("Dilated Image",dilated)         #显示膨胀后的图像
    closed1 = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel, iterations=1)  # 闭运算1
    cv.imshow("closed1 Image", closed1)

    # findContours 查找二进制图像中的轮廓
    contours, hierarchy = cv.findContours(closed1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    print("识别个数为：", len(contours))

    for cnt in contours:
        # 得到子图像
        x, y, w, h = cv.boundingRect(cnt)

        # 计算面积
        area = cv.contourArea(cnt)
        width = roi_bgr.shape[1]   # (193, 324, 3)
        height = roi_bgr.shape[0]
        # 过滤点面积比较小的轮廓
        if area < 50 or area > 30000:
            continue
        # 过滤边框（0,0,w,h）
        if x < 10 or y < 10 or (width - 10 <= x <= width) or (height - 10 <= y <= height):
            print("过滤边框", x,y,w,h)
            continue

        shape = getShape(cnt)
        if shape is not None:
            print('shape', shape, '面积', area)
            shape_list.append([name, shape, x, y, w, h])

    cv.imshow('out1', threshed)
    cv.waitKey()

shape_list = []

roi_bgr = cv.imread('Shape1.png',17)
# 视效果而定
# roi_bgr = cv.GaussianBlur(roi_bgr, (3, 3), 3)

cv.waitKey()
cv.destroyAllWindows()
# 每次分割一种颜色
roi = cv.cvtColor(roi_bgr, cv.COLOR_BGRA2GRAY)
ret, threshed = cv.threshold(roi, 120, 240, cv.THRESH_BINARY)
cv.imshow('roi_bgr', threshed)
colorDivision("红色", roi_bgr, lower_red, upper_red)
colorDivision("蓝色", roi_bgr, lower_blue, upper_blue)
colorDivision("青色", roi_bgr, lower_cyan, upper_cyan)
colorDivision("黑色", roi_bgr, lower_black, upper_black)
colorDivision("绿色", roi_bgr, lower_green, upper_green)
colorDivision("橙色", roi_bgr, lower_orange, upper_orange)
colorDivision("紫色", roi_bgr, lower_purple, upper_purple)
colorDivision("黄色", roi_bgr, lower_yellow, upper_yellow)

roi_bgr = cv2ImgAddText(roi_bgr, shape_list)
roi_bgr = cv2ImgAddRect(roi_bgr, shape_list)

cv.imwrite('result.png',roi_bgr)
cv.imshow('roi_bgr', roi_bgr)
cv.waitKey()
cv.destroyAllWindows()




