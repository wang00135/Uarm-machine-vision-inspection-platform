#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    在仿射变换中 原图中所有的平行线在结果图像中同样平行。
    为了创建这个矩阵，我们需要从原图像中找到三个点以及它们在输出出图像中的位置。
    cv2.getAffineTransform 会创建一个2x3的矩阵，最后这个矩将会传给函数 cv2.warpAffine
        more help(cv2.getAffineTransform)

    warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
    返回值：
        仿射操作后的图像
    参数解析：
        M：描述矩阵，使用函数getAffineTransform(src, dst) -> retval
            生成仿射描述矩阵
                参数解析：
                    src：原图中三个点的坐标
                    dst：目标图像中三个点坐标

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
"""
import cv2 as cv
import numpy as np

img = cv.imread('drawing_dst.jpg')
rows, cols, ch = img.shape
print(img.shape)

# 原图变换的顶点
pts1 = np.float32([[100, 100], [300, 50], [100, 400]])
# 目标图像变换顶点
pts2 = np.float32([[50, 50], [400, 50], [50, 400]])

# 构建仿射变换描述矩阵
M = cv.getAffineTransform(pts1, pts2)
# dst = cv.warpAffine(img, M, (cols, rows))
dst = cv.warpAffine(img, M, (cols, rows),
                    flags = cv.INTER_CUBIC,
                    borderMode = cv.BORDER_CONSTANT,
                    borderValue = (255, 255, 255))

# 在原图中标记这些顶点
cv.circle(img, (int(pts1[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)

# 在目标图中标记顶点
cv.circle(dst, (int(pts2[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)

cv.imshow('dst', dst)
cv.imshow('img', img)

cv.imwrite('./outputs/src.jpg', img)
cv.imwrite('./outputs/dst.jpg', dst)
cv.waitKey(0)
cv.destroyAllWindows()
