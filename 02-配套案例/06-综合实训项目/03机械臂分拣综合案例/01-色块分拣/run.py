from color_rec import ColorRec
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
        # self.tflite_run = TfliteRun(model_path=box_det_path)

        # 目标检测先验框
        # self.priors, _ = priors_box(image_sizes=ai_cfg.BOX_INPUT_SIZE)

        # 色块识别
        self.colorrec = ColorRec()

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

    def recImgDis(self, img):
        predictions = self.colorrec.imgRec(img)
        # print("predictions:",predictions)
        box_std = {"std": "none"}
        if predictions:
            boxs, boxs_centre, box_label, box_index, box_coordin = predictions
            box_std = {"std": "true", "boxs": boxs, "boxs_centre": boxs_centre,
                       "box_index": box_index, "box_coordin": box_coordin, "box_label": box_label}

        return img, box_std


if __name__ == "__main__":
    import multiprocessing as mp
    from embedded import auto_move

    cap = setCamera("auto")

    box_det_rec = BoxDetectRec()     # 检测与识别，坐标映射
    arm_servo = auto_move.ArmServo()  # 机械臂控制

    count = 0
    bo = []
    while True:
        ret, frame = cap.read()
        # 调整图像，进行ROI，获取分拣区域图像
        img = frame[int(frame.shape[0] / 4.6): int(frame.shape[0] - frame.shape[0] / 2.7),
                   int(frame.shape[1] / 3.4): int(frame.shape[1] - frame.shape[1] / 4.5)]

        img = cv2.resize(img, (640, 480))
        st = time.time()
        img, box_std = box_det_rec.recImgDis(img)   # 检测框绘制
        dvalue = 10
        if box_std["std"] == "true":
            bo.append(box_std["box_coordin"][0][0])
            if len(bo)>=2:
                dvalue = abs(bo[len(bo)-1]*10 - bo[len(bo)-2]*10)
            if box_std["box_coordin"] and dvalue<=5:
                count += 1
                if count > 70:
                    count = 0
                    print("--物体稳定状态！！")
                    print(box_std["box_coordin"][0])
                    arm_servo.imgRecCtr(box_std["box_coordin"], box_std['box_index'])  # 机械臂抓取
                    bo = []
            else:
                count = 0
            # print(box_std["box_index"])
        cv2.imshow("face_detect", img)
        cv2.waitKey(1)
