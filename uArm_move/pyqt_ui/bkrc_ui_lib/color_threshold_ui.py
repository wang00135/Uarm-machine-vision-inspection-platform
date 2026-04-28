from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqt_ui.bkrc_ui_lib.ui_bkrc import Ui_MainWindow
from pyqt_ui.bkrc_ui_lib import addcolor
from tools.config import config as cfg
from PyQt5.QtCore import *
import cv2
import yaml
import os
import time

class ColorThresholdUi(object):
    def __init__(self, ui: Ui_MainWindow, message, full_dict=None):
        self.ui = ui
        self.messageFrom = message
        self.full_dict = full_dict

        self.lab_file = './resource/lab_config.yaml'
        self.color = 'red'
        self.kernel_open = 3
        self.kernel_close = 3
        self.camera_ui = False

        # ---------------图像显示-----------------
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.showCamera)
        self.ui.label_process.setScaledContents(True)  # 控件自适应图像大小

        # 绑定滑动条监听
        self.ui.horizontalSlider_LMin.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('lmin'))
        self.ui.horizontalSlider_AMin.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('amin'))
        self.ui.horizontalSlider_BMin.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('bmin'))
        self.ui.horizontalSlider_LMax.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('lmax'))
        self.ui.horizontalSlider_AMax.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('amax'))
        self.ui.horizontalSlider_BMax.valueChanged.connect(lambda: self.horizontalSlider_labvaluechange('bmax'))

        # 绑定按键监听
        self.ui.pushButton_labWrite.pressed.connect(lambda: self.buttonRecClicked('labWrite'))
        self.ui.pushButton_addcolor.clicked.connect(self.addcolor)
        self.ui.pushButton_deletecolor.clicked.connect(self.deletecolor)
        self.ui.color_switch_button.clicked.connect(lambda: self.buttonRecClicked('color_switch_button'))

        self.createConfig()

    def buttonRecClicked(self, name):
        """
        摄像头控制按键监听
        Args:
            name: 按钮名称
        Returns: 空
        """
        if name == 'labWrite':
            try:
                self.save_yaml_data(self.current_lab_data, self.lab_file)
            except Exception as e:
                print('保存失败！')
                return
            print('保存成功！')

        if name == 'color_switch_button':
            self.camera_ui = not self.camera_ui
            if self.camera_ui:
                self.ui.color_switch_button.setText('开启')
                self.camera_timer.start()
            else:
                self.ui.color_switch_button.setText('关闭')
                self.camera_timer.stop()


    def showCamera(self):
        # 图像显示窗口
        img = self.full_dict[cfg.ORIGINAL_IMAGE]
        if img is not None:
            orgFrame = cv2.GaussianBlur(img, (3, 3), 3)
            frame_lab = cv2.cvtColor(orgFrame, cv2.COLOR_BGR2LAB)
            frame_lab = cv2.resize(frame_lab, (320, 240))
            mask = cv2.inRange(frame_lab,
                               (self.current_lab_data[self.color]['min'][0],
                                          self.current_lab_data[self.color]['min'][1],
                                          self.current_lab_data[self.color]['min'][2]),
                               (self.current_lab_data[self.color]['max'][0],
                                self.current_lab_data[self.color]['max'][1],
                                self.current_lab_data[self.color]['max'][2]))  # 对原图像和掩模进行位运算

            opend = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                                     cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_open, self.kernel_open)))
            closed = cv2.morphologyEx(opend, cv2.MORPH_CLOSE,
                                      cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_close, self.kernel_close)))

            closed = cv2.bitwise_not(closed)
            showImage = QImage(closed.data, closed.shape[1], closed.shape[0], QImage.Format_Indexed8)
            temp_pixmap = QPixmap.fromImage(showImage)
            self.ui.label_process.setPixmap(temp_pixmap)

    def horizontalSlider_labvaluechange(self, name):
        if name == 'lmin':
            self.current_lab_data[self.color]['min'][0] = self.ui.horizontalSlider_LMin.value()
            self.ui.label_LMin.setNum(self.current_lab_data[self.color]['min'][0])
        if name == 'amin':
            self.current_lab_data[self.color]['min'][1] = self.ui.horizontalSlider_AMin.value()
            self.ui.label_AMin.setNum(self.current_lab_data[self.color]['min'][1])
        if name == 'bmin':
            self.current_lab_data[self.color]['min'][2] = self.ui.horizontalSlider_BMin.value()
            self.ui.label_BMin.setNum(self.current_lab_data[self.color]['min'][2])
        if name == 'lmax':
            self.current_lab_data[self.color]['max'][0] = self.ui.horizontalSlider_LMax.value()
            self.ui.label_LMax.setNum(self.current_lab_data[self.color]['max'][0])
        if name == 'amax':
            self.current_lab_data[self.color]['max'][1] = self.ui.horizontalSlider_AMax.value()
            self.ui.label_AMax.setNum(self.current_lab_data[self.color]['max'][1])
        if name == 'bmax':
            self.current_lab_data[self.color]['max'][2] = self.ui.horizontalSlider_BMax.value()
            self.ui.label_BMax.setNum(self.current_lab_data[self.color]['max'][2])

    def get_yaml_data(self, yaml_file):
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.read()
        file.close()

        data = yaml.load(file_data, Loader=yaml.FullLoader)

        return data

    def save_yaml_data(self, data, yaml_file):
        file = open(yaml_file, 'w', encoding='utf-8')
        yaml.dump(data, file)
        file.close()

    def createConfig(self, c=False):
        if not os.path.isfile(self.lab_file):
            data = {'red': {'max': [255, 255, 255], 'min': [0, 150, 130]},
                    'green': {'max': [255, 110, 255], 'min': [47, 0, 135]},
                    'blue': {'max': [255, 136, 120], 'min': [0, 0, 0]},
                    'black': {'max': [89, 255, 255], 'min': [0, 0, 0]},
                    'white': {'max': [255, 255, 255], 'min': [193, 0, 0]}}
            self.save_yaml_data(data, self.lab_file)
            self.current_lab_data = data

            self.color_list = ['red', 'green', 'blue', 'black', 'white']
            self.ui.comboBox_color.addItems(self.color_list)
            self.ui.comboBox_color.currentIndexChanged.connect(self.selectionchange)
            self.selectionchange()
        else:
            try:
                self.current_lab_data = self.get_yaml_data(self.lab_file)
                self.color_list = self.current_lab_data.keys()
                self.ui.comboBox_color.addItems(self.color_list)
                self.ui.comboBox_color.currentIndexChanged.connect(self.selectionchange)
                self.selectionchange()
            except:
                print('读取颜色保存文件失败，格式错误！')

    def getColorValue(self, color):
        if color != '':
            self.current_lab_data = self.get_yaml_data(self.lab_file)
            if color in self.current_lab_data:
                self.ui.horizontalSlider_LMin.setValue(self.current_lab_data[color]['min'][0])
                self.ui.horizontalSlider_AMin.setValue(self.current_lab_data[color]['min'][1])
                self.ui.horizontalSlider_BMin.setValue(self.current_lab_data[color]['min'][2])
                self.ui.horizontalSlider_LMax.setValue(self.current_lab_data[color]['max'][0])
                self.ui.horizontalSlider_AMax.setValue(self.current_lab_data[color]['max'][1])
                self.ui.horizontalSlider_BMax.setValue(self.current_lab_data[color]['max'][2])
            else:
                self.current_lab_data[color] = {'max': [255, 255, 255], 'min': [0, 0, 0]}
                self.save_yaml_data(self.current_lab_data, self.lab_file)

                self.ui.horizontalSlider_LMin.setValue(0)
                self.ui.horizontalSlider_AMin.setValue(0)
                self.ui.horizontalSlider_BMin.setValue(0)
                self.ui.horizontalSlider_LMax.setValue(255)
                self.ui.horizontalSlider_AMax.setValue(255)
                self.ui.horizontalSlider_BMax.setValue(255)

    def selectionchange(self):
        self.color = self.ui.comboBox_color.currentText()
        self.getColorValue(self.color)

    def getcolor(self):
        color = self.d.lineEdit.text()
        self.ui.comboBox_color.addItem(color)
        time.sleep(0.1)
        self.qdi.accept()

    def closeqdialog(self):
        self.qdi.accept()

    def addcolor(self):
        self.qdi = QDialog()
        self.d = addcolor.Ui_Dialog()
        self.d.setupUi(self.qdi)
        self.qdi.show()
        self.d.pushButton_ok.clicked.connect(self.getcolor)
        self.d.pushButton_cancel.pressed.connect(self.closeqdialog)

    def deletecolor(self):
        self.color = self.ui.comboBox_color.currentText()
        del self.current_lab_data[self.color]
        self.save_yaml_data(self.current_lab_data, self.lab_file)

        self.ui.comboBox_color.clear()
        self.ui.comboBox_color.addItems(self.current_lab_data.keys())
