# 图像增强实现

# 亮度增强————直方图均衡化
import cv2
import matplotlib.pyplot as plt

# 1.读取图片并显示
src = cv2.imread("Resources/his.jpg",17)
b, g, r = cv2.split(src)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()


# 实现对比度增强
# 2.灰度化
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 3.直方图均衡化（对比度增强）
dst = cv2.equalizeHist(gray)

# 4.完成显示
plt.title("Histogram Equalization")
plt.imshow(dst, cmap='gray')
plt.show()