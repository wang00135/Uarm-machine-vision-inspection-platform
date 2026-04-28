import glob

import cv2 as cv
import numpy as np


# 鼠标回调函数
def showPixelValue(event, x, y, flags, param):
    global img, combinedResult, placeholder

    if event == cv.EVENT_MOUSEMOVE:
        # 获取鼠标悬停点的像素
        bgr = img[y, x]

        # 转换颜色空间
        # ycb = cv.cvtColor(np.uint8([[bgr]]), cv.COLOR_BGR2YCrCb)[0][0]
        lab = cv.cvtColor(np.uint8([[bgr]]), cv.COLOR_BGR2Lab)[0][0]
        hsv = cv.cvtColor(np.uint8([[bgr]]), cv.COLOR_BGR2HSV)[0][0]

        # 创建黑色背景
        placeholder = np.zeros((img.shape[0], 400, 3), dtype = np.uint8)

        # 绘制
        cv.putText(placeholder, "BGR {}".format(bgr), (20, 70), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                   cv.LINE_AA)
        cv.putText(placeholder, "HSV {}".format(hsv), (20, 140), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                   cv.LINE_AA)
        # cv.putText(placeholder, "YCrCb {}".format(ycb), (20, 210), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
        #            cv.LINE_AA)
        cv.putText(placeholder, "LAB {}".format(lab), (20, 280), cv.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                   cv.LINE_AA)

        # 将两张图合并成一张图
        combinedResult = np.hstack([img, placeholder])

        cv.imshow('PRESS P for Previous, N for Next Image', combinedResult)


if __name__ == '__main__':

    # 加载图片设置鼠标回调函数
    global img
    files = glob.glob('images/rub*.jpg')
    files.sort()
    img = cv.imread(files[0])
    img = cv.resize(img, (400, 400))
    cv.imshow('PRESS P for Previous, N for Next Image', img)

    # 创建空窗体
    cv.namedWindow('PRESS P for Previous, N for Next Image')
    # 设置鼠标回调函数
    cv.setMouseCallback('PRESS P for Previous, N for Next Image', showPixelValue)
    i = 0
    while (1):
        k = cv.waitKey(1) & 0xFF
        if k == ord('n'):
            i += 1
            img = cv.imread(files[i % len(files)])
            img = cv.resize(img, (400, 400))
            cv.imshow('PRESS P for Previous, N for Next Image', img)

        elif k == ord('p'):
            i -= 1
            img = cv.imread(files[i % len(files)])
            img = cv.resize(img, (400, 400))
            cv.imshow('PRESS P for Previous, N for Next Image', img)

        elif k == 27:
            cv.destroyAllWindows()
            break
