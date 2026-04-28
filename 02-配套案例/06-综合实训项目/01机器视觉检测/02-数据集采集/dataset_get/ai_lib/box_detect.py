from ai_lib.components.tflite_infer import TfliteRun
from ai_lib.components.prior_box import priors_box, parse_predict
from ai_lib.components.config import ai_cfg
from tools.camera.search_camera import setCamera
import numpy as np
import cv2
import time

BOX_DET_PATH = "../resource/model_zoo/box_160x120.tflite"

class BoxDetectRec(object):
    def __init__(self, box_det_path=BOX_DET_PATH):
        self.tflite_run = TfliteRun(model_path=box_det_path)
        self.priors, _ = priors_box(image_sizes=ai_cfg.BOX_INPUT_SIZE)
        # priors = priors.astype(np.float16)

        self.img_width = ai_cfg.CAM_WIDTH
        self.img_height = ai_cfg.CAM_HEIGHT

    def imgPreprocessing(self, img):
        img = np.float32(img.copy())
        img = cv2.resize(img, (ai_cfg.BOX_INPUT_SIZE[1], ai_cfg.BOX_INPUT_SIZE[0]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0 - 0.5
        input_data = img[np.newaxis, ...]
        return input_data

    def inference(self, img):
        input_data = self.imgPreprocessing(img)
        net_outs = self.tflite_run.inference(input_data)
        boxes, classes, scores = parse_predict(net_outs, self.priors, ai_cfg.BOX_CLASSES)
        boxs_centre = []    # box中心点坐标
        boxs = []           # box检测框
        box_index = []      # box识别结果索引
        box_label = []      # box识别结果
        roi_img = []        # box区域图片

        for prior_index in range(len(classes)):
            x1, y1, x2, y2 = int(boxes[prior_index][0] * self.img_width) + int(self.img_width * 0.02), \
                             int(boxes[prior_index][1] * self.img_height), \
                             int(boxes[prior_index][2] * self.img_width) - int(self.img_width * 0.02), \
                             int(boxes[prior_index][3] * self.img_height)

            x = int(x1 + abs(x2 - x1) / 2)
            y = int(y1 + abs(y2 - y1) / 2)
            boxs_centre.append((x, y))
            boxs.append((x1, y1, x2, y2))
            img_copy = img.copy()
            box_roi = img_copy[int(y1):int(y2), int(x1):int(x2)]  # 提取ROI
            roi_img.append(box_roi)

        boxs.sort()  # 排序
        boxs_centre.sort()

        self.predictions = [boxs, boxs_centre, box_label, box_index, roi_img]
        return self.predictions

def recImgDis(img, predictions):
    box_std= {"std": "none"}
    if predictions:
        boxs, boxs_centre, box_label, box_index, roi_img = predictions
        print("----", box_label,"\n", box_index)

        for i, box in enumerate(boxs):
            x1, y1, x2, y2 = box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(img, boxs_centre[i], 1, (0, 0, 255), 2)
            # if box_index and len(boxs) == len(box_index):
            #     img = putText(img, '{} {}'.format(box_label[i], box_index[i]), (x1, y1 - 4))
            #     cv2.imshow("img" + str(i), roi_img[i])

        box_std = {"std": "true", "boxs": boxs, "boxs_centre": boxs_centre,
                   "box_index": box_index, "roi_img": roi_img}

    return img, box_std

if __name__ == "__main__":
    cap = setCamera("auto")
    box_det_rec = BoxDetectRec()

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (640, 480))
        img = cv2.flip(img, 1, dst=None)  # 水平镜像
        img = cv2.flip(img, 0, dst=None)  # 垂直镜像
        st = time.time()
        box_pricet = box_det_rec.inference(img)
        img, box_std = recImgDis(img, box_pricet)

        if box_std["std"] != "none":

            try:
                box_img = box_std["roi_img"][0]
                print("roi:", type(box_img), box_img)
                cv2.imshow("s", box_img)
            except:
                pass

        cv2.imshow("img", img)
        cv2.waitKey(5)
