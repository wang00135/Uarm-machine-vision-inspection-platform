#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
 膨胀操作：
    原理：使用对应核中最大的像素值取代中心瞄点的像素值
    举例 使用3X3的全一矩阵进行膨胀
    原矩阵
    [[128 127 127 127 127]
     [127 127 127 127 127]
     [127 127 127 127 127]
     [127 127 127 128 127]
     [127 127 127 127 127]]
    ************************************************************
    膨胀后的矩阵
    [[128 128 127 127 127]
     [128 128 127 127 127]
     [127 127 128 128 128]
     [127 127 128 128 128]
     [127 127 128 128 128]]

    dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
        参数解析：
            anchor:默认为Point(-1,-1),内核中心点。省略时为默认值。
            iterations:膨胀次数。省略时为默认值1。
            borderType:推断边缘类型，具体参见borderInterpolate函数。默认为BORDER_DEFAULT, 边缘拷贝
            borderValue:边缘值，具体可参见createMorphoogyFilter函数。可省略。

 
"""

import cv2 as cv
import numpy as np

# img_path = 'test.png'
img_path = 'j.png'

img = cv.imread(img_path, 0)
ret, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

# 您可以将内核看作是一个小矩阵，我们在图像上滑动以进行（卷积）操作，例如模糊，锐化，边缘检测或其他图像处理操作。
# 核中不能有0的元素
kernel = np.ones((3, 3), np.uint8)

dilate = cv.dilate(img, kernel, iterations = 1)
dilate_2 = cv.dilate(img, kernel, iterations = 2)

cv.imwrite('./outputs/dilate.jpg', dilate)
cv.imwrite('./outputs/dilate_2.jpg', dilate_2)

cv.imshow('img', img)
cv.imshow('dilate', dilate)

cv.waitKey(0)
cv.destroyAllWindows()

# 理解提高
small = np.ones((5, 5), np.uint8) * 127
small[0, 0] = 128
small[3, 3] = 128
print(small)
print('*' * 60)
small_dilate = cv.dilate(small, kernel)
print(small_dilate)
