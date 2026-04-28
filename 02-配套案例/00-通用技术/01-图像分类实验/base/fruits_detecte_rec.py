from base.components.tflite_infer import TfliteRun
from base.components.config import ai_cfg
from base.components.utils import putText
from tools.log import log
import numpy as np
import cv2

FRUITS_MODEL_PATH = "../resource/model_zoo/fruits_veges_fake_model.tflite"

class FruitDetect(object):
    def __init__(self, model_path=FRUITS_MODEL_PATH):
        self.tflite_run = TfliteRun(model_path=model_path)  # 模型推理
        self.predictions = []

    # 模型输入数据预处理
    def imgPreprocessing(self, img):
        input_data = cv2.resize(img, ai_cfg.INPUT_SIZE)
        input_data = np.float32(input_data.copy())
        input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)
        input_data = input_data / 255.0 - 0.5
        input_data = input_data[np.newaxis, ...]
        return input_data

    # 模型推理
    def inference(self, img):
        input_data = self.imgPreprocessing(img)              # 获取测试图像
        predictions = self.tflite_run.inference(input_data)  # 模型推理
        return predictions

# 解析并显示识别结果
def recImgDis(img, predictions):
    dat = ""
    m = 0
    if not predictions is None:
        dat = ai_cfg.FRUITS_LABEL[np.argmax(predictions)]
        m = ai_cfg.FRUITS_M[np.argmax(predictions)]
        img = putText(img, dat, org=(0, 0))  # 结果绘制

    return img, (dat, m)

if __name__ == "__main__":
    img = cv2.imread("../resource/image_test/pineapple.jpeg")

    cap = cv2.VideoCapture(0)
    fruit_detect = FruitDetect()

    while True:
        ret, frame = cap.read()
        img = cv2.resize(frame, (640, 480))

        fruit_detect_pricet = fruit_detect.inference(img)
        img, label = recImgDis(img, fruit_detect_pricet)

        log.info(label)

        cv2.imshow("fruit_img", img)
        cv2.waitKey(10)
