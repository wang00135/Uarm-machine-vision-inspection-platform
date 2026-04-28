'''
grabCut算法实现图像分割
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('bear.jpg')
OLD_IMG = img.copy()
mask = np.zeros(img.shape[:2], np.uint8)#创建掩模
SIZE = (1, 65)
bgdModle = np.zeros(SIZE, np.float64)#创建背景模型
fgdModle = np.zeros(SIZE, np.float64)#创建前景模型
rect = (1, 1, img.shape[1], img.shape[0])  #矩形标记区域
cv2.grabCut(img, mask, rect, bgdModle, fgdModle, 10, cv2.GC_INIT_WITH_RECT)#grabcut图像分割

mask2 = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')#寻找mask中的前景像素

img =cv2.bitwise_and(img,img,mask=mask2)#位与提取原图中的前景区域

cv2.imshow('mask2',mask2)
cv2.imshow('img',img)
cv2.imshow('src',OLD_IMG)

cv2.waitKey(0)
