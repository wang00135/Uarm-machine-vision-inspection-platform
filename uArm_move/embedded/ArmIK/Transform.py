# encoding:utf-8
import cv2
import math
import numpy as np

class TransForm(object):
    def __init__(self, map_param_path=None):

        # 机械臂原点即云台中心，距离摄像头画面中心的距离， 单位cm
        self.image_center_distance = 13.5

        # 计算每个像素对应的实际距离
        self.map_param_ = np.load(map_param_path)['map_param']
        print("wq--map_param:", self.map_param_)

    def leMap(self, x, in_min, in_max, out_min, out_max):
        # 数值映射 将一个数从一个范围映射到另一个范围
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def convertCoordinate(self, x, y, size):
        # 将图形的像素坐标转换为机械臂的坐标系
        # 传入坐标及图像分辨率，例如(100, 100, (640, 320))
        x = self.leMap(x, 0, size[0], 0, 640)
        x = x - 320
        x_ = round(x * self.map_param_ , 2)

        y = self.leMap(y, 0, size[1], 0, 480)
        y = y - 240
        y_ = round(y * self.map_param_ + self.image_center_distance, 2)

        return x_, y_

    def world2pixel(self, l, size):
        # 将现实世界的长度转换为图像像素长度
        # 传入坐标及图像分辨率，例如(10, (640, 320))
        l_ = round(l/self.map_param_, 2)

        l_ = self.leMap(l_, 0, 640, 0, size[0])

        return l_

    def getROI(self, box):
        # 获取检测物体的roi区域
        # 传入cv2.boxPoints(rect)返回的四个顶点的值，返回极值点
        x_min = min(box[0, 0], box[1, 0], box[2, 0], box[3, 0])
        x_max = max(box[0, 0], box[1, 0], box[2, 0], box[3, 0])
        y_min = min(box[0, 1], box[1, 1], box[2, 1], box[3, 1])
        y_max = max(box[0, 1], box[1, 1], box[2, 1], box[3, 1])

        return (x_min, x_max, y_min, y_max)

    def getMaskROI(self, frame, roi, size):
        # 除roi区域外全部变成黑色
        # 传入图形，roi区域，图形分辨率
        x_min, x_max, y_min, y_max = roi
        x_min -= 10
        x_max += 10
        y_min -= 10
        y_max += 10

        if x_min < 0:
            x_min = 0
        if x_max > size[0]:
            x_max = size[0]
        if y_min < 0:
            y_min = 0
        if y_max > size[1]:
            y_max = size[1]

        black_img = np.zeros([size[1], size[0]], dtype=np.uint8)
        black_img = cv2.cvtColor(black_img, cv2.COLOR_GRAY2RGB)
        black_img[y_min:y_max, x_min:x_max] = frame[y_min:y_max, x_min:x_max]

        return black_img

    def getCenter(self, rect, roi, size, square_length):
        # 获取木块中心坐标
        # 传入minAreaRect函数返回的rect对象， 木快极值点， 图像分辨率， 木块边长

        x_min, x_max, y_min, y_max = roi

        # 根据木块中心的坐标，来选取最靠近图像中心的顶点，作为计算准确中心的基准
        if rect[0][0] >= size[0]/2:
            x = x_max
        else:
            x = x_min
        if rect[0][1] >= size[1]/2:
            y = y_max
        else:
            y = y_min

        # 计算木块的对角线长度
        square_l = square_length/math.cos(math.pi/4)

        # 将长度转换为像素长度
        square_l = self.world2pixel(square_l, size)

        # 根据木块的旋转角来计算中心点
        dx = abs(math.cos(math.radians(45 - abs(rect[2]))))
        dy = abs(math.sin(math.radians(45 + abs(rect[2]))))

        if rect[0][0] >= size[0] / 2:
            x = round(x - (square_l/2) * dx, 2)
        else:
            x = round(x + (square_l/2) * dx, 2)
        if rect[0][1] >= size[1] / 2:
            y = round(y - (square_l/2) * dy, 2)
        else:
            y = round(y + (square_l/2) * dy, 2)

        return x, y

    def getAngle(self, x, y, angle):
        # 获取旋转的角度
        # 参数：机械臂末端坐标, 木块旋转角
        theta6 = round(math.degrees(math.atan2(abs(x), abs(y))), 1)
        angle = abs(angle)

        if x < 0:
            if y < 0:
                angle1 = -(90 + theta6 - angle)
            else:
                angle1 = theta6 - angle
        else:
            if y < 0:
                angle1 = theta6 + angle
            else:
                angle1 = 90 - theta6 - angle

        if angle1 > 0:
            angle2 = angle1 - 90
        else:
            angle2 = angle1 + 90

        if abs(angle1) < abs(angle2):
            servo_angle = int(500 + round(angle1 * 1000 / 240))
        else:
            servo_angle = int(500 + round(angle2 * 1000 / 240))

        return servo_angle

        # 参数为要比较的轮廓的列表

    def getAreaMaxContour(self, contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # 历遍所有轮廓
            contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                    area_max_contour = c
        return area_max_contour, contour_area_max  # 返回最大的轮廓

    def getCoordinate(self, img, img_centerx, img_centery):
        # print("centery:", img_centery, img_centerx)
        max_area = 0
        size = (640, 480)
        world_x = world_y = rotation_angle = None
        buf_img = img.copy()
        src_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, src_img = cv2.threshold(src_img, 100, 255, cv2.THRESH_BINARY)
        # cv2.imshow("i", src_img)
        opened = cv2.morphologyEx(src_img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
        # cv2.imshow("closed", closed)
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
        areaMaxContour, area_max = self.getAreaMaxContour(contours)  # 找出最大轮廓

        if areaMaxContour is not None:
            # print("--max_area:", area_max)
            if area_max > 2500:  # 有找到最大面积
                rect = cv2.minAreaRect(areaMaxContour)
                rotation_angle = rect[2]
                box = np.int0(cv2.boxPoints(rect))
                cv2.drawContours(buf_img, [box], -1, (0, 255, 0), 2)
                # cv2.imshow("buf_img", buf_img)
                world_x, world_y = self.convertCoordinate(img_centerx, img_centery, size)  # 转换为现实世界坐标

        return (world_x, world_y, rotation_angle)
