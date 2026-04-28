#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
 旋转
warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
    返回值：
        旋转操作后的图像
    参数解析：
        M：描述矩阵，使用函数getRotationMatrix2D(center, angle, scale) -> retval
            生成旋转描述矩阵
                参数解析：
                    center:中心点
                    angle:旋转角度（负数顺时针旋转，正数逆时针旋转）
                    scale:缩放因子

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
            边界填充值
'''

import cv2 as cv
import numpy as np

# image_path = './test.png'
image_path = './Fig4.11(a).jpg'

img = cv.imread(image_path)
rows, cols = img.shape[:2]

# 的第一个参数为旋转中心 第二个为旋转角度
#  第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
M = cv.getRotationMatrix2D((cols / 2, rows / 2), -45, .6)

dst = cv.warpAffine(img, M, (cols, rows))

# 镜像填充
dst1 = cv.warpAffine(img, M, (cols, rows),
                     flags = cv.INTER_CUBIC,
                     borderMode = cv.BORDER_DEFAULT)
# 拉伸填充
dst2 = cv.warpAffine(img, M, (cols, rows),
                     flags = cv.INTER_CUBIC,
                     borderMode = cv.BORDER_REPLICATE)
# 溢出填充
dst3 = cv.warpAffine(img, M, (cols, rows),
                     flags = cv.INTER_CUBIC,
                     borderMode = cv.BORDER_WRAP)
# 指定值填充
dst4 = cv.warpAffine(img, M, (cols, rows),
                     flags = cv.INTER_CUBIC,
                     borderMode = cv.BORDER_CONSTANT,
                     borderValue = (255, 255, 255))

cv.imwrite('./outputs/src.jpg', img)
cv.imwrite('./outputs/None.jpg', dst)
cv.imwrite('./outputs/BORDER_DEFAULT.jpg', dst1)
cv.imwrite('./outputs/BORDER_REPLICATE.jpg', dst2)
cv.imwrite('./outputs/BORDER_WRAP.jpg', dst3)
cv.imwrite('./outputs/BORDER_CONSTANT.jpg', dst4)

cv.imshow('img', np.hstack((dst, dst1)))

cv.waitKey(0)
cv.destroyAllWindows()
