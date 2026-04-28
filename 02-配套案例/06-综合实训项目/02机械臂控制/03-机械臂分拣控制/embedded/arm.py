from telnetlib import COM_PORT_OPTION
import time
import platform
import os
import serial.tools.list_ports
from embedded.uarm.wrapper import SwiftAPI

class Arm:
    def __init__(self,COM=None):
        self.port = self.checkport(COM)
        self.arm = SwiftAPI(port=self.port, baudrate=115200)
        # 设置移动速度系数
        self.arm.set_speed_factor(100)
        # self.arm.set_speed(30)
        

    def checkport(self, COM):
        print('Checking Device...... \n')
        port = None
        if platform.system() == 'Windows':
            plist = list(serial.tools.list_ports.comports())
            if len(plist) <= 0:
                print ("The Serial port can't find!")
            else:
                plist_0 =list(plist[0])
                port= plist_0[0]
                print('Current device: ' + port + '\n')
        else:
            try:
                # 获取机械臂端口信息
                ret = os.popen("ls /dev/serial/by-id").read()
                port = "/dev/serial/by-id/" + ret.split('\n')[0].split('/')[-1]
                # 打印检测到的机械臂端口
                print('Current device: ' + port + '\n')
            except:
                print ("The Serial port can't find!")

        if port is not None:
            return port
        else:   
            return COM
    
    '''
    复位函数
    '''
    def Arm_Reset(self):
        # 复位
        self.arm.reset(speed=1000)
        # time.sleep(1)

    '''
    设置伺服连接函数
    '''
    def Arm_Set_servo_attach(self):
        self.arm.set_servo_attach()
        
    '''
    设置伺服断开函数
    '''
    def Arm_Set_servo_detach(self):
        self.arm.set_servo_detach()
        
    '''
    返回机械臂当前坐标
    '''
    def Arm_Get_Position(self):
        return self.arm.get_position()

    '''
    回归待抓取位置
    '''    
    def Arm_Beginning(self):
        self.arm.set_position(x=115, y=-3, z=45)


if __name__ == "__main__":
    Swift = Arm()
    # 复位
    Swift.Arm_Reset()
    # ########################机械臂掉电#############################
    Swift.Arm_Set_servo_detach()
    time.sleep(5)

    # 移动机械臂后机械臂上电
    Swift.Arm_Set_servo_attach()
    print("当前机械臂xyz坐标:", Swift.arm.get_position())
