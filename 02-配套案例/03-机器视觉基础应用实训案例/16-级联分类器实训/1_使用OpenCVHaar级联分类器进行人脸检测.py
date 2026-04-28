#!/usr/bin env python3
# -*- coding:UTF8 -*-

"""
        
"""

import cv2 as cv

baby = cv.imread('baby.jpg')
baby_gray = cv.cvtColor(baby, cv.COLOR_BGR2GRAY)

# 加载人脸分类器
haar_cascade_face = cv.CascadeClassifier(
    './haarcascade/haarcascade_frontalface_default.xml')

faces_rects = haar_cascade_face.detectMultiScale(baby_gray,
                                                 scaleFactor = 1.2,
                                                 minNeighbors = 5)
print('Faces found: ', len(faces_rects))
for (x, y, w, h) in faces_rects:
    # 人脸绘制
    cv.rectangle(baby, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv.imwrite('./outputs/baby_face.jpg', baby)
cv.imshow('baby_face', baby)
cv.waitKey(0)
