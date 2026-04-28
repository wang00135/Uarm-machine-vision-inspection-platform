"""
ORB快速角点检测示例代码

cv2.ORB_create()是创建一个ORB对象，其函数原型为：
ORB_create([, nfeatures[, scaleFactor[, nlevels[, edgeThreshold[, firstLevel[, WTA_K[, scoreType[, patchSize[, fastThreshold]]]]]]]]]) -> retval
参数解析：
nfeatures:保留的特征点个数
……
"""

import cv2 as cv
import copy

def main():
    motor = cv.imread('./motor.jpg')
    motor_copy = copy.copy(motor)


    #旋转图像90°
    motor_rotate = cv.rotate(motor,cv.ROTATE_90_CLOCKWISE)
    motor_rotate_copy = copy.copy(motor_rotate)

    #获取检测图像的灰度图
    motor_gray = cv.cvtColor(motor_copy,cv.COLOR_BGR2GRAY)
    motor_rotate_gray = cv.cvtColor(motor_rotate_copy,cv.COLOR_BGR2GRAY)

    #新建ORB角点检测对象，仅保留500个特征
    orb = cv.ORB_create(nfeatures= 500)

    #获得两幅图像的特征点和特征描述符
    kp1, des1 = orb.detectAndCompute(motor_gray,None)
    kp2, des2 = orb.detectAndCompute(motor_rotate_gray,None)

    #在原始图像上画出特征点
    motor_rotate = cv.drawKeypoints(motor_rotate, kp2, None, (255, 0, 0))
    motor = cv.drawKeypoints(motor,kp1,None,(255,0,0))

    cv.imshow('motor_rotate', motor_rotate)
    cv.imshow('motor', motor)



    cv.waitKey(0)

if __name__ == '__main__':
    main()