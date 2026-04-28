import numpy as np
import cv2
from components import yaml_handle
from components.Transform import TransForm
import math
from tools.camera.camera import Camera

MAP_PARAM_PATH = "resource/camera_calibration/map_param.npz"
LAB_FILE_PATH = "resource/lab_config.yaml"
color_list = ['red', 'green', 'blue']
color_value = {'red': [0, 0, 255], 'green': [0, 255, 0], 'blue': [255, 0, 0]}


class ColorRec(object):
    def __init__(self, map_param_path=MAP_PARAM_PATH, lab_file_path=LAB_FILE_PATH):
        self.lab_data = yaml_handle.get_yaml_data(lab_file_path)
        self.lab_file_path = lab_file_path
        self.max_area = 0
        self.areaMaxContour_max = 0
        self.color_area_max = 0
        self.last_x = self.last_y = 0
        self.cont = 0

        self.transform = TransForm(map_param_path)

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
        center_x = None
        center_y = None
        world_x = None
        world_y = None
        box = None
        box_coordin = []
        color_id = []
        color = 0
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
            _cnt = None
            _col = None
            if areaMaxContour is not None:
                if area_max > self.max_area:  # 找最大面积
                    self.max_area = area_max
                    self.color_area_max = i
                    self.areaMaxContour_max = areaMaxContour

            if self.max_area > 2500:  # 有找到最大面积
                rect = cv2.minAreaRect(self.areaMaxContour_max)  # 得到最小外接矩形
                rotation_angle = rect[2]
                box = np.int0(cv2.boxPoints(rect)) # 计算中心点坐标
                pt1_x, pt1_y = box[0, 0], box[0, 1]
                pt2_x, pt2_y = box[2, 0], box[2, 1]
                center_x, center_y = int((pt1_x + pt2_x) / 2), int((pt1_y + pt2_y) / 2)

                roi = self.transform.getROI(box)  # 获取roi区域
                img_centerx, img_centery = self.transform.getCenter(rect, roi, (640, 480), 3)  # 获取木块中心坐标

                world_x, world_y = self.transform.convertCoordinate(img_centerx, img_centery, (640, 480))  # 转换为现实世界坐标
                box_coordin.append([world_x, world_y])
                cv2.drawContours(img, [box], -1, self.range_rgb[self.color_area_max], 2)
                cv2.putText(img, '(' + self.color_area_max + "," + str(world_x) + ',' +
                            str(world_y) + " " + " {:.2f}".format(rotation_angle) + ')',
                            (min(box[0, 0], box[2, 0]), box[2, 1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)   # 绘制中心点  self.range_rgb[self.color_area_max]

                cv2.circle(img, (center_x, center_y), 2, (255, 255, 255), 2)  # 绘制矩形
                distance = math.sqrt(pow(world_x - self.last_x, 2) + pow(world_y - self.last_y, 2))  # 对比上次坐标来判断是否移动
                self.last_x, self.last_y = world_x, world_y
                if distance < 0.5:
                    self.cont += 1
                    if self.cont > 60:
                        self.cont = 0
                        # angle = self.transform.getAngle(world_x, world_x, rotation_angle)  # 计算夹持器需要旋转的角度
                        if self.color_area_max == 'red':  # 红色最大
                            color = 1
                        elif self.color_area_max == 'green':  # 绿色最大
                            color = 2
                        elif self.color_area_max == 'blue':  # 蓝色最大
                            color = 3
                        else:
                            color = 0
                        # return ((world_x, world_y, rotation_angle), [color])
                else:
                    self.cont = 0
                self.max_area = 0
                # print(color_list.index(self.color_area_max))
                color_id.append((color_list.index(self.color_area_max)+1))
                return box, (center_x, center_y), self.color_area_max,color_id , box_coordin
            if _cnt is not None and area_max > 2000:
                # drawing = cv2.drawContours(drawing, [_cnt], -1, color_value[_col], 2, 8)     # 绘制轮廓
                rect = cv2.minAreaRect(_cnt)  # 得到最小外接矩形
                # 计算中心点坐标
                box = np.int0(cv2.boxPoints(rect))
                pt1_x, pt1_y = box[0, 0], box[0, 1]
                pt2_x, pt2_y = box[2, 0], box[2, 1]
                center_x, center_y = int((pt1_x + pt2_x) / 2), int((pt1_y + pt2_y) / 2)
            # return box, (center_x, center_y), "color", color, (world_x, world_y)
        # return img


if __name__ == "__main__":
    camera = Camera(calibration_param_path="resource/camera_calibration/calibration_param.npz")
    camera.camera_open()
    camera.camera_location_flag = False

    color_rec = ColorRec()

    while True:
        img = camera.frame

        if img is not None:
            cp_img = img.copy()
            color_rec.imgRec(cp_img)
            # print(color_rec.imgRec(cp_img))

            cv2.imshow("img", cp_img)
            cv2.waitKey(10)

