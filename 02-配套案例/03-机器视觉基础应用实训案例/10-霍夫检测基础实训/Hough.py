import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('test.jpg')  # 读入图片
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # 灰度图像
gray = cv2.GaussianBlur(gray,(9,9),1.5)  # 先进行高斯模糊，防止噪点影响
edges = cv2.Canny(gray,50,150)  # 边缘检测
plt.subplot(121), plt.imshow(edges, 'gray')
plt.xticks([]),plt.yticks([])
# hough transform
lines = cv2.HoughLines(edges, 0.5, np.pi/180, 80)  # 霍夫变换检测直线
# print(lines)

lines1 = lines[:,0,:]  # 提取为为二维
for rho,theta in lines1[:]:   # 将检测到的直线画出来
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a)) 
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)

plt.subplot(122), plt.imshow(img,)
plt.xticks([]), plt.yticks([])
plt.show()
