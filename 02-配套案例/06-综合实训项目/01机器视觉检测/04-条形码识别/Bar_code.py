import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pyzbar.pyzbar as pyzbar


def PIL_putText(img, text, x, y, color=(255, 0, 0)):
    frame = img
    # PIL图片上打印汉字
    font = ImageFont.truetype("./font/simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    draw.text((x, y - 10), text, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    # PIL图片转cv2 图片
    frame = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return frame


def code_detection(img):
    frame = img
    center_x, center_y = 0, 0
    barcodeData = ''
    barcodeData1 = ''
    barcodeType = ''
   # 判断摄像头是否初始化并成功打开
    if img is not None:
        # 把输入图像灰度化
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 转换灰度图
        # 获取自适配阈值
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        barcodes = pyzbar.decode(binary)      # 使用pyzbar检测图像中的条码、二维码
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            # PIL图片上打印汉字
            frame = PIL_putText(frame, text, x, y-10, (255, 0, 0))
            cv2.circle(frame, (int(x + w/2), int(y + h/2)), 2, (255, 255, 0), 2, cv2.LINE_AA)
            if barcodeData == '' or barcodeData != barcodeData1:
                barcodeData1 = barcodeData
                center_x, center_y = (int(x + w / 2), int(y + h / 2))
                # print("Recognize result>>> type： {0}  content： {1}".format(barcodeType, barcodeData))
            else:
                pass
        # cv2.imshow('image', frame)  # 显示图像帧
        barcodeData = "type： {0}  content： {1}".format(barcodeType, barcodeData)
    return frame, barcodeData,  center_x, center_y



if __name__ == "__main__":
    img = cv2.imread("./1.png")
    img = cv2.resize(img, (int(img.shape[0:2][1]/4), int(img.shape[0:2][0]/4)))
    frame, barcodeData, center_x, center_y = code_detection(img)
    print(barcodeData)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    # # # 摄像头识别
    # cap = cv2.VideoCapture(0)
    # while True:
    #     _, img = cap.read()
    #     if _:
    #         frame, barcodeData,  center_x, center_y = code_detection(img)
    #         print(barcodeData)
    #         cv2.imshow('img', img)
    #
    #     k = cv2.waitKey(25)  # 每25ms读取一次键盘按键，同时控制帧率
    #     if k == ord('q'):  # 当检测到键盘q键按下，程序退出
    #         break


