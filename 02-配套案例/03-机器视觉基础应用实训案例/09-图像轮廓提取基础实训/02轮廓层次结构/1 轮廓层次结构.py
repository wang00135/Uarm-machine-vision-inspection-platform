#!/usr/bin/env python3
# encod:utf8

import cv2 as cv


def splitContour(img, flag = True):
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    print(hierarchy)
    if flag:
        i = 0
        for i in range(len(hierarchy[0])):
            if (hierarchy[0][i][0] != -1 and hierarchy[0][i][3] == -1) or (
                    hierarchy[0][i][0] == -1 and hierarchy[0][i][1] != -1 and hierarchy[0][i][3] == -1):
                x, y, w, h = cv.boundingRect(contours[i])
                temp = img[y:y + h, x:x + w]
                cv.imshow('temp', temp)
                cv.waitKey(0)
    else:
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            temp = img[y:y + h, x:x + w]
            cv.imshow('temp', temp)
            cv.waitKey(0)


def main():
    img_path = 'plate.png'
    gray = cv.imread(img_path, 0)
    splitContour(gray, flag = True)
    # splitContour(gray, flag=False)


if __name__ == '__main__':
    main()
