'''
    对比度增强——限制对比度的自适应阈值均衡化
'''

import cv2

# '1. 初始操作'
src = cv2.imread("Resources/his_1.png", 17)

# '2. 灰度化'
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 对比：全局直方图均衡化
eqHist = cv2.equalizeHist(gray)

# '3. 创建CLAHE对象'
# 生成自适应均衡化图像方法
# 参数：clipLimit：颜色对比度的阈值，tileGridSize：进行像素均衡化的网格大小，即在多少网格下进行直方图的均衡化操作
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

# '4. 限制对比度的自适应阈值均衡化'
dst = clahe.apply(gray)

# '5. 完成显示'
cv2.imshow("Src Image", src)
cv2.imshow("eh Image", dst)
cv2.imshow("eqHist Image", eqHist)
cv2.waitKey(0)
