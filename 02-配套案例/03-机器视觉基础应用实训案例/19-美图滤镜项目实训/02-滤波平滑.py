'''
    滤波平滑
'''
import cv2
import matplotlib.pyplot as plt

# '1. 初始操作'读取原始图像
img = cv2.imread('Resources/GaussianBlur.png')
cv2.imshow("img",img)
cv2.waitKey()

# '2. 均值滤波'  （5, 5）模糊核大小，表示5X5的全一矩阵
blur = cv2.blur(img, (5, 5))
# 显示滤波结果
cv2.imshow("blur ", blur)
cv2.waitKey(0)

'''
中值滤波
'''
# '1. 初始操作'
img = cv2.imread('Resources/medianBlur.png')
cv2.imshow("img ", img)
cv2.waitKey(0)

# '2. 中值滤波'
mblur = cv2.medianBlur(img, 5)
# 均值对比
blur = cv2.blur(img, (5, 5))
# 显示均值滤波
cv2.imshow("Mean Filter ", blur)
cv2.waitKey(0)

# 显示中值滤波
cv2.imshow("Middle Filter ", mblur)
cv2.waitKey(0)

# 高斯滤波

# '1. 初始操作'
img = cv2.imread('Resources/GaussianBlur.png')
cv2.imshow("img ", img)
cv2.waitKey(0)

# '2. 高斯滤波'
g_blur = cv2.GaussianBlur(img, (3, 3), 3)
# 结果显示
cv2.imshow("Gaussian Filter ", g_blur)
cv2.waitKey(0)


# 双边滤波

# '1. 初始操作'
img_path = 'Resources/bilater.png'
img = cv2.imread(img_path)

# '2. 双边滤波'
b_filter = cv2.bilateralFilter(img, 20, 80, 100)

# '3. 完成显示'
plt.title("Bilateral Filter")
cv2.imshow("Bilateral Filter ", b_filter)
cv2.waitKey(0)
