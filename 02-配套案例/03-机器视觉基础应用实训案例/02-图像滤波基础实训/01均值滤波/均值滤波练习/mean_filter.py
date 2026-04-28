#!/usr/bin/env python3
# coding=utf8

import cv2 as cv

img_path = '../images/Fig4.11(a).jpg'

img = cv.imread(img_path)

blur_3X3 = cv.blur(img, (3, 3))
blur_5X5 = cv.blur(img, (5, 5))
blur_9X9 = cv.blur(img, (9, 9))
blur_15X15 = cv.blur(img, (15, 15))
blur_35X35 = cv.blur(img, (35, 35))

cv.imwrite('blur_3X3.jpg', blur_3X3)
cv.imwrite('blur_5X5.jpg', blur_5X5)
cv.imwrite('blur_9X9.jpg', blur_9X9)
cv.imwrite('blur_15X15.jpg', blur_15X15)
cv.imwrite('blur_35X35.jpg', blur_35X35)
