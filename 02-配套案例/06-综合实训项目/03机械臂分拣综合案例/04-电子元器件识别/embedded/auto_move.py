import time
from embedded.uarm.wrapper import SwiftAPI
import platform
import serial
import serial.tools.list_ports
import os
import yaml


class ArmServo(object):
    def __init__(self,  yaml_path='./resource/arm_polar.yaml'):
        self.port = self.checkport(COM=None)
        # self.port = "COM20"
        self.arm = SwiftAPI(port=self.port, baudrate=115200)

        # 机械臂分拣坐标
        self.arm_polar_val = self.getYamlData(yaml_path)

        self.polar_height = -8   # 抓取高度值
        self.x_weight = 5.0        # 表示图像坐标所对应的x轴角度系数

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
        self.servoAngle(0)  # 旋转角度

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

    def imgRecCtr(self, starts, id, auto=True):
        id_index = 0
        for i, val in enumerate(reversed(starts)):
            if val:
                if id and auto:
                    print("id:", id)
                    if len(id) > 1:
                        id_index = id[len(id) - (i + 1)]
                    else:
                        id_index = id[0]

                x, y, z = val[0], val[1]*10, self.polar_height
                x = 90 + x * self.x_weight
                
                self.moveUp()  # 机械臂归位

                self.servosMove((x, y, z+50), movetime=1500, wait_flag=True)
                self.servoAngle(180-x)  # 旋转角度控制
                self.servosMove((x, y, z), movetime=500, wait_flag=True)

                self.armClampBlock(True)  # 机械臂爪子抓取
                # self.moveUp()  # 归位
                self.servosMove((x, y, z+50), movetime=500, wait_flag=True)

                if auto:
                    if id:
                        self.autoMove(id_index)
                    else:
                        if i > 3:
                            i = 3
                        self.autoMove(i)
                else:
                    self.autoMove(id)

                self.armClampBlock(False)  # 放下
        self.initMove()
