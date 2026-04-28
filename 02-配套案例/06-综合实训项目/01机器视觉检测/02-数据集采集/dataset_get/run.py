import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from ui_bkrc import Ui_MainWindow
from PyQt5.QtCore import *
import addlabel
from tools.camera.search_camera import setCamera
from ai_lib.box_detect import BoxDetectRec, recImgDis
from ai_lib.components.config import ai_cfg
import cv2
import time
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.camera_open = True
        self.cap = setCamera("auto")

        self.labels = ["src",]
        self.mode = False   # False保存原始图片  True保存目标检测提取图片
        self.image = None
        self.img_write_flag = False
        self.save_num = 0

        self.box_det_rec = BoxDetectRec(ai_cfg.BOX_DET_PATH)

        self.label_28.setText("模式1：采集原始图片")

        # ---------------图像显示-----------------
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.showCamera)
        self.camera_timer.start()

        self.label_process.setScaledContents(True)   # 控制自适应图像大小

        # 绑定按键监听
        self.pushButton_addlabel.clicked.connect(self.addLabel)
        self.pushButton_deletelabel.clicked.connect(self.deleteLabel)
        self.pushButton_imgwrite.pressed.connect(lambda: self.buttonRecClicked("imgwrite"))
        self.pushButton_mode.pressed.connect(lambda: self.buttonRecClicked("mode"))

        self.comboBox_label.currentIndexChanged.connect(self.labelComboboxChange)

    def labelComboboxChange(self):
        # combobox_val = self.comboBox_label.currentText()
        self.save_num = 0

    def buttonRecClicked(self, name):
        """
        数据集采集控制按键监听
        Args:
            name: 按钮名称
        Returns: 空
        """
        if name == "imgwrite":     # 保存图像
            self.img_write_flag = True
            # self.saveImg(self.image)
        elif name == "mode":       # 数据集采集模式切换
            self.mode = not self.mode
            if self.mode:
                self.label_28.setText("模式2：采集目标检测ROI区域图片")
            else:
                self.label_28.setText("模式1：采集原始图片")

    def addLabel(self):
        # 添加标签
        self.qdi = QDialog()
        self.d = addlabel.Ui_Dialog()
        self.d.setupUi(self.qdi)
        self.qdi.show()
        self.d.pushButton_ok.clicked.connect(self.getLabel)
        self.d.pushButton_cancel.pressed.connect(self.closeqDialog)

    def deleteLabel(self):
        # 删除标签
        result = self.messageDelect('是否确认删除此类别?')
        if not result:
            label = self.comboBox_label.currentText()
            del self.labels[self.labels.index(label)]
            self.comboBox_label.clear()
            self.comboBox_label.addItems(self.labels)

    def getLabel(self):
        # 获取标签
        label = self.d.lineEdit.text()
        self.labels.append(label)
        self.comboBox_label.addItem(label)
        time.sleep(0.1)
        self.qdi.accept()

    def closeqDialog(self):
        # 关闭窗口
        self.qdi.accept()

    # 弹窗提示函数
    def messageDelect(self, string):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(' ')
        messageBox.setText(string)
        messageBox.addButton(QPushButton('确认'), QMessageBox.YesRole)
        messageBox.addButton(QPushButton('取消'), QMessageBox.NoRole)
        return messageBox.exec_()

    def saveImg(self, img):
        self.save_num += 1
        label = self.comboBox_label.currentText()
        path = "./datasets/" + label + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        cv2.imwrite(path + label + time.strftime("-%Y-%m-%d-%H-%M-%S", time.localtime()) + ".jpg", img)

    def showCamera(self):
        # 图像显示窗口
        _, frame = self.cap.read()
        if _:
            # 调整图像，进行ROI，获取分拣区域图像
            img = frame[int(frame.shape[0] / 4.9): int(frame.shape[0] - frame.shape[0] / 2.7),
                       int(frame.shape[1] / 3.7): int(frame.shape[1] - frame.shape[1] / 4.5)]

            #img = cv2.resize(img, (640, 480))
            self.image = cv2.resize(img, (640, 480))
            cv2.putText(self.image, str(self.save_num), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 0, 255), 5)
            temp_img = img.copy()
            if self.mode:
                # temp_img = img.copy()
                self.image, box_std = recImgDis(self.image, self.box_det_rec.inference(temp_img))
                if box_std["std"] != "none":
                    try:
                        box_img = box_std["roi_img"][0]
                        if self.img_write_flag:
                            self.img_write_flag = False
                            self.saveImg(box_img)
                    except:
                        pass
            else:
                if self.img_write_flag:
                    self.img_write_flag = False
                    self.saveImg(temp_img)

            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.label_process.setPixmap(QPixmap.fromImage(showImage))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())


