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
            kernel:腐蚀操作的内核。 如果不指定，默认为一个简单的 3x3全一矩阵。
                否则，我们就要明确指定它的形状，可以使用函数getStructuringElement()。
            anchor:默认为-1表示内核中心点，省略时为默认值
            iterations:腐蚀次数。省略时为默认值1
            borderType:推断边缘类型，具体参见borderInterpolate函数。默认值为边缘值拷贝
            borderValue:边缘填充值，具体可参见createMorphoogyFilter函数，可省略,默认为0
    作用：
        腐蚀对于去除白噪声很有用，也可以用来断开两个连接在一一起的物体
 
"""

import cv2 as cv
import numpy as np

img_path = 'j.png'
# img_path = 'bkrc.jpg'

img = cv.imread(img_path, 0)
ret, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

kernel = np.ones((3, 3), np.uint8)

erosion = cv.erode(img, kernel, iterations = 1)
erosion_2 = cv.erode(img, kernel, iterations = 2)

cv.imshow('img', img)
cv.imshow('erode', erosion)

cv.imwrite('./outputs/erosion_iter_1.jpg', erosion)
cv.imwrite('./outputs/erosion_iter_2.jpg', erosion_2)

cv.waitKey(0)
cv.destroyAllWindows()

# 腐蚀理解提高
small = np.ones((5, 5), np.uint8) * 127
small[0, 0] = 0
small[3, 3] = 0
print(small)
print('*' * 60)
small_erosion = cv.erode(small, kernel)
print(small_erosion)

print('*' * 60)
small = np.ones((5, 5), np.uint8) * 127
small[0, 0] = 100
small[3, 3] = 100
print(small)
print('*' * 60)
small_erosion = cv.erode(small, kernel)
print(small_erosion)

# 边缘处理
print('*' * 60)
small = np.ones((5, 5), np.uint8) * 127
small[0, 0] = 100
small[3, 3] = 100
print(small)
print('*' * 60)
small_erosion = cv.erode(small, kernel, borderType = cv.BORDER_CONSTANT, borderValue = 126)
print(small_erosion)
