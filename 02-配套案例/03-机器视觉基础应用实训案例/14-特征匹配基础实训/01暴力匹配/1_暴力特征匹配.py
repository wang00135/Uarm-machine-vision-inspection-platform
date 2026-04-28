#!/usr/bin env python3
# -*- coding:UTF8 -*-


"""
暴力匹配（BFMatcher）是指用暴力方法找到点集一中每个描述符在点集二中距离最近的描述符
    描述符之间做距离测试
    首先初始化BF匹配器，获得BF对象
    class BFMatcher(DescriptorMatcher)
        Class methods defined here:
          create(...) from builtins.type
            create([, normType[, crossCheck]]) -> retval
                normType用来指定使用距离测试的类型，默认值是cv2.Norm_L2
                    可选值为：NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2
                crossCheck：crossCheck（交叉验证）是消除False-positive matches的一种方式
                            另外一种方式是ratio，knn就是ratio的一种
                            使用knnMatch的时候，crossCheck要设置成False
                            默认值为False
    使用函数bf.match()开始匹配
    match(queryDescriptors, trainDescriptors[, mask]) -> matches
        queryDescriptors：查询描述符
        trainDescriptors：训练描述符
        返回 matches：DMatch对象列表
            DMatch.distance - 描述符之间的距离，越低越好
            DMatch.trainIdx - 训练描述符里的描述符索引
            DMatch.queryIdx - 查询描述符里的描述符索引
            DMatch.imgIdx - 训练图像的索引


    使用函数drawMatches绘制匹配到的关键点
    drawMatches(img1, keypoints1, img2, keypoints2, matches1to2, outImg[, matchColor[, singlePointColor[, matchesMask[, flags]]]]) -> outImg
        img1：图像1
        keypoints1：图像1中的特征点
        img2：图像2
        keypoints2:图像2中的特征点
        matches1to2：matches1to2 Matches from the first image to the second one, which means that keypoints1[i]
         has a corresponding point in keypoints2[matches[i]]
        matchColor：指定画线的颜色，默认值表示颜色是随机产生的
        matchColor：单个关键点圆圈的颜色，默认值-1，表示颜色随机产生
        flags：绘线标志位,LINE_4 = 4 LINE_8 = 8 LINE_AA = 16
        返回关键点匹配绘制结果图像
"""

import cv2 as cv


def main():
    img = cv.imread('./shape.png')
    test = cv.imread('./test.png')

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    test_gray = cv.cvtColor(test, cv.COLOR_BGR2GRAY)

    # 得到两幅图的关键点, 及描述符
    orb = cv.ORB_create()
    kp, des = orb.detectAndCompute(img_gray, None)
    kp_t, des_t = orb.detectAndCompute(test_gray, None)

    # 初识BF匹配器
    bf = cv.BFMatcher().create(crossCheck = True)

    # 开始匹配
    matches = bf.match(des, des_t)
    # 排序，升序，得到最优匹配结果
    matches = sorted(matches, key = lambda x: x.distance)
    result = cv.drawMatches(img, kp, test, kp_t, matches[:len(matches) // 2], None, flags = cv.LINE_AA)

    cv.imshow('result', result)
    cv.imwrite('./outputs/bf_result.jpg', result)
    cv.waitKey(0)
    cv.destroyWindow('matches')


if __name__ == '__main__':
    main()
