from components.tflite_infer import TfliteRun
from components.config import ai_cfg
from components.utils import putText
import numpy as np
import cv2

FRUITS_MODEL_PATH = "./resource/model_zoo/pt_fruits.tflite"
MAP_PARAM_PATH = "./tools/CameraCalibration/map_param.npz"


class ChineseDetect(object):
    def __init__(self, model_path=FRUITS_MODEL_PATH):
        self.tflite_run = TfliteRun(model_path=model_path)  # 模型推理
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
                if dat in ["ldentify", "quantity"]:
                    dat_index = 0
                elif dat in ["中国", "China"]:
                    dat_index = 1
                elif dat in ["百科荣创"]:
                    dat_index = 2
                elif dat in ["人工智能"]:
                    dat_index = 3
                else:
                    dat_index = -1

                predictions = [dat, dat_index]
            else:
                predictions = ["", -1]
        return predictions


# 解析并显示识别结果
def recImgDis(img, predictions):
    dat = 0
    print(predictions)
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
        # print("tim:", (time.time() - s) * 1000)
        img, label = recImgDis(img, fruit_detect_pricet)

        cv2.imshow("fruit_img", img)
        cv2.waitKey(10)
