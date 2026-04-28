#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
扩展缩放

在缩放时推荐使用 cv.INTER_AREA
在扩展时推荐使用 cv.INTER_CUBIC 慢) 和 cv2.INTER_LINEAR
默认情况下所有改变图像尺寸大小的操作使用的插值方法 是 cv.INTER_LINEAR

    resize(src, dsize[, dst[, fx[, fy[, interpolation]]]]) -> dst
    返回值
        dst:缩放操作结果
    参数解析：
        dsize:目标图像缩放大小 （h,w）
        fx：x轴缩放比例
        fy：y轴缩放比例
        interpolation:指定插值方式
            cv.INTER_AREA
            cv.INTER_CUBIC

    使用注意
        长宽都缩小2倍
        rsize = cv.resize(src, None, fx=.5, fy=.5, interpolation=cv.INTER_AREA)

        缩放的指定尺寸
        resize = cv.resize(src, (500, 600), intterpolation=cv.INTER_AREA)

'''

import cv2 as cv

img = cv.imread('./test.png')

# 放大
# 下面的None，本应该是输出图像的尺寸，但是因为后边我们设置了缩放因子
# 因此这里为 None
res = cv.resize(img, None, fx = 2, fy = 2, interpolation = cv.INTER_CUBIC)

# OR
# 我们直接设置输出图像的尺寸 所以不用设置缩放因子
# height, width = img.shape[:2]
# res = cv.resize(img, (2 * width, 2 * height), interpolation=cv.INTER_CUBIC)

# 缩小
height, width = img.shape[:2]
res1 = cv.resize(img, None, fx = .5, fy = .5, interpolation = cv.INTER_AREA)

cv.imshow('zoom', res)
cv.imshow('zoom out', res1)
cv.imshow('src img', img)

cv.waitKey(0)
cv.destroyAllWindows()
