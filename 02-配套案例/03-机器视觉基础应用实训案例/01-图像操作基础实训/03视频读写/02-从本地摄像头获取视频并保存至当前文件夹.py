#从本地摄像头获取视频并保存至当前文件夹
import cv2 as cv

#获取本地摄像头对象
cap = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc('I', '4', '2', '0')          #设置视频编解码格式
out = cv.VideoWriter('savefile.avi', fourcc,30,(640,480)) #设置视频保存的属性

#如果检测到摄像头已打开
if cap.isOpened():
    state, frame = cap.read() #抓取下一个视频帧状态和图像
    while state:              #当抓取成功则进入循环
        state,frame = cap.read() #抓取每一帧图像
        cv.imshow('video',frame) #显示图像帧
        out.write(frame)         #保存当前图像帧

        k = cv.waitKey(25)       #每25ms读取一次键盘按键，同时控制帧率
        if k == 113 :            #当检测到q键按下，程序退出
            break
