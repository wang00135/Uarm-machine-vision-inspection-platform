import cv2
import numpy as np

moon = cv2.imread("./sudoku.jpg", 0)
row, column = moon.shape
moon_f = np.copy(moon)
moon_f = moon_f.astype("float")

Roberts = np.zeros((row, column))

for x in range(row - 1):
    for y in range(column - 1):
        gx = abs(moon_f[x + 1, y + 1] - moon_f[x, y])
        gy = abs(moon_f[x + 1, y] - moon_f[x, y + 1])
        Roberts[x, y] = gx + gy

sharp = moon_f + Roberts

sharp = np.where(sharp < 0, 0, np.where(sharp > 255, 255, sharp))
sharp = sharp.astype("uint8")

cv2.imshow("src", moon)
cv2.imshow("Roberts_sharp", sharp)
cv2.imwrite('./Roberts_sharp.jpg',sharp)

cv2.waitKey()
