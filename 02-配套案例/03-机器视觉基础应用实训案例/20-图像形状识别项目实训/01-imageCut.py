import cv2 as cv
import numpy as np

def imgHandle(img):
        # 将原图像灰度化
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 平均滤波
        blur = cv.blur(gray, (5, 5))
        # 简单阈值的二值化
        # ret, thresh = cv.threshold(blur, 0,255,cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
        ret, thresh = cv.threshold(blur, 170, 255, cv.THRESH_BINARY)
        cv.imshow('out1', thresh)
        # 查找轮廓
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, \
                                              cv.CHAIN_APPROX_SIMPLE)[-2:]
        print(len(contours))
        # 找最大面积轮廓
        area_max = 0
        _cnt = None
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            area = cv.contourArea(cnt)
            if x < 5 or y < 5 or (gray.shape[1] - 5 <= x <= gray.shape[1]) or (gray.shape[0] - 5 <= y <= gray.shape[0]):
                print("过滤边框", x, y, w, h)
                continue
            if area > area_max:
                area_max = area
                _cnt = cnt
        # 直边界矩形
        x, y, w, h = cv.boundingRect(_cnt)
        print(x, y, w, h)
        frame = img[y:h + y, x:w + x]
        return frame

input = cv.imread("Shape.png")
cv.imshow('input', input)
# 图像剪裁
out = imgHandle(input)
cv.imwrite("Shape1.png", out)  # 保存剪裁后的图像
cv.imshow('out', out)
cv.waitKey()
cv.destroyAllWindows()


