import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqt_ui import untitled
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QTimer
from embedded.arm import Arm
from components import color_rec
from embedded.ArmIK import Transform
from tools.camera.camera import Camera
import cv2
from PIL import ImageFont, ImageDraw, Image
color_value = {'red': [0, 0, 255], 'green': [0, 255, 0], 'blue': [255, 0, 0]}


class MainWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.ui = untitled.Ui_button_confirm_2()
        self.ui.setupUi(self)
        self.cap = cv2.VideoCapture(0)
        self.color_rec = color_rec.ColorRec()

        # 初始化
        self.init_ui()
        self.show_ = False
        self.ui.label_2.setPixmap(QPixmap("./pyqt_ui/image/uarm.jpg"))  # 在label上显示图片
        self.ui.label_2.setScaledContents(True)  # 让图片自适应label大小

        self.box = None  # 图像中的色块位置
        self.box1 = None  # 图像中的色块位置

        self.trans_form = Transform.TransForm()  # 坐标映射

        # 机械臂控制
        self.Swift = Arm()

    def click_confirm(self):
        text_ = self.Swift.arm.get_position()
        text_[0] = round(text_[0], 1)
        text_[1] = round(text_[1], 1)
        text_[2] = round(text_[2], 1)
        self.ui.label.setText(str(text_))  # 获取当前机械臂坐标
        print(self.ui.label.text())

    def click_arm_stop(self):
        self.Swift.Arm_Set_servo_detach()  # 机械臂掉电

    def click_arm_start(self):
        self.Swift.Arm_Set_servo_attach()  # 机械臂上电

    def show_image(self):
        if self.show_ == False:
            self.show_ = True
            # ---------------图像显示-----------------
            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.get_img)
            self.camera_timer.start()
        else:
            self.show_ = False
            self.camera_timer.stop()
            self.ui.label_2.setPixmap(QPixmap("./pyqt_ui/image/uarm.jpg"))  # 在label上显示图片
            self.ui.label_2.setScaledContents(True)  # 让图片自适应label大小

    def get_img(self):
        _, img = self.cap.read()
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 调整图像，进行ROI，获取分拣区域图像
            cutimg = img[int(img.shape[0] / 4.6): int(img.shape[0] - img.shape[0] / 2.7),
                       int(img.shape[1] / 3.4): int(img.shape[1] - img.shape[1] / 4.5)]
            cutimg = cv2.resize(cutimg, (320, 240))
            # 颜色识别
            self.box, _col, self.center_x, self.center_y = self.color_rec.imgRec(cutimg)
            if self.box is not None:
                cv2.circle(cutimg, (self.center_x, self.center_y), 2, color_value[_col], 2)  # 绘制中心点

            # 结果显示
            show = cv2.resize(cutimg, (320, 240))
            self.img_size = (320, 240)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ui.label_2.setPixmap(QPixmap.fromImage(showImage))  # 在label上显示图片
            self.ui.label_2.setScaledContents(True)  # 让图片自适应label大小
        cv2.destroyAllWindows()

    def get_img_index(self):
        # print("box：",self.box)
        # print((self.center_x, self.center_y))
        if self.box is not None:
            self.box1, self.center_x1, self.center_y1 = self.box, self.center_x, self.center_y
            text_ = self.center_x1, self.center_y1
            # self.ui.label_4.setText(str(text_))  # 获取当前色块坐标
        else:
            text_ = "未获取到色块位置！"
            print("erro!!!")
        self.ui.label_4.setText(str(text_))  # 获取当前色块坐标

    def calculate_length(self):
        # 计算图像中的色块边长像素值
        box = self.box1
        lenx = abs(box[3][0]-box[2][0])
        leny = abs(box[1][1]-box[2][1])
        return (lenx, leny)

    def transform_index(self):
        if self.box1 is not None:
            world_x, world_y = self.trans_form.convertCoordinate(self.center_x1, self.center_y1, self.img_size)  # 坐标映射，将图像中的像素位置转换为现实世界坐标
            text_ = world_x, world_y
        else:
            text_ = "请先获取色块位置！"
            print("erro!!!")
        self.ui.label_5.setText(str(text_))  # 获取当前色块坐标映射

    # ui初始化
    def init_ui(self):
        # 初始化方法，这里可以写按钮绑定等的一些初始函数
        self.ui.button_confirm.clicked.connect(self.click_confirm)
        self.ui.button_confirm_3.clicked.connect(self.click_arm_stop)
        self.ui.button_confirm_4.clicked.connect(self.click_arm_start)
        self.ui.button_confirm_5.clicked.connect(self.get_img_index)
        self.ui.button_confirm_6.clicked.connect(self.transform_index)
        self.ui.showimg.clicked.connect(self.show_image)
        self.show()


if __name__ == '__main__':
    e = MainWindow()
    sys.exit(e.app.exec())
