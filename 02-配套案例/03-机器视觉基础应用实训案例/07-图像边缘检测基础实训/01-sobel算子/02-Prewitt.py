import cv2
import numpy as np

moon = cv2.imread("./sudoku.jpg", 0)   #读取图片，并且为灰度图
row, column = moon.shape                #获取图片形状 （行， 列）

moon_f = np.copy(moon)
moon_f = moon_f.astype("float")
prewitt = np.zeros((row, column))
print(type(prewitt[0, 0]))

#计算X轴和Y轴梯度
for x in range(1, row - 1):
    for y in range(1, column - 1):
        gx = abs((moon_f[x + 1, y - 1] + moon_f[x + 1, y] + moon_f[x + 1, y + 1]) - (
                moon_f[x - 1, y - 1] + moon_f[x - 1, y] + moon_f[x - 1, y + 1]))
        gy = abs((moon_f[x - 1, y + 1] + moon_f[x, y + 1] + moon_f[x + 1, y + 1]) - (
                moon_f[x - 1, y - 1] + moon_f[x, y - 1] + moon_f[x + 1, y - 1]))
        prewitt[x, y] = gx + gy



sharp = moon_f + prewitt
sharp = np.where(sharp < 0, 0, np.where(sharp > 255, 255, sharp))
sharp = sharp.astype("uint8")

cv2.imshow("src", moon)
cv2.imshow("prewitt_sharp", sharp)

cv2.waitKey()