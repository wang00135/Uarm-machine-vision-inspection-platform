#彩色图像的直方图对比
import cv2 as cv
import numpy as np

img1 = cv.imread('test.png')
img2 = cv.imread('test1.png')

hsvt1 = cv.cvtColor(img1,cv.COLOR_BGR2HSV)
hsvt2 = cv.cvtColor(img2,cv.COLOR_BGR2HSV)

hist1 = cv.calcHist([hsvt1],[0,1],None,[180,256],[0,180,0,256])
hist2 = cv.calcHist([hsvt2],[0,1],None,[180,256],[0,180,0,256])

hstnor1 = cv.normalize(hist1,dst= None)
hstnor2 = cv.normalize(hist2,dst= None)

res1 = cv.compareHist(hstnor1,hstnor1,cv.HISTCMP_BHATTACHARYYA)
res2 = cv.compareHist(hstnor1,hstnor2,cv.HISTCMP_BHATTACHARYYA)

font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img1, str(round(res1,5)), (0, 50), font,2, (0, 255, 255),3)
cv.putText(img2, str(round(res2,5)), (0, 50), font,2, (0, 255, 255),3)

cv.imshow('img1',img1)
cv.imshow('img2',img2)

cv.imwrite('res1.jpg',img1)
cv.imwrite('res2.jpg',img2)
cv.waitKey(0)