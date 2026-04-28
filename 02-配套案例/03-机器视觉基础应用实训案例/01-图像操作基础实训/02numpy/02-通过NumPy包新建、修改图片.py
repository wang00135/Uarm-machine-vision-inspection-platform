#通过NumPy包新建、修改图片

import cv2 as cv
import numpy as np

#新建一个200×200的三通道像素值均为127的灰色图像- BGR(127,127,127)
source_img = np.ones((200,200,3), np.uint8)*127
#利用列表的切片操作将图片中坐标为（100，100）的像素点改为绿色-BGR(0,255,0)
source_img[100,100] = [0,255,0]

#利用NumPy工具将图片中坐标为（50，50）的像素点改为红色-BGR(0,0,255)
print(source_img.item(50, 50, 2))
source_img.itemset((50,50, 0), 0)
source_img.itemset((50,50, 1), 0)
source_img.itemset((50,50, 2), 255)

#显示修改后的图片
cv.imshow('windows',source_img)
cv.waitKey(0)