from ai_lib.components.tflite_infer import TfliteRun
from ai_lib.components.config import ai_cfg
from ai_lib.components.utils import putText
from embedded.ArmIK.Transform import TransForm
from tools.log import log
import numpy as np
import cv2
import math

FRUITS_MODEL_PATH = "../resource/model_zoo/pt_fruits.tflite"
MAP_PARAM_PATH = "../tools/CameraCalibration/map_param.npz"

class FruitDetect(object):
    def __init__(self, model_path=FRUITS_MODEL_PATH):
        self.tflite_run = TfliteRun(model_path=model_path)  # 模型推理
        # self.trans_form = TransForm(map_param_path=map_param_path)
        self.predictions = []

    # 模型输入数据预处理
    def imgPreprocessing(self, img):
        input_data = cv2.resize(img, ai_cfg.REC_INPUT_SIZE)
        input_data = np.float32(input_data.copy())
        input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)
        input_data = input_data / 255.0 - 0.5
        input_data = input_data[np.newaxis, ...]
        return input_data

    # 模型推理
    def inference(self, img, auto=False):
        input_data = self.imgPreprocessing(img)              # 获取测试图像
        predictions = self.tflite_run.inference(input_data)  # 模型推理
        if auto:
            socr = predictions[0][np.argmax(predictions)]
            if socr > ai_cfg.DIS_THR:
                dat = ai_cfg.FRUITS_LABEL[np.argmax(predictions)]

                # label_1 = ["鸡", "苹果", "白菜", "福特", "中国", "ldentify"]
                # label_2 = ["狗", "芒果", "洋葱", "别克", "百科荣创", "quantity"]
                # label_3 = ["牛", "石榴", "西兰花", "宝马", "人工智能", "China"]
                if dat == '苹果':
                    dat_index = 0
                elif dat == '芒果':
                    dat_index = 0
                elif dat == '洋葱':
                    dat_index = 1
                elif dat == '西兰花':
                    dat_index = 2
                else:
                    dat_index = -1

                predictions = [dat, dat_index]
            else:
                predictions = ["", -1]
        return predictions


 # # 找出面积最大的轮廓
    # # 参数为要比较的轮廓的列表
    # def getAreaMaxContour(self, contours):
    #     contour_area_temp = 0
    #     contour_area_max = 0
    #     area_max_contour = None
    #
    #     for c in contours:  # 历遍所有轮廓
    #         contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
    #         if contour_area_temp > contour_area_max:
    #             contour_area_max = contour_area_temp
    #             if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
    #                 area_max_contour = c
    #     return area_max_contour, contour_area_max  # 返回最大的轮廓

    # def getCoordinate(self, img, img_centerx, img_centery):
    #     # print("centery:", img_centery, img_centerx)
    #     max_area = 0
    #     size = (640, 480)
    #     world_x = world_y = rotation_angle = None
    #     buf_img = img.copy()
    #     src_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     _, src_img = cv2.threshold(src_img, 100, 255, cv2.THRESH_BINARY)
    #     # cv2.imshow("i", src_img)
    #     opened = cv2.morphologyEx(src_img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
    #     closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
    #     # cv2.imshow("closed", closed)
    #     contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
    #     areaMaxContour, area_max = self.getAreaMaxContour(contours)  # 找出最大轮廓
    #
    #     if areaMaxContour is not None:
    #         # print("--max_area:", area_max)
    #         if area_max > 2500:  # 有找到最大面积
    #             rect = cv2.minAreaRect(areaMaxContour)
    #             rotation_angle = rect[2]
    #             box = np.int0(cv2.boxPoints(rect))
    #             cv2.drawContours(buf_img, [box], -1, (0, 255, 0), 2)
    #             # cv2.imshow("buf_img", buf_img)
    #             world_x, world_y = self.trans_form.convertCoordinate(img_centerx, img_centery, size)  # 转换为现实世界坐标
    #
    #     return (world_x, world_y, rotation_angle)

# 解析并显示识别结果
def recImgDis(img, predictions):
    dat = 0
    if not predictions is None:
        socr = predictions[0][np.argmax(predictions)]
        if socr > 0.85:
            dat = ai_cfg.FRUITS_LABEL[np.argmax(predictions)]
            img = putText(img, "{} {:.2f}".format(dat, socr), org=(0, 0))  # 结果绘制

    return img, dat

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    fruit_detect = FruitDetect()
    import time

    while True:
        ret, frame = cap.read()
        img = cv2.resize(frame, (640, 480))
        s = time.time()
        fruit_detect_pricet = fruit_detect.inference(img)
        print("tim:", (time.time() - s) * 1000)
        img, label = recImgDis(img, fruit_detect_pricet)

        log.info(label)

        cv2.imshow("fruit_img", img)
        cv2.waitKey(10)
