#!/usr/bin/env python3
# -*- coding:UTF8 -*-

"""
FAST快速角点检测示例代码

cv2.FastFeatureDetector_create()是创建一个FAST对象，其函数原型为：
FastFeatureDetector_create([, threshold[, nonmaxSuppression[, type]]])
参数解析：
threshold:阈值
非极大值抑制：Boolean类型
邻域大小：共有三个取值，分别为如下：
cv2.FAST_FEATURE_DETECTOR_TYPE_5_8
cv2.FAST_FEATURE_DETECTOR_TYPE_7_12
cv2.FAST_FEATURE_DETECTOR_TYPE_9_16
"""

import cv2 as cv
import numpy as np

def main():
    img = cv.imread('fast.jpg')
    img_copy = img.copy()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 初始化FAST算法
    # fast  = cv.FastFeatureDetector_create()
    # 或带参数初始化
    fast = cv.FastFeatureDetector_create(threshold=20,nonmaxSuppression=True,type=cv.FAST_FEATURE_DETECTOR_TYPE_9_16)
    kp = fast.detect(gray,None)

    img = cv.drawKeypoints(img, kp, None, (255, 0, 0), 2)

    # 查看是否采用了非极大值抑制
    nonmaxSuppression = fast.getNonmaxSuppression()
    if nonmaxSuppression:
        fast.setNonmaxSuppression(False)

    # 关闭非极大值抑制
    kp = fast.detect(img_copy,None)
    print(len(kp))
    img_copy =cv.drawKeypoints(img_copy, kp, None, (255, 0, 0), 2)


    cv.imshow('img', img)
    cv.imshow('img_copy', img_copy)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()