from pyqt_ui.bkrc_ui_lib.ui_bkrc import Ui_MainWindow

class ArmMoveTableUi(object):
    def __init__(self, ui: Ui_MainWindow, message, full_dict=None):
        self.ui = ui
        self.messageFrom = message
        self.full_dict = full_dict

        # ---------------机械臂控制相关参数--------------
        self.buzz_flag = False     # 蜂鸣器控制标志
        self.pump_flag = False     # 吸盘控制标志
        self.gripper_flag = False  # 电动夹控制标志

        self.motor_enable = True   # 伺服电机使能标志
        self.motor_enable_flag = False  # 伺服电机控制标志

        self.x_val_min = 45
        self.x_val_max = 180

        self.y_val_min = 115
        self.y_val_max = 350

        self.z_val_min = -50
        self.z_val_max = 150

        self.angle_max = 180
        self.angle_min = 0

        self.move_x = 90
        self.move_y = 120
        self.move_z = 50
        self.move_angle = 90  # 旋转角

        self.ui.angle_slider.setValue(self.move_angle)
        self.ui.label_angle.setText("旋转角：{}°".format(self.move_angle))

        self.ui.move_x_slider.setValue(self.move_x)
        self.ui.move_x_val.setText(str(self.move_x) + '°')

        self.ui.move_y_slider.setValue(self.move_y)
        self.ui.move_y_val.setText(str(self.move_y) + 'mm')

        self.ui.move_z_slider.setValue(self.move_z)
        self.ui.move_z_val.setText(str(self.move_z) + 'mm')

        # -------------------slide控件初始化------------------------
        # 设置滑动杆区间值
        self.ui.angle_slider.setMinimum(self.angle_min)
        self.ui.angle_slider.setMaximum(self.angle_max)

        self.ui.move_x_slider.setMinimum(self.x_val_min)
        self.ui.move_x_slider.setMaximum(self.x_val_max)

        self.ui.move_y_slider.setMinimum(self.y_val_min)
        self.ui.move_y_slider.setMaximum(self.y_val_max)

        self.ui.move_z_slider.setMinimum(self.z_val_min)
        self.ui.move_z_slider.setMaximum(self.z_val_max)

        # 机械臂滑动杆的信号与 moveSliderValueChange函数绑定
        self.ui.angle_slider.valueChanged.connect(lambda: self.moveSliderValueChange('angle_slider'))

        self.ui.move_x_slider.valueChanged.connect(lambda: self.moveSliderValueChange('move_x_val'))
        self.ui.move_y_slider.valueChanged.connect(lambda: self.moveSliderValueChange('move_y_val'))
        self.ui.move_z_slider.valueChanged.connect(lambda: self.moveSliderValueChange('move_z_val'))

        # ----------------------Button控件初始化------------------
        self.ui.angle_add.pressed.connect(lambda: self.buttonMoveClicked("angle_add"))
        self.ui.angle_cut.pressed.connect(lambda: self.buttonMoveClicked("angle_cut"))

        self.ui.move_up_button.pressed.connect(lambda: self.buttonMoveClicked("move_up_button"))
        self.ui.move_down_button.pressed.connect(lambda: self.buttonMoveClicked("move_down_button"))
        self.ui.move_left_button.pressed.connect(lambda: self.buttonMoveClicked("move_left_button"))
        self.ui.move_right_button.pressed.connect(lambda: self.buttonMoveClicked("move_right_button"))
        self.ui.move_centre_button.pressed.connect(lambda: self.buttonMoveClicked("move_centre_button"))
        self.ui.move_top_button.pressed.connect(lambda: self.buttonMoveClicked("move_top_button"))
        self.ui.move_back_button.pressed.connect(lambda: self.buttonMoveClicked("move_back_button"))

        self.ui.buzz_button.pressed.connect(lambda: self.buttonMoveClicked("buzz_button"))
        self.ui.pump_button.pressed.connect(lambda: self.buttonMoveClicked("pump_button"))
        self.ui.gripper_button.pressed.connect(lambda: self.buttonMoveClicked("gripper_button"))
        self.ui.motor_button.pressed.connect(lambda: self.buttonMoveClicked("motor_button"))

        # -------------------comboBox控件初始化------------------------
        self.box_list = ['1号位置', '2号位置', '3号位置', '4号位置']
        self.ui.comboBox_place.addItems(self.box_list)
        self.ui.comboBox_place.currentIndexChanged.connect(self.boxPlaceComboboxChange)
        self.box_index = 0

    # ---------------------下拉菜单监听-----------------------
    def boxPlaceComboboxChange(self):
        combobox_val = self.ui.comboBox_place.currentText()
        self.box_index = self.box_list.index(combobox_val)
        self.full_dict['arm_ctr_val'] = [True,
                                         [self.move_x, self.move_y, self.move_z, self.move_angle],
                                         [self.buzz_flag, self.pump_flag, self.gripper_flag],
                                         {'std': self.motor_enable_flag,
                                          'val': [self.motor_enable, self.box_index]}]

    # ---------------------按键监听-----------------------
    def buttonMoveClicked(self, name):
        print("move_ctl_mode:", name)
        if name == "move_button":
            # 执行舵机控制指令
            pass
        else:
            if name == "angle_add":
                self.move_angle += 1
                if self.move_angle > self.angle_max:
                    self.move_angle = self.angle_max
                    print("move_angle:", self.move_angle)
                self.ui.angle_slider.setValue(self.move_angle)

                text = "旋转角：{}°".format(self.move_angle)
                if self.move_z > 65:
                    text = "旋转角：{}° (注意机械臂高度要低于65mm才可以控制！)".format(self.move_angle)
                self.ui.label_angle.setText(text)

            if name == "angle_cut":
                self.move_angle -= 1
                if self.move_angle < self.angle_min:
                    self.move_angle = self.angle_min
                    print("move_angle:", self.move_angle)
                self.ui.angle_slider.setValue(self.move_angle)

                text = "旋转角：{}°".format(self.move_angle)
                if self.move_z > 65:
                    text = "旋转角：{}° (注意机械臂高度要低于65mm才可以控制！)".format(self.move_angle)
                self.ui.label_angle.setText(text)

            if name == "move_up_button":
                self.move_z += 1
                if self.move_z > self.z_val_max:
                    self.move_z = self.z_val_max
                    print("z_val_erro:", self.move_z)
                self.ui.move_z_slider.setValue(self.move_z)
                self.ui.move_z_val.setText(str(self.move_z) + 'mm')

            if name == "move_down_button":
                self.move_z -= 1
                if self.move_z < self.z_val_min:
                    self.move_z = self.z_val_min
                    print("z_val_erro:", self.move_z)
                self.ui.move_z_slider.setValue(self.move_z)
                self.ui.move_z_val.setText(str(self.move_z) + 'mm')

            if name == "move_left_button":
                self.move_x -= 1
                if self.move_x < self.x_val_min:
                    self.move_x = self.x_val_min
                    print("x_val_erro:", self.move_x)
                self.ui.move_x_slider.setValue(self.move_x)
                self.ui.move_x_val.setText(str(self.move_x) + '°')

            if name == "move_right_button":
                self.move_x += 1
                if self.move_x > self.x_val_max:
                    self.move_x = self.x_val_max
                    print("x_val_erro:", self.move_x)
                self.ui.move_x_slider.setValue(self.move_x)
                self.ui.move_x_val.setText(str(self.move_x) + '°')

            if name == "move_top_button":
                self.move_y += 1
                if self.move_y > self.y_val_max:
                    self.move_y = self.y_val_max
                    print("y_val_erro:", self.move_y)
                self.ui.move_y_slider.setValue(self.move_y)
                self.ui.move_y_val.setText(str(self.move_y) + 'mm')

            if name == "move_back_button":
                self.move_y -= 1
                if self.move_y < self.y_val_min:
                    self.move_y = self.y_val_min
                    print("y_val_erro:", self.move_y)
                self.ui.move_y_slider.setValue(self.move_y)
                self.ui.move_y_val.setText(str(self.move_y) + 'mm')

            if name == "move_centre_button":
                self.move_x = 90
                self.move_y = 120
                self.move_z = 50
                self.move_angle = 90

                self.ui.angle_slider.setValue(self.move_angle)
                self.ui.label_angle.setText("旋转角：{}°".format(self.move_angle))

                self.ui.move_x_slider.setValue(self.move_x)
                self.ui.move_x_val.setText(str(self.move_x) + '°')

                self.ui.move_y_slider.setValue(self.move_y)
                self.ui.move_y_val.setText(str(self.move_y) + 'mm')

                self.ui.move_z_slider.setValue(self.move_z)
                self.ui.move_z_val.setText(str(self.move_z) + 'mm')

            if name == "buzz_button":
                self.buzz_flag = True

            if name == 'pump_button':
                self.pump_flag = not self.pump_flag
                if self.pump_flag:
                    self.ui.pump_button.setText('吸盘：开启')
                else:
                    self.ui.pump_button.setText('吸盘：关闭')

            if name == 'gripper_button':
                self.gripper_flag = not self.gripper_flag
                if self.gripper_flag:
                    self.ui.gripper_button.setText('电动夹：闭合')
                else:
                    self.ui.gripper_button.setText('电动夹：打开')

            if name == 'motor_button':
                self.motor_enable = not self.motor_enable
                self.motor_enable_flag = True
                if self.motor_enable:
                    self.ui.motor_button.setText('伺服电机启动')
                    self.messageFrom("设置{}坐标成功！！".format(self.box_list[self.box_index]))
                else:
                    self.ui.motor_button.setText('伺服电机掉电')

            self.full_dict['arm_ctr_val'] = [True,
                                             [self.move_x, self.move_y, self.move_z, self.move_angle],
                                             [self.buzz_flag, self.pump_flag, self.gripper_flag],
                                             {'std': self.motor_enable_flag,
                                              'val': [self.motor_enable, self.box_index]}]

            self.buzz_flag = False
            self.motor_enable_flag = False

        # ---------------------滑动条监听----------------------

    def moveSliderValueChange(self, name):
        if name == "angle_slider":
            val = self.ui.angle_slider.value()

            text = "旋转角：{}°".format(val)
            if self.move_z > 65:
                text = "旋转角：{}° (注意机械臂高度要低于65mm才可以控制！)".format(val)
            self.ui.label_angle.setText(text)
            self.move_angle = val

        if name == 'move_x_val':
            val = self.ui.move_x_slider.value()
            self.temp = str(val)
            self.ui.move_x_val.setText(self.temp + '°')
            self.move_x = val

        if name == "move_y_val":
            val = self.ui.move_y_slider.value()
            self.temp = str(val)
            self.ui.move_y_val.setText(self.temp + 'mm')
            self.move_y = val

        if name == "move_z_val":
            val = self.ui.move_z_slider.value()
            self.temp = str(val)
            self.ui.move_z_val.setText(self.temp + 'mm')
            self.move_z = val

        self.full_dict['arm_ctr_val'] = [True,
                                         [self.move_x, self.move_y, self.move_z, self.move_angle],
                                         [self.buzz_flag, self.pump_flag, self.gripper_flag],
                                         {'std': self.motor_enable_flag,
                                          'val': [self.motor_enable, self.box_index]}]





