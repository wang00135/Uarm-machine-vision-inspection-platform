# coding: utf-8
import cv2
import numpy as np

'''
函数名：template_match
输入：
template    模板
img   原图
输出：
(x,y)    匹配位置的左上角坐标，找不到返回None
'''


def template_match(template, img):
    tpl_h, tpl_w = template.shape[:2]
    img_h, img_w = img.shape[:2]
    for i in range(img_h - tpl_h):
        for j in range(img_w - tpl_w):
            roi = img[i:i+tpl_h, j:j+tpl_w]
            if (template == roi).all():
                return (j,i)
    return None


# 程序入口
def main():
    # 读取原图
    resource = cv2.imread('src.jpg')
    # 截取模板
    tpl = resource[117:299, 154:376].copy()
    # 模板匹配
    pos = template_match(tpl, resource)
    tpl_h, tpl_w = tpl.shape[:2]
    # 结果绘制
    if pos is not None:
        x,y = pos
        cv2.rectangle(resource, (x,y), (x+tpl_w,y+tpl_h), (0, 255, 0), 2)
    # 结果显示
    cv2.imshow('template', tpl)
    cv2.imshow('result', resource)
    cv2.imwrite('template.jpg', resource)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
