#!/usr/bin env python3
# -*- coding:UTF8 -*-

#灰度直方图的计算与显示
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('test.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(img_gray, cmap=plt.cm.gray)

hist = cv2.calcHist([img], [0], None, [256], [0, 256])
print(type(hist))

# 创建一个新的子视图存放灰度图
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)

# 设置参数范围
plt.xlim([0, 256])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
