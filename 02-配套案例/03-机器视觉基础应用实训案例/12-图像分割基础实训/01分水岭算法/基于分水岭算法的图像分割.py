#!/usr/bin env python3
# -*- coding:UTF8 -*-


"""
    OpenCV实现了一个基于掩模的分水岭算法。在这种算法中我们要设置那些山谷点会汇合，那些不会。
    这是一种交互 式的图像分割。我们要做的就是给我们已知的对象打上不同的标签。
    如果某个区域肯定是前景或对象，就使用某个颜色（或灰度值）标签标记它。
    如果某个区域肯定不是对象而是背景就使用另外一个颜色标签标记。
    而剩下的不能确定是前景还是背景的区域就用 0 标记。这就是我们的标签。
    然后实施分水岭算法。 每一次灌水，我们的标签就会被更新，当两个不同颜色的标签相遇时就构建堤坝，
    直到将所有山峰淹没，最后我们得到的边界对象（堤坝）的值为 -1。
"""
import cv2 as cv
import numpy as np

img = cv.imread('img.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imshow('thresh', thresh)

# 去除噪声
kernel = np.ones((5, 5), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=3)

# 膨胀操作，用来确定背景区域
sure_bg = cv.dilate(opening, kernel, iterations=4)
cv.imshow('sure_bg', sure_bg)

# Finding sure foreground area
# 距离变换的基本含义是计算一个图像中非零像素点到最近的零像素点的距离
# 也就是到零像素点的最短距离
# 最常见的距离变换算法就是通过连续的腐蚀操作来实现,
# 腐蚀操作的停止条件是所有前景像素都被完全腐蚀。
# 这样根据腐蚀的先后顺序，我们就得到各个前景像素点到前景中心骨架像素点的距离
# 根据各个像素点的距离值，设置为不同的灰度值。这样就完成了二值图像的距离变换
# cv.distanceTransform(src, distanceType, maskSize)
# 第二个参数 0,1,2 分别表示 CV_DIST_L1, CV_DIST_L2 , CV_DIST_C
dist_transform = cv.distanceTransform(opening, 1, 5)
ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# 查找不知道的区域
sure_fg = np.uint8(sure_fg)
cv.imshow('sure_fg', sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)#图像相减
cv.imshow('unknown', unknown)


# Marker labelling创建标签
# 把将背景标为0 其他对象从1开始正整数标记
ret, markers1 = cv.connectedComponents(sure_fg)
markers = markers1 + 1
# 不能确定的区域标记为0
markers[unknown == 255] = 0

# 到最后一步 实施分水岭算法了。标签图像将会修改  边界区域的标签将变为-1
markers3 = cv.watershed(img, markers)
img[markers3 == -1] = [0, 0, 255]

cv.imshow('watershed', img)

cv.waitKey(0)
cv.destroyAllWindows()
