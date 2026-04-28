#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2平移-2.py:
http://docs.opencv.org/3.2.0/da/d6e/tutorial_py_geometric_transformations.html
    warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
    返回值：
        平移操作后的图像
    参数解析：
        M：描述矩阵，示例M = np.float32([[1, 0, 100], [0, 1, 50]])
            表示在x轴上向左平移100个像素单位，在Y轴上向下平移50个像素单位
        dsize：输出图像的大小（宽，高）
        flags：插值方式有如下插值法可用
            cv.INTER_NEAREST  最邻近插值,将离新像素所在位置最近的像素像素值赋值给新像素
            cv.INTER_LINEAR  双线性插值, x、y方向临近像素取乘以相应权重并相加赋值给i新的像素值
            cv.INTER_CUBIC  双立方插值, 精度更高，计算量最大，取附近十六个点加权取像素值
            cv.INTER_LANCZOS4  附近像素及原像素加权取值
        borderModer:
            BORDER_CONSTANT = 0  以borderValue值填充边界
            BORDER_DEFAULT = 4   镜像填充
            BORDER_REFLECT = 2  镜像填充
            BORDER_REFLECT101 = 4  镜像填充
            BORDER_REPLICATE = 1  拉伸填充
            BORDER_TRANSPARENT = 5  暂时不知道
            BORDER_WRAP = 3  溢出填充
        borderValue：
            填充值
"""

import cv2 as cv
import numpy as np

img = cv.imread('./test.png')
rows, cols = img.shape[:2]
M = np.float32([[1, 0, cols // 2], [0, 1, 0]])
dst = cv.warpAffine(img, M, (cols, rows))
dst1 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4,
                     borderMode = cv.BORDER_CONSTANT, borderValue = (255, 255, 0))
dst2 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4,
                     borderMode = cv.BORDER_DEFAULT)
dst3 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4,
                     borderMode = cv.BORDER_WRAP)

cv.imwrite('./outputs/x100_y50_default.jpg', dst)
cv.imwrite('./outputs/constant.jpg', dst1)
cv.imwrite('./outputs/BORDER_DEFAULT.jpg', dst2)
cv.imwrite('./outputs/BORDER_WRAP.jpg', dst3)

cv.imshow('dst', dst)
cv.imshow('dst1', dst1)
cv.waitKey(0)
cv.destroyAllWindows()
