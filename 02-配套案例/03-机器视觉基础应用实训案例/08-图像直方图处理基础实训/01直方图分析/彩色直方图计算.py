#!/usr/bin env python3
# -*- coding:UTF8 -*-

#彩色图像直方图的计算与显示
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('test.png')
cv2.imshow('SrcImage', img)
chans = cv2.split(img)
colors = ('b', 'g', 'r')
plt.title("’Flattened’ Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")

for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])
plt.show()
