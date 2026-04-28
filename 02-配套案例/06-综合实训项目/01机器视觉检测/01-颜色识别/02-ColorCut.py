'''
    色彩分割的设计与实现——项目代码
'''
'''
    色彩分割的设计与实现步骤记录：
    1.导入OpenCV库
    2.定义图片文件的位置
    3.为滑动条创建一个窗口作为载体
    4.创建滑动条 -> 创建 HSV 六个变量的滑动条
    5.图像预处理 + 颜色分割 + 结果调试
        5-1：读入一张图像
        5-2：色彩空间转换 -> 将RGB图像转换为HSV图像
        5-3：获取滑动条数值 -> 分别获取六个滑动条的数值
        5-4：颜色分割(掩模) -> 收纳大于最低值，小于最高值的像素
        5-5：图像像素级运算 -> 掩模 & 原图 = 感兴趣区域(ROI)
        5-6：获取ROI区域后完成显示和调试
        5-7：延迟执行对应操作
    6.关闭所有窗口
'''

# 1.导入需要用到的函数库
import cv2
import numpy as np


def stackImages(scale, imgArray):
    """
        将多张图像压入同一个窗口显示，可使用范围：
        :param scale:float类型，输出图像显示百分比，控制缩放比例，0.5=图像分辨率缩小一半
        :param imgArray:元组嵌套列表，需要排列的图像矩阵
        :return:输出图像
    """

    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def empty(obj):
    """
        滑动条回调函数：获取滑动条的数值可以在回调函数中进行
        :param obj: 空
        :return: 空
        """
    pass


# 2.定义图片文件位置
img_path = "Resources/test2.jpg"

# 3.为 滑动条 创建一个窗口作为载体
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)

# 4.创建滑动条 -> 创建 HSV 六个变量的滑动条
# createTrackbar()参数含义：  1)滑动条名称 2)滑动条依附的窗口 3)滑动条最小值 4)滑动条最大值  5)回调函数
cv2.createTrackbar("Hue Min", "TrackBars", 0, 180, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 19, 180, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 134, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 160, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# 5-1：读入一张图像
img = cv2.imread(img_path)

# 5-2：色彩空间转换 -> 将RGB图像转换为HSV图像
# cvtColor()参数含义：  1)需要转换的图像   2)色彩空间转换的模式，该参数来实现不同类型的颜色空间转换
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 5.图像预处理 + 颜色分割
# while循环执行显示动作
while True:

    # 5-3：获取滑动条数值 -> 分别获取六个滑动条的数值
    # getTrackbarPos()参数含义：   1)创建滑动条时设置的名称   2)滑动条依附的窗口
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    # 5-4：颜色分割(掩模) ->  收纳大于最低值，小于最高值的像素
    # 依次获取HSV三个变量的 最小阈值 与 最大阈值
    lower = np.array([[h_min], [s_min], [v_min]])
    upper = np.array([[h_max], [s_max], [v_max]])
    # inRange()参数含义：  1)需要分割的图像  2)最低值   3)最高值
    mask = cv2.inRange(imgHSV, lower, upper)

    # 5-5：图像像素级运算 -> 掩模 & 原图 = 感兴趣区域(ROI)
    # 对原图图像进行按位与的操作，掩码区域保留
    # bitwise_and()参数含义：  1)矩阵图像1  2)矩阵图像2   3)mask：掩模图像
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    # 5-6：获取ROI区域后对应显示和调试
    # 方式1：分开显示
    # cv2.imshow("Original", img)
    # cv2.imshow("HSV", imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)
    # 方式2：同窗显示
    imageStack = stackImages(1, ([img, imgHSV], [mask, imgResult]))
    cv2.imshow("stacked image", imageStack)

    # 5-7：延迟执行对应操作
    if cv2.waitKey(1) == ord('q'):
        break
# 6.关闭所有窗口
cv2.destroyAllWindows()
