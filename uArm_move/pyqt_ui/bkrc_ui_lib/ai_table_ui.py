from pyqt_ui.bkrc_ui_lib.ui_bkrc import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from pyqt_ui.bkrc_ui_lib.AnimationShadowEffect import AnimationShadowEffect
import random
from tools.config import config as cfg
import cv2
import time
import socket
import numpy as np
import os

class AiTableUi(object):
    def __init__(self, ui: Ui_MainWindow, message, full_dict=None):
        self.ui = ui
        self.messageFrom = message

        self.full_dict = full_dict
        self.move_temp = 0
        self.img_rec_mode = 0  # 图像识别模式
        # self.obj_id = 0        # 物体位置id
        # self.lib_id = 0        # 仓库位置id
        # self.obj_flag = [False, False, False]
        # self.lib_flag = [False, False, False]
        # self.sorting_flag = [True, True]
        #

        #
        # self.sorting_val = self.full_dict[cfg.SORTING_VAL]

        # self.move_ctl = EmbdDrive(q_send)  # 机械臂控制
        # self.arm_move = ArmServo(self.move_ctl)

        self.time_cont = 0
        aniCamera = AnimationShadowEffect(Qt.blue, self.ui.move_button)
        self.ui.ai_camera.setGraphicsEffect(aniCamera)
        aniCamera.start()

        # 图像自适应控件大小
        self.ui.libbox0_label.setScaledContents(True)
        self.ui.libbox1_label.setScaledContents(True)
        self.ui.libbox2_label.setScaledContents(True)
        self.ui.libbox3_label.setScaledContents(True)

        self.ui_boxs = [self.ui.libbox0_label, self.ui.libbox1_label,
                        self.ui.libbox2_label, self.ui.libbox3_label]

        self.loadImg()   # 加载图像分类图片资源

        # -------------------comboBox控件初始化------------------------
        self.img_dis_list = ['自动控制', '手动控制']
        self.ui.exe_mode_combobox.addItems(self.img_dis_list)
        self.ui.exe_mode_combobox.currentIndexChanged.connect(self.imgDisComboboxChange)

        # ----------------------Button控件初始化------------------
        # 图像识别button
        self.ui.det_button.pressed.connect(lambda: self.buttonRecClicked("det_button"))
        self.ui.electron_button.pressed.connect(lambda: self.buttonRecClicked("electron_button"))
        self.ui.fruits_button.pressed.connect(lambda: self.buttonRecClicked("fruits_button"))
        self.ui.garbage_button.pressed.connect(lambda: self.buttonRecClicked("garbage_button"))
        self.ui.color_button.pressed.connect(lambda: self.buttonRecClicked("color_button"))
        self.ui.shape_button.pressed.connect(lambda: self.buttonRecClicked("shape_button"))
        self.ui.size_button.pressed.connect(lambda: self.buttonRecClicked("size_button"))
        self.ui.angle_button.pressed.connect(lambda: self.buttonRecClicked("angle_button"))
        self.ui.area_button.pressed.connect(lambda: self.buttonRecClicked("area_button"))

        # 仓库搬运控制button
        self.ui.lib_box_0.pressed.connect(lambda: self.buttonBoxClicked("lib_box_0"))
        self.ui.lib_box_1.pressed.connect(lambda: self.buttonBoxClicked("lib_box_1"))
        self.ui.lib_box_2.pressed.connect(lambda: self.buttonBoxClicked("lib_box_2"))
        self.ui.lib_box_3.pressed.connect(lambda: self.buttonBoxClicked("lib_box_3"))

        self.ui.m_cangku.pressed.connect(lambda: self.buttonBoxClicked("m_cangku"))

        self.ui.move_button.pressed.connect(lambda: self.buttonMoveClicked("move_button"))
        self.ui.adjust_camera.pressed.connect(lambda: self.buttonMoveClicked("adjust_camera"))

        # 机械臂控制button
        aniButton = AnimationShadowEffect(Qt.blue, self.ui.move_button)
        self.ui.move_button.setGraphicsEffect(aniButton)
        self.ui.move_button.clicked.connect(aniButton.stop)  # 按下按钮停止动画
        aniButton.start()

        # ---------------图像显示-----------------
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.showCamera)
        self.camera_timer.start()
        self.ui.ai_camera.setScaledContents(True)

    def loadImg(self):
        self.electron_img = []
        self.fruits_img = []
        self.garbage_img = []
        self.refuse_img = []
        self.img_list = [[], self.electron_img, self.fruits_img, self.refuse_img]

        bas_path = ":/electron/images/electron/"
        for i in range(0, 4):
            self.electron_img.append(QPixmap(bas_path + str(i) + ".jpg"))

        bas_path = ":/fruits/images/fruits/"
        for i in range(0, 4):
            self.fruits_img.append(QPixmap(bas_path + str(i) + ".png"))

        bas_path = ":/refuse/images/refuse/"
        for i in range(0, 4):
            self.refuse_img.append(QPixmap(bas_path + str(i) + ".png"))

        bas_path = ":/garbage/images/garbage/"
        for i in range(1, 17):
            self.garbage_img.append(QPixmap(bas_path + str(i) + ".jpg"))

    def showCamera(self):
        # 图像显示窗口
        img = self.full_dict[cfg.REC_IMAGE]
        if img is not None:
            show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ui.ai_camera.setPixmap(QPixmap.fromImage(showImage))

        self.time_cont += 1
        if self.time_cont > 20:
            self.time_cont = 0
            self.objImgDis()

    # ---------------------按键监听-----------------------
    def buttonRecClicked(self, name):
        if name == 'det_button':
            self.img_rec_mode = cfg.DET_REC
        if name == 'electron_button':
            self.img_rec_mode = cfg.ELECTRON_REC
        if name == 'fruits_button':
            self.img_rec_mode = cfg.FRUIT_REC
        if name == 'garbage_button':
            self.img_rec_mode = cfg.GARBAGE_REC
        if name == 'color_button':
            self.img_rec_mode = cfg.COLOR_REC
        if name == "shape_button":
            self.img_rec_mode = cfg.SHAPE_REC
        if name == "size_button":
            self.img_rec_mode = cfg.SIZE_REC
            self.full_dict['get_val'] = True
        if name == "angle_button":
            self.img_rec_mode = cfg.ANGLE_REC
        if name == "area_button":
            self.full_dict['get_val'] = True
            self.img_rec_mode = cfg.AREA_REC

        self.libImgDis()   # 更新仓库显示

    def buttonBoxClicked(self, name):
        self.obj_id = -1
        # combobox_val = self.ui.exe_mode_combobox.currentText()
        # sort_mode = self.full_dict[cfg.SORTING_MODE]
        # if combobox_val == "自动控制":
        #     sort_mode[0] = True
        # elif combobox_val == "手动控制":
        #     sort_mode[0] = False

        if name == "m_cangku":
            self.libImgDis(True)
        if name == "lib_box_0":
            self.obj_id = 0
        if name == "lib_box_1":
            self.obj_id = 1
        if name == "lib_box_2":
            self.obj_id = 2
        if name == "lib_box_3":
            self.obj_id = 3

        self.sorting_val = self.full_dict[cfg.SORTING_VAL]  # 获取最新状态值
        self.sorting_val[cfg.MOVE_COM][2] = self.obj_id
        self.full_dict[cfg.SORTING_VAL] = self.sorting_val
        # self.full_dict[cfg.SORTING_MODE] = sort_mode


    def libImgDis(self, rdm=False):
        """
        仓库位置图像更新控制
        Args:
            val:  图像识别模式（1~6）
            rdm:  随机位置使能 （True/False）
        Returns:
        """
        self.sorting_val = self.full_dict[cfg.SORTING_VAL]  # 获取最新状态值

        if self.img_rec_mode > 0 and self.img_rec_mode <= cfg.GARBAGE_REC:
            add_val = [0, 1, 2, 3]
            idex = self.img_rec_mode

            if rdm:  # 随机生成
                random.shuffle(add_val)

            for i, val in enumerate(add_val):
                # 在UI界面中显示对应识别模式图片
                self.ui_boxs[i].setPixmap(self.img_list[idex][val])

            self.sorting_val[cfg.WAREHOUSE_COM] = add_val     # 更新仓库位置

        self.sorting_val[cfg.IMG_COM] = self.img_rec_mode     # 更新识别模式
        self.full_dict[cfg.SORTING_VAL] = self.sorting_val    # 更新状态值
        # print('self.img_rec_mode :',  self.full_dict[cfg.SORTING_VAL])

    def objImgDis(self):
        # self.sorting_val = self.full_dict[cfg.SORTING_VAL]
        # obj_val = self.sorting_val[cfg.CARGO_COM]
        # move_idex = self.sorting_val[cfg.MOVE_COM][1]

        move_idex = self.full_dict['rec_index']

        if self.img_rec_mode > 0 and self.img_rec_mode <= cfg.GARBAGE_REC:
            if move_idex >= 0:
                self.ui.rec_img.setPixmap(self.img_list[self.img_rec_mode][move_idex])


    # def buttonBoxClicked(self, name):
    #     if name[0] == 'b' or name[0] == 'l':
    #         if name == "box_0":
    #             self.obj_flag[0] = True
    #             self.obj_id = 1
    #         if name == "box_1":
    #             self.obj_id = 2
    #             self.obj_flag[1] = True
    #         if name == "box_2":
    #             self.obj_id = 3
    #             self.obj_flag[2] = True
    #
    #         if name == "lib_box_0":
    #             self.lib_id = 1
    #             self.lib_flag[0] = True
    #         if name == "lib_box_1":
    #             self.lib_id = 2
    #             self.lib_flag[1] = True
    #         if name == "lib_box_2":
    #             self.lib_id = 3
    #             self.lib_flag[2] = True

            # self.sortingMove()   # 获取物体搬运指令

    #     if name == "huowu":
    #         pass
    #         # self.lib_id = 0
    #         # self.lib_id = 0
    #
    #     if name == "m_cangku":
    #         self.libImgDis(rdm=True)
    #
    # def sortingMove(self):
    #     self.sorting_val = self.full_dict[cfg.SORTING_VAL]
    #
    #     def get_index(lst=None, item=True):
    #         return np.array([i for i in range(len(lst)) if lst[i] == item]) + 1
    #
    #     obj_index = get_index(self.obj_flag, True)
    #     lib_index = get_index(self.lib_flag, True)
    #
    #     print("---index:", obj_index, " ", lib_index)
    #
    #     if len(obj_index) > 0 and self.sorting_flag[0]:
    #         self.sorting_flag[1] = False
    #         if len(obj_index) > 1:
    #             if obj_index[1] != self.move_temp:
    #                 self.sorting_val[cfg.MOVE_COM] = [0,  self.move_temp,  obj_index[1]]
    #             else:
    #                 self.sorting_val[cfg.MOVE_COM] = [0,  self.move_temp, obj_index[0]]
    #             self.obj_flag = [False, False, False]
    #             self.lib_flag = [False, False, False]
    #             self.sorting_flag = [True, True]
    #             self.move_temp = 0
    #         elif len(lib_index) > 0:
    #             self.sorting_val[cfg.MOVE_COM] = [1, obj_index[0], lib_index[0]]
    #             self.obj_flag = [False, False, False]
    #             self.lib_flag = [False, False, False]
    #             self.sorting_flag = [True, True]
    #             self.move_temp = 0
    #         else:
    #             self.move_temp = obj_index[0]
    #
    #     elif len(lib_index) > 0 and self.sorting_flag[1]:
    #         self.sorting_flag[0] = False
    #         if len(lib_index) > 1:
    #             if lib_index[1] != self.move_temp:
    #                 self.sorting_val[cfg.MOVE_COM] = [2, self.move_temp, lib_index[1]]
    #             else:
    #                 self.sorting_val[cfg.MOVE_COM] = [2, self.move_temp, lib_index[0]]
    #             self.obj_flag = [False, False, False]
    #             self.lib_flag = [False, False, False]
    #             self.sorting_flag = [True, True]
    #             self.move_temp = 0
    #         elif len(obj_index) > 0:
    #             self.sorting_val[cfg.MOVE_COM] = [3, lib_index[0], obj_index[0]]
    #             self.obj_flag = [False, False, False]
    #             self.lib_flag = [False, False, False]
    #             self.sorting_flag = [True, True]
    #             self.move_temp = 0
    #         else:
    #             self.move_temp = lib_index[0]
    #
    #     self.full_dict[cfg.SORTING_VAL] = self.sorting_val
    #     print("-----full:", self.full_dict[cfg.SORTING_VAL])
    #
    # # self.sorting_val[MOVE_COM][CARGO] = int(combobox_val)
    # # self.full_dict[cfg.SORTING_VAL] = self.sorting_val
    #
    def buttonMoveClicked(self, name):
        sorting_mode = self.full_dict[cfg.SORTING_MODE]
        if name == "move_button":
          sorting_mode[0] = not sorting_mode[0]
          if sorting_mode[0]:
              self.ui.move_button.setText("分拣开启")
          else:
              self.ui.move_button.setText("分拣关闭")

        if name == "adjust_camera":
            sorting_mode[2] = not sorting_mode[2]
            if sorting_mode[2]:
                self.ui.adjust_camera.setText("摄像头位置校准开启")
            else:
                self.ui.adjust_camera.setText("摄像头位置校准关闭")

        self.full_dict[cfg.SORTING_MODE] = sorting_mode


    #         # 执行舵机控制指令
    #         sort_mode = self.full_dict[cfg.SORTING_MODE]
    #         self.sorting_val = self.full_dict[cfg.SORTING_VAL]
    #         print("sort_mode{},val{}".format(sort_mode, self.sorting_val))
    #         if sort_mode[0]:
    #             if sort_mode[1] == 1:
    #                 self.sorting_val[cfg.MOVE_COM] = [1, 2, 3]
    #         else:
    #             if sort_mode[1] == 1:
    #                 self.sorting_val[cfg.MOVE_COM] = [1, self.obj_id, self.lib_id]
    #             elif sort_mode[1] == 2:
    #                 self.sorting_val[cfg.MOVE_COM] = [1, self.obj_id, 0]
    #                 self.obj_flag = [False, False, False]
    #
    #         self.full_dict[cfg.SORTING_VAL] = self.sorting_val
    #
    def imgDisComboboxChange(self):
        combobox_val = self.ui.exe_mode_combobox.currentText()
        sort_mode = self.full_dict[cfg.SORTING_MODE]
        if combobox_val == "自动控制":
            sort_mode[1] = 0
        elif combobox_val == "手动控制":
            sort_mode[1] = 1
        self.full_dict[cfg.SORTING_MODE] = sort_mode
        print("self.full_dict[cfg.SORTING_MODE]:", self.full_dict[cfg.SORTING_MODE])
        # print("imgDisComboboxChange:", self.full_dict)

    # def imgRecComboboxChange(self):
    #     combobox_val = self.ui.img_rec_combobox.currentText()
    #     sort_mode = self.full_dict[cfg.SORTING_MODE]
    #     self.sorting_val = self.full_dict[cfg.SORTING_VAL]
    #     if combobox_val == "固定位置分拣":
    #         sort_mode[1] = 1
    #         self.sorting_val[cfg.MOVE_COM] = [0, 0, 0]
    #     elif combobox_val == "图像识别分拣":
    #         sort_mode[1] = 2
    #         self.sorting_val[cfg.CARGO_COM] = []
    #     elif combobox_val == "自动识别分拣":
    #         sort_mode[1] = 3
    #         self.sorting_val[cfg.CARGO_COM] = []
    #     self.full_dict[cfg.SORTING_MODE] = sort_mode
    #     self.full_dict[cfg.SORTING_VAL] = self.sorting_val
    #

