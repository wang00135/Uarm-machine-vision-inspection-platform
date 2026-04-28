# import the necessary packages
import cv2
import numpy as np
from components import yaml_handle
import math
from components.utils import putText

LAB_FILE_PATH = "resource/lab_config.yaml"

class AreaDetector:
    def __init__(self, lab_file_path=LAB_FILE_PATH ):
        self.lab_data = yaml_handle.get_yaml_data(lab_file_path)
        self.lab_file_path = lab_file_path

        self.max_area = 0
        self.areaMaxContour_max = 0
        self.color_area_max = 0

        self.standard_pixel = 0  # 获得基准像素值
        self.standard_mm = 30  # 与基准尺寸，单位毫米

        self.range_rgb = {
            'red':   (0, 0, 255),
            'blue':  (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
        }

    def distance(self, pixel):
        temp = (self.standard_mm * pixel) / self.standard_pixel  # 计算的到被测物体真实尺寸
        return round(temp, 2)  # 结果保留两

    def areaDetect(self, c, width, height):
        shape = "unidentified"
        area = 0
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # 如果形状是三角形，它将有3个顶点
        if len(approx) == 3:
            shape = "三角形"
            area = (width * height) / 2

        # 如果形状有4个顶点，它要么是一个正方形，要么是矩形
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # 正方形的宽高比近似等于1，否则，形状就是矩形
            shape = "正方形" if 0.95 <= ar <= 1.05 else "矩形"
            area = width * height
        # 如果形状是六边形，它将有6个顶点
        elif len(approx) == 6:
            shape = "六边形"

        else:
            shape = "圆形"
            area = 3.14 * (width/2) *  3.14 * (width/2)
        # 返回形状的名称
        return shape, area

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

    def imgRec(self, img, flag=False):
        self.lab_data = yaml_handle.get_yaml_data(self.lab_file_path )
        frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间
        rect = None

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
                cv2.drawContours(img, [box], -1, self.range_rgb[self.color_area_max], 2)
                self.max_area = 0
                (x, y, w, h) = cv2.boundingRect(box)
                if self.standard_pixel != 0:  # 判断基准像素是否更新
                    width = self.distance(rect[1][0])
                    height = self.distance(rect[1][1])
                    shape_rec, area_rec = self.areaDetect(self.areaMaxContour_max, width, height)
                    img = putText(img, "{}:{:.0f}mm".format(shape_rec, area_rec), org=(x, y + 10),
                                  color=(255, 255, 255))  # 结果绘制

        if flag and rect is not None:
            pixel = int((rect[1][0] + rect[1][1]) / 2)  # 计算基准像素值
            self.standard_pixel = pixel  # 更新基准像素值

        return img




if __name__ == "__main__":
    area_det = AreaDetector()
    cap = cv2.VideoCapture(0)

    while True:
        re, frame = cap.read()
        # 调整图像，进行ROI，获取分拣区域图像
        frame = frame[int(frame.shape[0] / 4.6): int(frame.shape[0] - frame.shape[0] / 2.7),
                int(frame.shape[1] / 3.4): int(frame.shape[1] - frame.shape[1] / 4.5)]
        size = frame.shape[0:2]
        catframe = cv2.resize(frame, (int(size[1] * 2), int(size[0]) * 2))

        key = cv2.waitKey(10)
        img = area_det.imgRec(catframe, key)
        cv2.imshow("d", img)

