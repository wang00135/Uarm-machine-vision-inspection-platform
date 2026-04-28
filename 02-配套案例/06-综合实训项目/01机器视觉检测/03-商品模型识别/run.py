import numpy as np
# import tensorflow as tf
import tflite_runtime.interpreter as tflite
import cv2
import time
from PIL import ImageFont, ImageDraw, Image
import config as config

cfg = config.cfg

class TfliteRun:
    def __init__(self):
        # 读取模型
        self.interpreter = tflite.Interpreter(model_path=cfg["tflite_model_path"])

        # 分配张量
        self.interpreter.allocate_tensors()

    def inference(self, img):
        # 获取输入层和输出层维度
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # print("input_details", input_details)
        # print("output_datalis", output_details)

        # 设置输入数据
        input_shape = input_details[0]['shape']

        input_data = img
        self.interpreter.set_tensor(input_details[0]['index'], input_data)
        self.interpreter.invoke()     # 推理
        output_data = self.interpreter.get_tensor(output_details[0]['index'])    # 获取输出层数据
        return output_data

font_path = 'simsun.ttc'

# 在图像中显示中文
def putText(img, text, org=(0, 0), color=(0, 0, 255), font_size=80):
    font = ImageFont.truetype(font_path, font_size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(org, text, fill=color, font=font)
    img = np.array(img_pil)
    return img

capture = cv2.VideoCapture(cfg["camera_id"])
start = time.time()
model = TfliteRun()

while True:
    _, frame = capture.read()
    if frame is None:
        print('No camera found')
    # 调整图像，进行ROI，获取分拣区域图像
    catframe = frame[int(frame.shape[0] / 4.6): int(frame.shape[0] - frame.shape[0] / 2.7),
               int(frame.shape[1] / 3.4): int(frame.shape[1] - frame.shape[1] / 4.5)]

    size = catframe.shape[0:2]
    img = cv2.resize(catframe, (224, 224))
    img = np.float32(img.copy())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img / 255.0
    img = img[np.newaxis, ...]

    start = time.time()
    y_pred = model.inference(img)  # 图像分类

    catframe = putText(catframe, cfg["labels_list"][np.argmax(y_pred)], org=(0, 0))

    # fps_str = "FPS: %.2f" % (1 / (time.time() - start))
    # print((time.time() - start) * 1000)
    # cv2.putText(frame, fps_str, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 2)
    catframe = cv2.resize(catframe, (int(size[1]*2), int(size[0])*2))
    cv2.imshow('frame', catframe)
    cv2.moveWindow("frame", 0, 0)
    if cv2.waitKey(1) == ord('q'):
        exit()
