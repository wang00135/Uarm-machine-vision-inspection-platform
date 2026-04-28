#从本地视频文件获取视频
import cv2 as cv

#设置本地视频文件路径
path = './test.mp4'
#获取本地视频对象
cap = cv.VideoCapture(path)
#如果检测到正确获取视频对象已打开
if cap.isOpened():
    state, frame = cap.read() #抓取下一个视频帧状态和图像
    while state:              #当抓取成功则进入循环
        state,frame = cap.read() #抓取每一帧图像
        cv.imshow('video',frame) #显示图像帧
        k = cv.waitKey(25)       #每25ms读取一次键盘按键，同时控制帧率
        if k == 113 :            #当检测到q键按下，程序退出
            break
