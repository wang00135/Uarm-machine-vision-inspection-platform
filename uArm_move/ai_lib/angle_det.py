# import the necessary packages
import cv2
import numpy as np
from ai_lib.components import yaml_handle
import math
from ai_lib.components.utils import putText

LAB_FILE_PATH = "../resource/lab_config.yaml"

class AngleDetector:
    def __init__(self,lab_file_path=LAB_FILE_PATH ):
        self.lab_data = yaml_handle.get_yaml_data(lab_file_path)
        self.lab_file_path = lab_file_path

        self.max_area = 0
        self.areaMaxContour_max = 0
        self.color_area_max = 0

        self.range_rgb = {
            'red':   (0, 0, 255),
            'blue':  (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
        }

    def getAreaMaxContour(self, contours):
        # 找出面积最大的轮廓
        # 参数为要比较的轮廓的列表
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # 遍历所有轮廓
            contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:        # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                    area_max_contour = c
        return area_max_contour, contour_area_max  # 返回最大的轮廓

    def imgRec(self, img):
        self.lab_data = yaml_handle.get_yaml_data(self.lab_file_path )
        frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间

        for i in self.lab_data:
            frame_mask = cv2.inRange(frame_lab,
                                     (self.lab_data[i]['min'][0],
                                      self.lab_data[i]['min'][1],
                                      self.lab_data[i]['min'][2]),
                                     (self.lab_data[i]['max'][0],
                                      self.lab_data[i]['max'][1],
                                      self.lab_data[i]['max'][2]))  # 对原图像和掩模进行位运算

            opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))   # 开运算
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))      # 闭运算
            contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
            areaMaxContour, area_max = self.getAreaMaxContour(contours)  # 找出最大轮廓

            if areaMaxContour is not None:
                if area_max > self.max_area:  # 找最大面积
                    self.max_area = area_max
                    self.color_area_max = i
                    self.areaMaxContour_max = areaMaxContour

            if self.max_area > 2500:  # 有找到最大面积
                rect = cv2.minAreaRect(self.areaMaxContour_max)
                box = np.int0(cv2.boxPoints(rect))
                rotation_angle = rect[2]
                print(rotation_angle)
                cv2.drawContours(img, [box], -1, self.range_rgb[self.color_area_max], 2)
                self.max_area = 0
                (x, y, w, h) = cv2.boundingRect(box)
                img = putText(img, "{:.2f}".format(rotation_angle) + "°", org=(x, y+10), color=(255, 255, 255))  # 结果绘制

        return img


if __name__ == "__main__":
    a = AngleDetector()
    cap = cv2.VideoCapture(0)

    while True:
        re, img = cap.read()
        img = a.imgRec(img)
        cv2.imshow("d", img)
        cv2.waitKey(10)
