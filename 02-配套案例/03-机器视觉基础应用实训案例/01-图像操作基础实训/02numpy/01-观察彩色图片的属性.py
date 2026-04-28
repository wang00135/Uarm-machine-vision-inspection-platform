# 观察彩色图片的属性
import cv2 as cv

#读取图片
img = cv.imread('./test_alpha.png')
cv.imshow('windows', img)
#显示图片像素信息
print("图片img的类型：", type(img))
print("图片img的大小：{}".format(img.shape))
print("图片img的高度：{}".format(img.shape[0]))
print("图片img的宽度：{}".format(img.shape[1]))
print("图片img的维度：{}".format(img.shape[2]))

cv.waitKey(0)