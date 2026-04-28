#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
油画滤镜的设计与实现
"""
# 定义油画滤镜实现
# 参数：
# templateSize：模板大小
# bucketSize：桶阵列
# step：模板滑动步长
def oilPainting(img, templateSize, bucketSize, step):
    # 图像灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 获取灰度图在桶中的所属分区
    gray = ((gray / 256) * bucketSize).astype(int)  
    h, w = img.shape[:2]
    
    # 用来存放过滤图像
    oilImg = np.zeros(img.shape, np.uint8)  

    for i in range(0, h, step):
        top = i - templateSize
        bottom = i + templateSize + 1
        if top < 0:
            top = 0
        if bottom >= h:
            bottom = h - 1

        for j in range(0, w, step):
            left = j - templateSize
            right = j + templateSize + 1
            if left < 0:
                left = 0
            if right >= w:
                right = w - 1

            # 灰度等级统计
            buckets = np.zeros(bucketSize, np.uint8)  # 桶阵列，统计在各个桶中的灰度个数
            bucketsMean = [0, 0, 0]  # 对像素最多的桶，求其桶中所有像素的三通道颜色均值
            # 对模板进行遍历
            for c in range(top, bottom):
                for r in range(left, right):
                    buckets[gray[c, r]] += 1  # 模板内的像素依次投入到相应的桶中，有点像灰度直方图

            maxBucket = np.max(buckets)  # 找出像素最多的桶以及它的索引
            maxBucketIndex = np.argmax(buckets)

            for c in range(top, bottom):
                for r in range(left, right):
                    if gray[c, r] == maxBucketIndex:
                        bucketsMean += img[c, r]
            bucketsMean = (bucketsMean / maxBucket).astype(int)  # 计算三通道颜色均值

            # 油画图
            for m in range(step):
                for n in range(step):
                    oilImg[m + i, n + j] = (bucketsMean[0], bucketsMean[1], bucketsMean[2])
    return oilImg

import cv2
import matplotlib.pyplot as plt
import numpy as np

# 图片读取与显示
img = cv2.imread('Resources/yh.jpg', cv2.IMREAD_ANYCOLOR)
oil = oilPainting(img, 4, 8, 2)

cv2.imshow("yh",img)
cv2.waitKey(0)

# 结果显示
cv2.imshow("yh_result",oil)
cv2.waitKey(0)
