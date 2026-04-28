#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
透视变换
    对于透视变换，我们需要一个3x3变换矩
    构建这个变换矩需要在输入图像上找4个点，以及它们在输出图像上对应的位置
    注意四个点中的任意三个都不能共线。这个变换矩阵可以用函数 cv.getPerspectiveTransform()构建
    然后把这个矩阵传给函数 getPerspectiveTransform(src, dst[, solveMethod]) -> retval
        返回值：透视变换的3x3矩阵
        参数解析：
            src：原图中四点坐标
            dst：目标图像四点坐标
            solveMethod：传递给cv.solve(DecompTypes) 解决一个或多个线性系统或最小二乘问题
             有以下值可选，DECOMP_LU是默认值
                DECOMP_CHOLESKY = 3
                DECOMP_EIG = 2
                DECOMP_LU = 0
                DECOMP_NORMAL = 16
                DECOMP_QR = 4
                DECOMP_SVD = 1

    透视变换函数原型
    warpPerspective(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst
        参数解析
            M:透视变换的2X4描述矩阵，由函数getPerspectiveTransform得到
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

img = cv.imread('./plate.jpg')
h, w, c = img.shape
print(h, w)

pts1 = np.float32([(88, 92), (218, 118), (84, 125), (211, 160)])
pts2 = np.float32([(88, 118), (218, 118), (88, 160), (218, 160)])

M = cv.getPerspectiveTransform(pts1, pts2)
print(M)
# dst = cv.warpPerspective(img, M, (w, h))
dst = cv.warpPerspective(img, M, (int(w), int(h)),
                         flags = cv.INTER_CUBIC,
                         borderMode = cv.BORDER_CONSTANT,
                         borderValue = (255, 255, 255))

# 在原图中标记这些顶点
cv.circle(img, (int(pts1[0][0]),int(pts1[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[1][0]),int(pts1[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[2][0]),int(pts1[2][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(img, (int(pts1[3][0]),int(pts1[3][1])), 1, (0, 0, 255), cv.LINE_AA)

# 在目标图中标记顶点
cv.circle(dst, (int(pts2[0][0]),int(pts2[0][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[1][0]),int(pts2[1][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[2][0]),int(pts2[2][1])), 1, (0, 0, 255), cv.LINE_AA)
cv.circle(dst, (int(pts2[3][0]),int(pts2[3][1])), 1, (0, 0, 255), cv.LINE_AA)

cv.imwrite('./outputs/plate_src.jpg', img)
cv.imwrite('./outputs/plate_dst.jpg', dst)

cv.imshow('img', img)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()
