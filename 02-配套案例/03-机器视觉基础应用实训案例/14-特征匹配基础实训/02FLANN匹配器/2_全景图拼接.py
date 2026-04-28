#!/usr/bin env python3
# -*- coding:UTF8 -*-

import cv2 as cv
import numpy as np


class Stitcher:

    def panorama_get(self, im1, im2, H):
        h1, w1 = im1.shape[:2]
        h2, w2 = im2.shape[:2]
        pts1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)  # 转为3维坐标
        pts2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
        pts1_ = cv.perspectiveTransform(pts1, H)  # H：3*3 矩阵，所以pts1也该为3维坐标
        pts = np.concatenate((pts1_, pts2), axis = 0)  # 列连接
        # np.min 是行优先
        [xmin, ymin] = np.int32(pts.min(axis = 0).ravel() - 0.5)
        [xmax, ymax] = np.int32(pts.max(axis = 0).ravel() + 0.5)
        t = [-xmin, -ymin]  # 左加右减
        Ht = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])  # 相当于一个向右平移
        result = cv.warpPerspective(im1, Ht.dot(H), (xmax - xmin, ymax - ymin),
                                    flags = cv.INTER_LINEAR,
                                    borderMode = cv.BORDER_REFLECT101)  # 最后一个参数是输出图像的宽、高
        result[t[1]:h2 + t[1], t[0]:w2 + t[0]] = im2
        return result

    def stitch(self, imageA, imageB, ratio = 0.75, reproThresh = 4, showMathes = True):

        H_A, W_A = imageA.shape[:2]
        H_B, W_B = imageB.shape[:2]
        H_MAX = max(H_A, H_B)
        W_MAX = max(W_A, W_B)
        imageA = cv.resize(imageA, (W_MAX, H_MAX), cv.INTER_LINEAR)
        imageB = cv.resize(imageB, (W_MAX, H_MAX), cv.INTER_LINEAR)
        # 第一步：两种图的关键点，及描述符
        (kpsA, dpsA) = self.detectandcompute(imageA)
        (kpsB, dpsB) = self.detectandcompute(imageB)

        # 获得变化的矩阵H
        M = self.matchKeypoint(kpsA, dpsA, kpsB, dpsB, ratio, reproThresh)

        if M is None:
            return None
        (matches, H, status) = M

        result = self.panorama_get(imageA, imageB, H)

        if showMathes:
            # 第六步：对图像的关键点进行连接
            via = self.showMatches(imageA, imageB, kpsA, kpsB, matches, status)

            return via, result

        return None, result

    # 画出关键点匹配结果
    def showMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # 将两个图像进行拼接
        # 根据图像的大小，构造全零矩阵
        H_A, W_A = imageA.shape[:2]
        H_B, W_B = imageB.shape[:2]
        via = np.zeros((max(H_A, H_B), W_A + W_B, 3), np.uint8)
        # 将图像A和图像B放到全部都是零的图像中
        via[:H_A, :W_A] = imageA
        via[:H_A, W_A:] = imageB
        # 根据matches中的索引，构造出点的位置信息
        for (trainIdx, queryIdx), s in zip(matches, status):
            if s == 1:
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0] + W_A), int(kpsB[trainIdx][1]))
                # 使用cv.line进行画图操作
                cv.line(via, ptA, ptB, (0, 255, 0), 1)

        return via

    def matchKeypoint(self, kpsA, dpsA, kpsB, dpsB, ratio, reproThresh):

        # 第二步：实例化BFM匹配， 找出符合添加的关键点的索引
        bf = cv.BFMatcher()

        matcher = bf.knnMatch(dpsA, dpsB, 2)
        matches = []

        for match in matcher:

            if len(match) == 2 and match[0].distance < match[1].distance * ratio:
                # 添加match[0]
                matches.append((match[0].trainIdx, match[0].queryIdx))
        # 第三步：使用cv.findHomography找出符合添加的H矩阵
        # 关键点必须等于4，
        if len(matches) >= 4:
            # 根据索引找出符合条件的位置
            kpsA = np.float32([kpsA[i] for (_, i) in matches])
            kpsB = np.float32([kpsB[i] for (i, _) in matches])
            # 找到两个平面之间的透视变换
            H, status = cv.findHomography(kpsA, kpsB, cv.RANSAC, reproThresh)

            return matches, H, status
        return None

    def detectandcompute(self, image):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        orb = cv.ORB_create()
        kps, des = orb.detectAndCompute(gray, None)
        kps = np.float32([kp.pt for kp in kps])
        return kps, des


def test():
    imgA_path = 'A.jpg'
    imgB_path = 'B.jpg'
    imgA = cv.imread(imgA_path)
    imgB = cv.imread(imgB_path)
    via, result = Stitcher().stitch(imgA, imgB)
    cv.imshow('test', result)
    cv.imshow('kps', via)
    cv.imwrite('./outputs/test.jpg', result)
    cv.imwrite('./outputs/via.jpg', via)
    cv.waitKey(0)


if __name__ == '__main__':
    test()
