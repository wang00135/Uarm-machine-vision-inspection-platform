#!/usr/bin/env python3
# coding=utf8

import cv2 as cv
import numpy as np

# 构建一个用于加权均值核
kernel = np.array([[1, 2, 1],
                   [2, 4, 2],
                   [1, 2, 1]]) / 16


def test_img():
    img_path = './images/Fig4.11(a).jpg'
    img = cv.imread(img_path)
    # 使用自定义核进行2D卷积——加权均值
    dst = cv.filter2D(img, -1, kernel)
    cv.imwrite('weighted_mean.jpg', dst)
    cv.imshow('weighted_mean', dst)
    cv.waitKey(0)


def test_array():
    example = np.array(range(0, 25), np.uint8).reshape(-5, 5)
    print(example)
    print('*' * 60)
    dst = cv.filter2D(example, -1, kernel)
    print(dst)


if __name__ == '__main__':
    # test_img()
    test_array()
