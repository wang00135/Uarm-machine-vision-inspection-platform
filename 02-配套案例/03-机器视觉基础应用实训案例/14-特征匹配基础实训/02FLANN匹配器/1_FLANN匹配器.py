#!/usr/bin env python3
# -*- coding:UTF8 -*-


"""
FLANN是快速最近邻搜索包（Fast_Library_for_Approximate_Nearest_Neighbors）的简称。
它是一个对大数据集和高特征进行最近邻搜索算法的集合，
并且这些算法都是经过优化的，在面对大数据集时它的表现要好于BFMatcher
"""

import cv2 as cv
import numpy as np


def main():
    img = cv.imread('./shape.png')
    test = cv.imread('./test.png')

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    test_gray = cv.cvtColor(test, cv.COLOR_BGR2GRAY)

    # 得到两幅图的关键点
    orb = cv.ORB_create()
    kp, des = orb.detectAndCompute(img_gray, None)
    kp_t, des_t = orb.detectAndCompute(test_gray, None)
    des = des.astype(np.float32)
    des_t = des_t.astype(np.float32)

    # 低版本OpenCV中使用FLANN
    # 构造FLANN参数
    # FLANN_INDEX_KDTREE = 0
    # index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 10)
    # search_params = dict(checks=2)
    # # 初始化FLANN特征匹配器
    # flann = cv.FlannBasedMatcher(index_params, search_params)

    flann = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)

    # 开始匹配
    matches = flann.knnMatch(des, des_t, k = 2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    good.sort(key = lambda x: x[0].distance)
    result = cv.drawMatchesKnn(img, kp, test, kp_t, good[:len(good) // 2], None, flags = 2)

    cv.imshow('result', result)
    cv.imwrite('./outputs/flann_knn_result.jpg', result)

    cv.waitKey(0)
    cv.destroyWindow('matches')


if __name__ == '__main__':
    main()
