# 1.导入函数库
import cv2
import numpy as np


def nothing(obj):
    """
       滑动条回调函数：获取滑动条的数值可以在回调函数中进行
       :param obj: 空
       :return: 空
       """
    pass


# 2.创建一个黑色的图像作为调色板
img = np.zeros((500, 1000, 3), np.uint8)

# 3.为 滑动条 创建一个窗口作为载体
cv2.namedWindow('image')
cv2.resizeWindow("image", 500, 500)

# 4.创建滑动条 -> 创建RGB的滑动条
# createTrackbar()参数含义：  1)滑动条名称 2)滑动条依附的窗口 3)滑动条最小值 4)滑动条最大值  5)回调函数
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)
# 为 ON/OFF 功能创建开关
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

# 5.图像预处理 + 颜色分割
# while循环执行显示动作
while True:

    # 5-1：获取滑动条数值 -> 分别获取滑动条的数值
    # getTrackbarPos()参数含义：   1)创建滑动条时设置的名称   2)滑动条依附的窗口
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    # 5-2：判断switch开关是否处于开启状态
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b, g, r]

    cv2.imshow('image', img)

    # 5-3：延迟执行对应操作
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
