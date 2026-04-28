import math
import time
from tools.config import config as cfg
from embedded.uarm.wrapper import SwiftAPI
import platform
import serial
import serial.tools.list_ports
import os
import yaml

class ArmServo(object):
    def __init__(self, full_dict=None, yaml_path='../resource/arm_polar.yaml'):
        self.port = self.checkport(COM=None)
        self.arm = SwiftAPI(port=self.port, baudrate=115200)

        # 全局共享数据
        self.full_dict = full_dict

        # 机械臂分拣坐标
        self.arm_polar_val = self.getYamlData(yaml_path)

        self.polar_height = -8   # 抓取高度值
        self.x_weight = 5.5        # 表示图像坐标所对应的x轴角度系数

        # 定义不同位置的变量参数
        self.com_list_lib = [[], self.arm_polar_val[0], self.arm_polar_val[1],
                             self.arm_polar_val[2], self.arm_polar_val[3]]

        self.arm.set_speed_factor(100)  # 设置移动速度系数

        self.initMove()

    def checkport(self, COM):
        print('Checking Device...... \n')
        port = None
        if platform.system() == 'Windows':
            plist = list(serial.tools.list_ports.comports())
            if len(plist) <= 0:
                print("The Serial port can't find!")
            else:
                plist_0 = list(plist[0])
                port = plist_0[0]
        else:
            try:
                # 获取机械臂端口信息
                ret = os.popen("ls /dev/serial/by-id").read()
                port = "/dev/serial/by-id/" + ret.split('\n')[0].split('/')[-1]
                # 打印检测到的机械臂端口
                print('Current device: ' + port + '\n')
            except:
                print("The Serial port can't find!")

        if port is not None:
            return port
        else:
            return COM

    def getYamlData(self, yaml_file):
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.read()
        file.close()

        data = yaml.load(file_data, Loader=yaml.FullLoader)
        return data

    def saveYamlData(self, data, yaml_file):
        file = open(yaml_file, 'w', encoding='utf-8')
        yaml.dump(data, file)
        file.close()

    def armReset(self):
        # 复位
        self.arm.reset(speed=4000)

    def initMove(self):
        # self.armReset()
        self.servosMove((90, 120, 50), movetime=1000)
        self.servoAngle(0)

    def armServoSwitch(self, std=True):
        # 设置伺服连接函数
        if std:
            self.arm.set_servo_attach()
        else:
            self.arm.set_servo_detach()

    def armGetPolar(self):
        #　返回机械臂当前坐标
        return self.arm.get_polar()

    def armClampBlock(self, enable=False, movetime=2000, mode=1):
        # 定义夹积木块函数， mode=1 爪子 mode=2 吸盘   enable=True：夹住，=False：松开
        if mode == 1:
            self.arm.set_gripper(catch=enable)
        else:
            self.arm.set_pump(on=enable)
        time.sleep(movetime/1000)

    def armBuzzer(self, tim=2):
        self.arm.set_buzzer(frequency=1000, duration=tim)

    def moveUp(self, movetime=1500):
        # 机械臂向上移动
        # self.arm.set_position(x=115, y=-3, z=45, speed=movetime)
        self.arm.set_polar(rotation=90, stretch=136, height=50,
                           timeout=movetime)

        time.sleep(movetime / 1000)

    def servosMove(self, coordinate_data, movetime=1500, wait_flag=True):
        # 机械臂移动控制
        self.arm.set_polar(rotation=coordinate_data[0],
                           stretch=coordinate_data[1],
                           height=coordinate_data[2], timeout=movetime, speed=300)
        if wait_flag:
            time.sleep(movetime / 1000)

    def servoAngle(self, angle, timeout=15, wait_flag=True):
        # 旋转角度控制
        self.arm.set_wrist(angle, timeout=timeout)
        if wait_flag:
            time.sleep(timeout / 1000)

    def autoMove(self, id):
        if id >= 0 and id <= 3:
            self.servosMove(self.arm_polar_val[id]['xyz'])
            self.servoAngle(180-self.arm_polar_val[id]['angle'])


    def imgRecCtr(self, starts, id, auto=False):
        # for i, val in enumerate(starts):

        sorting_val = self.full_dict[cfg.SORTING_VAL]
        wareh = sorting_val[cfg.WAREHOUSE_COM]

        id_index = 0
        for i, val in enumerate(reversed(starts)):
            if val:
                if id and auto:
                    print("id:", id)
                    if len(id) > 1:
                        id_index = id[len(id) - (i + 1)]
                        self.full_dict['rec_index'] = id_index
                    else:
                        id_index = id[0]

                x, y, z = val[0], val[1]*10, self.polar_height
                x = 90 + x * self.x_weight
                self.moveUp()  # 归位
                #print("11111")
                self.servosMove((x, y, z+50), movetime=1500, wait_flag=True)
                self.servoAngle(180-x)
                self.servosMove((x, y, z), movetime=500, wait_flag=True)
                #print("22222")
                self.armClampBlock(True)  # 抓取
                # self.moveUp()  # 归位
                self.servosMove((x, y, z+50), movetime=500, wait_flag=True)

                if auto:
                    if id and id_index >= 0:
                        self.autoMove(wareh.index(id_index))
                    else:
                        if i > 3:
                            i = 3
                        self.autoMove(i)
                else:
                    self.autoMove(id)

                self.armClampBlock(False)  # 放下
        self.initMove()


    def imgRecMove(self, starts: list, ends: list, mode=1):
        """
        图像识别结果物体分拣功能函数
        Args:
            starts: 货物位置
            ends:   仓库位置
            mode:   执行模式
        Returns:
        """
        for i, val in enumerate(starts):
            if val:
                self.moveUp()
                # self.setBusServoPulse(2, self.com_list_box[i+1][-1], 500) # 旋转角控制
                self.servosMove(self.com_list_box[i+1][:3], 1500)
                self.armClampBlock(True)  # 抓取
                self.moveUp()             # 归位
                index = ends.index(val) + 1  # 获取仓库位置的索引
                # self.setBusServoPulse(2, self.com_list_lib[index][-1], 500) # 旋转角控制
                self.servosMove(self.com_list_lib[index][:3], 1500)
                self.armClampBlock(False)  # 放下
                self.servosMove((self.com_list_lib[index][0], self.com_list_lib[index][1] + 2,
                                     self.com_list_lib[index][2] + 5), 500)
        self.initMove()

    def recMoveAuto(self, vals,  starts: list, ends: list, auto=False, index=0):
        """
        根据物体坐标位置自动控制机械臂移动
        Args:
            vals: 物体抓取的位置（x, y, angle(物体的旋转角)）
            ends: 物体放置位置的索引值
            auto:
            index:
            物体位置 【1， 2， 3】     通用数据
            识别结果顺序【2， 1， 3】   全局变量
            物体搬运位置【1， 2， 3】   全局变量
        Returns:
        """
        if auto:
            for i, val in enumerate(vals):
                self.moveUp()
                # servo2_angle = self.getAngle(*val)     # 计算夹持器需要旋转的角度
                # self.setBusServoPulse(2, servo2_angle, 500)
                x = val[0] * -1
                if x > 0:
                    x -= cfg.X_BIAS
                else:
                    x += cfg.X_BIAS
                self.servosMove((x, val[1] + cfg.Y_BIAS, 3), 1500)
                self.armClampBlock(True)  # 抓取
                self.moveUp()             # 归位

                if starts and sum(starts):
                    index = ends.index(starts[i]) + 1  # 根据货物类别获取仓库位置的索引
                else:
                    index = 1

                # self.setBusServoPulse(2, self.com_list_lib[index][-1], 500) # 旋转角控制
                self.servosMove(self.com_list_lib[index][:3], 1500)
                self.armClampBlock(False)  # 放下
                self.servosMove((self.com_list_lib[index][0], self.com_list_lib[index][1] + 2,
                                     self.com_list_lib[index][2] + 5), 500)
                self.initMove()
        else:
            # x, y, roi_angle = vals[index]
            val = vals[index-1]
            self.moveUp()
            # servo2_angle = self.getAngle(*val)  # 计算夹持器需要旋转的角度
            # self.set_servo_angle(2, servo2_angle, 500)
            self.servosMove((val[0]*-1 + 1.5, val[1], 3), 1500)
            self.armClampBlock(True)  # 抓取
            self.moveUp()             # 归位
            index = ends.index(starts[index-1]) + 1  # 根据货物类别获取仓库位置的索引
            # self.setBusServoPulse(2, self.com_list_lib[index][-1], 500)
            self.servosMove(self.com_list_lib[index][:3], 1500)
            self.armClampBlock(False)  # 放下
            self.servosMove((self.com_list_lib[index][0], self.com_list_lib[index][1] + 2,
                                 self.com_list_lib[index][2] + 5), 500)

    def allAutoMove(self, full_dict):
        sort_mode = full_dict[cfg.SORTING_MODE]
        sort_val = full_dict[cfg.SORTING_VAL]
        move_com = sort_val[cfg.MOVE_COM]
        cargo_com = sort_val[cfg.CARGO_COM]
        warehouse_com = sort_val[cfg.WAREHOUSE_COM]
        img_det_xy = full_dict[cfg.IMG_DET_XY]  # 矩形框中心坐标位置映射
        img_com = sort_val[cfg.IMG_COM]

        if sort_mode[0]:  # 自动分拣模式
            if sort_mode[1] == 1:
                # 基本分拣模式
                if move_com[1] and move_com[2]:  # 货物位置与仓库位置不为空
                    self.autoMove(all_auto=True)
                    sort_val[cfg.MOVE_COM] = [0, 0, 0]
                    full_dict[cfg.SORTING_VAL] = sort_val

            elif sort_mode[1] == 2:
                # 图像识别分拣模式
                if sum(cargo_com) and img_com:
                    self.imgRecMove(cargo_com, warehouse_com)
                    sort_val[cfg.CARGO_COM] = [0, 0, 0]
                    # sort_val[cfg.IMG_COM] = 0
                    full_dict[cfg.SORTING_VAL] = sort_val
                    full_dict[cfg.IMG_DET_XY] = []

            elif sort_mode[1] == 3:
                # 自动抓取分拣
                if full_dict[cfg.IMG_DET_XY]:
                    self.recMoveAuto(img_det_xy, cargo_com, warehouse_com, auto=True)
                    sort_val[cfg.CARGO_COM] = [0, 0, 0]
                    full_dict[cfg.IMG_DET_XY] = []
                    full_dict[cfg.SORTING_VAL] = sort_val

        else:  # 手动分拣
            if sort_mode[1] == 1:
                # 基本分拣模式
                if move_com[1] and move_com[2]:  # 货物位置与仓库位置不为空
                    self.autoMove(move_com[0], move_com[1], move_com[2])
                    sort_val[cfg.MOVE_COM] = [0, 0, 0]
                    full_dict[cfg.SORTING_VAL] = sort_val

            elif sort_mode[1] == 2:
                # 图像识别分拣模式
                # print("wq-:", move_com, " ", img_com)
                if move_com[1] and img_com and sum(cargo_com):  # 货物位置与仓库位置不为空
                    # print("wq-:", move_com, " ", img_com, "-",cargo_com[move_com[1] - 1], " ", warehouse_com.index(cargo_com[move_com[1] - 1]) + 1)
                    try:
                        self.autoMove(1, move_com[1], warehouse_com.index(cargo_com[move_com[1] - 1]) + 1)
                        sort_val[cfg.MOVE_COM] = [0, 0, 0]
                        cargo_com[move_com[1] - 1] = 0
                        if sum(cargo_com) == 0:
                            sort_val[cfg.IMG_COM] = 0
                            sort_val[cfg.CARGO_COM] = [0, 0, 0]
                            full_dict[cfg.IMG_DET_XY] = []
                        else:
                            sort_val[cfg.CARGO_COM] = cargo_com
                        print("wq-:sort_val{}".format(sort_val))
                        full_dict[cfg.SORTING_VAL] = sort_val
                    except:
                        sort_val[cfg.MOVE_COM] = [0, 0, 0]
                        # sort_val[cfg.IMG_COM] = 0

