import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqt_ui import untitled
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QTimer
from components import color_rec
from embedded.ArmIK import Transform
import cv2
import auto_move
color_value = {'red': [0, 0, 255], 'green': [0, 255, 0], 'blue': [255, 0, 0]}

store_index = (159.7, 140.3, 5.1)  # 定义仓库坐标位置


class MainWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.ui = untitled.Ui_button_confirm_2()
        self.ui.setupUi(self)
        self.cap = cv2.VideoCapture(0)

        # 初始化
        self.init_ui()
        self.show_ = False
        self.ui.label_2.setPixmap(QPixmap("./pyqt_ui/image/uarm.jpg"))  # 在label上显示图片
        self.ui.label_2.setScaledContents(True)  # 让图片自适应label大小
        self.color_rec = color_rec.ColorRec()  # 色块识别

        self.box = None  # 图像中的色块位置
        self.box1 = None  # 图像中的色块位置

        self.trans_form = Transform.TransForm()  # 坐标映射
        self.store_index = store_index

        # 机械臂控制
        # self.Swift = Arm()
        self.Swift = auto_move.ArmServo()  # 机械臂基本控制

    def click_confirm(self):
        text_ = self.Swift.arm.get_position()
        text_[0] = round(text_[0], 1)
        text_[1] = round(text_[1], 1)
        text_[2] = round(text_[2], 1)
        self.ui.label.setText(str(text_))  # 获取当前机械臂坐标
        # print("store_index：",self.store_index)
        self.store_index = text_

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

            show = cv2.resize(cutimg, (320, 240))
            self.img_size = (320, 240)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ui.label_2.setPixmap(QPixmap.fromImage(showImage))  # 在label上显示图片
            self.ui.label_2.setScaledContents(True)  # 让图片自适应label大小
        cv2.destroyAllWindows()

    def Grab_object(self):
        if self.box is not None:
            world_x, world_y = self.world_x, self.world_y
            print("store_index1：", self.store_index)
            self.Swift.imgRecCtr(world_x, world_y, self.store_index)  # 机械臂移动
        else:
            print("erro!!!")

    def calculate_length(self):
        # 计算图像中的色块边长像素值
        lenx = 1
        leny = 1
        if self.box is not None:
            box = self.box
            lenx = abs(box[3][0]-box[2][0])
            leny = abs(box[1][1]-box[2][1])
        return (lenx,leny)

    def transform_index(self):
        text_ = "未获取到色块位置！"
        # 色块坐标映射
        if self.box is not None:
            l = self.calculate_length()
            if l[0] >= 10 and l[0] <= 200:
                print("center_x, center_y", self.center_x, self.center_y)
                self.world_x, self.world_y= self.trans_form.convertCoordinate(self.center_x, self.center_y, self.img_size)  # 坐标映射，将图像中的像素位置转换为现实世界坐标
                text_ = self.world_x, self.world_y
        else:
            print("erro!!!")
        self.ui.label_5.setText(str(text_))  # 获取当前色块坐标

    # ui初始化
    def init_ui(self):
        # 初始化方法，这里可以写按钮绑定等的一些初始函数
        self.ui.button_confirm.clicked.connect(self.click_confirm)
        self.ui.button_confirm_3.clicked.connect(self.click_arm_stop)
        self.ui.button_confirm_4.clicked.connect(self.click_arm_start)
        self.ui.button_confirm_5.clicked.connect(self.Grab_object)  # 开始分拣
        self.ui.button_confirm_6.clicked.connect(self.transform_index)  # 色块坐标映射
        self.ui.showimg.clicked.connect(self.show_image)
        self.show()


if __name__ == '__main__':
    e = MainWindow()
    sys.exit(e.app.exec())
