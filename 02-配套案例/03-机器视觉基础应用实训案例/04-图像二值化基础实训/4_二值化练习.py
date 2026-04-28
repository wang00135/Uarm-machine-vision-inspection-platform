import cv2 as cv

# 读入灰度图
gray = cv.imread('./test1.jpg', 0)

# 大津法   全局最佳阈值（双峰图像）
# ret, thr_inv = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
# ret, thr = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
# ret, thr_inv = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
# print(ret)

# 自适应
th2 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 5, 20)
# th3 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 7, 15)

cv.imshow('thresh', th2)
cv.waitKey()
