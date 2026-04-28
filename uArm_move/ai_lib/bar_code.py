import cv2
import numpy as np
from pyzbar.pyzbar import decode

# 导入图片
# img = cv2.imread('QR.jpg')

# 通过摄像头识别图片
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        print(barcode.data)
        myData = barcode.data.decode('utf-8')
        print(myData)
        # 条形码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # 字体颜色（rgb)
        myColour = (0, 255, 0)

        # 输出内容
        myOutPut = barcodeData
        # 需要先把输出的中文字符转换成Unicode编码形式(  str.decode("utf-8)   )

        # 添加方框
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColour, 5)

        # 添加文本
        pts2 = barcode.rect
        cv2.putText(img, myOutPut, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColour, 2)

    cv2.imshow("Result", img)
    cv2.waitKey(1)