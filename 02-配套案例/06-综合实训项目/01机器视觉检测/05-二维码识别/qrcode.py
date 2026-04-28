import cv2
import numpy as np

# 构造二维码识别对象
detector = cv2.QRCodeDetector()
# 读取输入图像
img = cv2.imread("./test_img/qr_test.png")
# 检测并识别
res, points,code = detector.detectAndDecode(img)
print(res, points, code)
if points is not  None:
    # 绘制二维码所在位置
    cv2.drawContours(img,[np.int32(points)],0,(0,0,255),2)
# 显示图像
cv2.imshow('img',img)
cv2.waitKey(0)
