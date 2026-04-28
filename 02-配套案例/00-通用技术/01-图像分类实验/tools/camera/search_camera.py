import numpy as np
from socket import *
import cv2

def getHostIp():
    import socket
    """
    查询本机ip地址
    :return: ip
    """
    ip = ""
    s = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        print(e)
    finally:
        s.close()
    return ip

# 获取网络摄像头IP
def getCameraIp():
    # hostIP本机IP
    hostIP = getHostIp()
    print("hostIP:", hostIP)
    # 修复获取不到某些格式的IP地址,
    # 注意默认小车网关IP地址需要满足 格式 192.168.xxx.YYY  xxx可以是一位数、两位数、三位数
    tmp = hostIP.split('.')
    hostIP = '.'.join(tmp[:-1]+['', ])
    PORT = 8600
    BUFSIZE = 1024

    udpCliSock = socket(AF_INET, SOCK_DGRAM)
    udpCliSock.bind(('', 0))
    # udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, str("wifi0" + '\0').encode('utf-8'))

    udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    print('Listening for broadcast at ', udpCliSock.getsockname())
    udpCliSock.settimeout(.3)  # 设置连接超时等待时间
    send_pack = np.ones((4,), np.uint8)
    send_pack[0] = ord('D')
    send_pack[1] = ord('H')

    # 小车网络摄像头在8600端口开放了一个udp协议的服务，向该端口发送指定命令，可以得到网络摄像头的基本信息
    cameraIP = None
    for i in range(100, 254):
        try:
            udpCliSock.sendto(send_pack.tobytes(), (hostIP + str(i), PORT))
            print(hostIP+str(i))
            data = udpCliSock.recvfrom(BUFSIZE)
            if data[0][:2].decode("UTF-8") == "DH":
                print(data[0])
                cameraIP = data[0][4:19].decode("UTF-8").strip("\x00")
                print(cameraIP)
                udpCliSock.close()
                break
        except Exception as e:
            print(e)
    return cameraIP.strip("\x00")

# 获取MIPI摄像头图像
class MIPICamera():
    def __init__(self):
        try:
            from jetcam.csi_camera import CSICamera
            self.camera = CSICamera(width=640, height=480)
        except:
            print("没有安装jetcam软件包！！")

    def read(self):
        try:
            res = True
            return res, self.camera.read()
        except:
            res = False
            print("没有MiPi摄像头！！")
            return res, None

    def isOpened(self):
        try:
            self.camera.read()
            return True
        except:
            return False


# 设置图像获取模式
# rtsp 为小车网络摄像头获取
# 若传入参数为数字则切换为USB摄像头
# 若传入参数为空则使用图片
def setCamera(model=''):
    if model == 'rtsp':
        cameraIP = getCameraIp()
        prot = '10554'
        play_adder = '/tcp/av0_1'
        rtsp_adder = ''.join(('rtsp://', 'admin:888888@', cameraIP, ':', prot, play_adder))
        print("rtsp_addder", rtsp_adder)
        return cv2.VideoCapture(rtsp_adder)
    elif model == 'auto':
        cap_flag = ""
        for i in range(1, 5):
            cap = cv2.VideoCapture(int(i))
            if cap.isOpened():
                cap_flag = cap
                break
        if cap_flag == "":
            cap = MIPICamera()
            red,_ = cap.read()
            if cap.isOpened() and red:
                print("MIPI摄像头可以！！")
                cap_flag = cap
            else:
               cap = cv2.VideoCapture(0)
               if cap.isOpened():
                    cap_flag = cap
        return cap_flag
    elif model == "mipi":
        return MIPICamera()
    elif model != "":
        cap_flag = ""
        cap = cv2.VideoCapture(int(model))
        if not cap.isOpened():
            for i in range(5):
                cap = cv2.VideoCapture(int(i))
                if cap.isOpened():
                    cap_flag = cap
                    break
        else:
            cap_flag = cap
        return cap_flag
    else:
        return model