from components.utils import getFaceBoxs, putText
from components.tflite_infer import TfliteRun
from components.prior_box import priors_box, parse_predict
from Chinese_Rec import ChineseDetect
from components.config import ai_cfg
from embedded.ArmIK.Transform import TransForm
from tools.camera.search_camera import setCamera
import numpy as np
import cv2
import time

BOX_DET_PATH = "./resource/model_zoo/box_160x120.tflite"
MAP_PARAM_PATH = "./resource/camera_calibration/map_param.npz"


class BoxDetectRec(object):
    def __init__(self, box_det_path=BOX_DET_PATH, map_param_path=MAP_PARAM_PATH):
        self.tflite_run = TfliteRun(model_path=box_det_path)

        # 目标检测先验框
        self.priors, _ = priors_box(image_sizes=ai_cfg.BOX_INPUT_SIZE)

        # 坐标映射
        self.trans_form = TransForm(map_param_path=map_param_path)

        # 文字识别
        self.electron_rec = ChineseDetect(model_path=ai_cfg.FRUIT_REC_PATH)

        self.img_width = ai_cfg.CAM_WIDTH
        self.img_height = ai_cfg.CAM_HEIGHT

    def adjust(self, img, boxs):
        # 摄像头位置校准函数
        std = False
        if boxs and len(boxs) < 2:
            h, w = img.shape[:2]
            x1, y1, x2, y2 = 320 - 48, 240 - 48, 320 + 48, 240 + 48
            cv2.line(img, (0, int(h / 2)), (w, int(h / 2)), (0, 0, 255), 2)
            cv2.line(img, (int(w / 2), 0), (int(w / 2), h), (0, 0, 255), 2)

            box = boxs[0]

            if abs(x1-box[0]) < 5 and abs(y1-box[1]) < 5 and abs(x2-box[2]) < 5 and abs(y2-box[3]) < 5:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                std = True
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return img, std

    def imgPreprocessing(self, img):
        # 输入数据预处理函数
        img = np.float32(img.copy())
        img = cv2.resize(img, (ai_cfg.BOX_INPUT_SIZE[1], ai_cfg.BOX_INPUT_SIZE[0]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0 - 0.5
        input_data = img[np.newaxis, ...]
        return input_data

    def inference(self, img, img_rec=False, img_mode=0):
        input_data = self.imgPreprocessing(img)
        s = time.time()
        net_outs = self.tflite_run.inference(input_data)
        # print("infer:", (time.time() - s) * 1000)
        boxes, classes, scores = parse_predict(net_outs, self.priors, ai_cfg.BOX_CLASSES)
        boxs_centre = []    # box中心点坐标
        boxs = []           # box检测框
        box_index = []      # box识别结果索引
        box_label = []      # box识别结果
        box_coordin = []    # box实际坐标映射+旋转角
        roi_img = []        # box区域图片

        for prior_index in range(len(classes)):
            x1, y1, x2, y2 = int(boxes[prior_index][0] * self.img_width) + int(self.img_width * 0.02), \
                             int(boxes[prior_index][1] * self.img_height), \
                             int(boxes[prior_index][2] * self.img_width) - int(self.img_width * 0.02),\
                             int(boxes[prior_index][3] * self.img_height)

            # print("x1-x2:{}y1-y2:{},x-y:{}".format(abs(x1 - x2), abs(y1 - y2), abs(x1 - x2)- abs(y1 - y2)))
            if abs(x1-x2) < 186 and abs(abs(x1 - x2)-abs(y1 - y2)) < 28:
                # 过滤异常检测到的物体
                x = int(x1 + abs(x2 - x1) / 2)
                y = int(y1 + abs(y2 - y1) / 2)
                boxs_centre.append((x, y))
                boxs.append((x1, y1, x2, y2))

        # 排序
        boxs.sort()
        boxs_centre.sort()
        for i, box in enumerate(boxs):
            if i > 3:
                break
            x1, y1, x2, y2 = box
            try:
                img_copy = img.copy()
                box_roi = img_copy[int(y1):int(y2), int(x1):int(x2)]  # 提取ROI
                if img_rec:
                    imclass, imgindex = self.electron_rec.inference(box_roi, auto=True)  # 识别
                    box_label.append(imclass)
                    box_index.append(imgindex)

                coord = self.trans_form.getCoordinate(box_roi, *boxs_centre[i])  # box实际坐标映射
                if coord[0] != None:
                    box_coordin.append(coord)
                roi_img.append(box_roi)
            except:
                print("---------------------------------------")
                pass

        self.predictions = [boxs, boxs_centre, box_label, box_index, box_coordin,  roi_img]
        return self.predictions


def recImgDis(img, predictions):
    box_std = {"std": "none"}
    if predictions:
        boxs, boxs_centre, box_label, box_index, box_coordin, roi_img = predictions
        # print("----", box_label,"\n", box_index)

        for i, box in enumerate(boxs):
            x1, y1, x2, y2 = box
            print("box:", box)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(img, boxs_centre[i], 1, (0, 0, 255), 2)

            print("len(box_index):", len(box_index))
            if box_index and len(boxs) == len(box_index):
                img = putText(img, '{} {}'.format(box_label[i], box_index[i]), (x1, y1 - 4))
                # cv2.imshow("img" + str(i), roi_img[i])

        box_std = {"std": "true", "boxs": boxs, "boxs_centre": boxs_centre,
                   "box_index": box_index, "box_coordin": box_coordin, "box_label": box_label}

    return img, box_std


if __name__ == "__main__":
    import multiprocessing as mp
    from embedded.auto_move import ArmServo

    cap = setCamera("auto")

    box_det_rec = BoxDetectRec()     # 检测与识别，坐标映射
    arm_servo = ArmServo()  # 机械臂控制

    count = 0

    while True:
        ret, frame = cap.read()
        #frame = cv2.resize(img, (640, 480))
        # 调整图像，进行ROI，获取分拣区域图像
        img = frame[int(frame.shape[0] / 4.6): int(frame.shape[0] - frame.shape[0] / 2.7),
                   int(frame.shape[1] / 3.4): int(frame.shape[1] - frame.shape[1] / 4.5)]

        img = cv2.resize(img, (640, 480))

        st = time.time()
        box_pricet = box_det_rec.inference(img, True, img_mode=2)  # 待识别物体检测
        img, box_std = recImgDis(img, box_pricet)   # 检测框绘制

        box_det_rec.adjust(img, box_std['boxs'])   # 摄像头位置校准

        # print(box_std["boxs"])

        if box_std["std"] != "none":
            if box_std["box_coordin"] and box_std["box_index"][0] != -1:
                count += 1
                if count > 30:
                    count = 0
                    print("--物体稳定状态！！")
                    print( box_std["box_coordin"])
                    arm_servo.imgRecCtr(box_std["box_coordin"], box_std['box_index'])  # 机械臂抓取
            else:
                count = 0
            # print(box_std["box_index"])
        cv2.imshow("chinese_detect", img)
        cv2.waitKey(1)
