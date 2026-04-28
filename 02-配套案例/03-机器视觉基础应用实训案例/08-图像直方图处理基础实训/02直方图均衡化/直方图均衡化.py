import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# 绘制直方图
def custom_hist(gray):
    h, w = gray.shape
    hist = np.zeros([256], dtype=np.uint8)
    for row in range(h):
        for col in range(w):
            pv = gray[row, col]
            hist[pv] += 1

    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.show()


src = cv.imread("./img2.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
cv.imshow("input", src)
dst = cv.equalizeHist(gray)
cv.imshow("outputEH", dst)

#custom_hist(gray)
custom_hist(dst)

cv.waitKey(0)
cv.destroyAllWindows()
