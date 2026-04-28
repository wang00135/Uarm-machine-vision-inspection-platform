import numpy as np
import cv2
import time
from components.tflite_infer import TfliteRun
from components.config import ai_cfg
from components.utils import putText

class ElectronRec(object):
    def __init__(self, model_path):
        self.tflite_run = TfliteRun(model_path=model_path)

    # 模型输入数据预处理
    def imgPreprocessing(self, img):
        input_data = cv2.resize(img, (224, 224))
        input_data = np.float32(input_data.copy())
        input_data = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)
        input_data = input_data / 255.0
        input_data = input_data[np.newaxis, ...]
        return input_data

    # 模型推理
    def inference(self, img, auto=False):
        input_data = self.imgPreprocessing(img)              # 获取测试图像
        predictions = self.tflite_run.inference(input_data)  # 模型推理
        if auto:
            socr = predictions[0][np.argmax(predictions)]
            if socr > 0.65:
                dat = ai_cfg.ELECTRONIC_LABELS[np.argmax(predictions)]
                print(dat)

                if dat == '电阻':
                    dat_index = 0
                elif dat == '电感':
                    dat_index = 1
                elif dat == '电容':
                    dat_index = 2
                elif dat == '开关':
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
    if not predictions is None:
        socr = predictions[0][np.argmax(predictions)]
        if socr > 0.85:
            dat = ai_cfg.ELECTRONIC_LABELS[np.argmax(predictions)]
            img = putText(img, "{} {:.2f}".format(dat, socr), org=(0, 0))  # 结果绘制

    return img, dat


if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    comm_rec = ElectronRec("electronic_model.tflite")

    while True:
        _, frame = capture.read()
        if frame is None:
            print('No camera found')

        start = time.time()
        y_pred = comm_rec.inference(frame, True)

        frame = putText(frame, ai_cfg.ELECTRONIC_LABELS[np.argmax(y_pred)], org=(0, 0))

        fps_str = "FPS: %.2f" % (1 / (time.time() - start))
        print((time.time() - start) * 1000)
        cv2.putText(frame, fps_str, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 2)
        frame = cv2.resize(frame, (320, 280))
        cv2.imshow('frame', frame)
        cv2.moveWindow("frame", 0, 0)
        if cv2.waitKey(1) == ord('q'):
            exit()