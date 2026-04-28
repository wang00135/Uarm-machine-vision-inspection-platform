#修改图片的颜色通道值
import cv2 as cv
import numpy as np

#读取图片
source_img = cv.imread('./test_alpha.png')
#显示原图
cv.imshow('source',source_img)

#利用切片操作使原始图片中蓝色通道的值全部为0
source_img[:,:,0] = 0
cv.imshow('DeletchannelB',source_img)
#再使原始图片中绿色通道的值全部为0
source_img[:,:,1] = 0
cv.imshow('DeletB&G',source_img)

cv.waitKey(0)
