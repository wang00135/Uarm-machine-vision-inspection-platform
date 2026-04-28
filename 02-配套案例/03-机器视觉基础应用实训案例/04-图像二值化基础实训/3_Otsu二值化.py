#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
参考https://www.hindawi.com/journals/mse/2014/794574/fig6/
   cv.THRESH_OTSU 使用大律法OTSU得到的全局自适应阈值
"""

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# 导入matplotlib用于显示直方图,使用命令 pip install matplotlib安装该模块
# matplotlib 是一个非常强大的图像处理库，建议花时间了解


gray = cv.imread('./noisy2.png', 0)
# gray = cv.imread('./test.png', 0)

ret, th1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

ret2, th2 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
print(ret2)

# 原图中存在较为严重噪声,这里降噪处理，关于降噪在图像平滑中讲解
blur = cv.GaussianBlur(gray, (5, 5), 0)

ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
print(ret3)

h1 = np.hstack((gray, th1))
h2 = np.hstack((th2, th3))
cv.imshow('threshold', np.vstack((h1, h2)))

# 计算灰度图的直方图
hist = cv.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(hist, color = 'r')
plt.xlim([0, 256])
plt.title("calcHist")
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
