from socket import socket, SOCK_STREAM,\
    AF_INET, SOCK_DGRAM
import numpy as np
from base.embedded.constant import *
from tools.log import log

plate_label = ["京" , "津", "沪" , "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新",
         "苏", "浙", "赣", "鄂", "桂", "甘", "晋", "蒙", "陕", "吉", "闽", "贵", "粤", "青",
         "藏", "川", "宁", "琼"]

class WifiConfig(object):
    def __init__(self):
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            print("ip:", ip)
        finally:
            s.close()

        tmp = ip.split('.')

        carip = '.'.join(tmp[:-1] + ['', ]) + str(1)
        self.server_adder = (carip, 60000)
        log.info(self.server_adder)

        # AF_INET表示IPV4地址，SOCK_STREAM表示走TCP
        self.client = socket(AF_INET, SOCK_STREAM)

        # 建立连接
        self.client.connect(self.server_adder)

    def _checkData(self, pack_length=FRAME_LEN):
        while True:
            dat_buf = self.client.recv(pack_length)
            if len(dat_buf) == FRAME_LEN and dat_buf[0] == FRAME_HEAD:
                break
            else:
                log.error("skip error package!!")
        return dat_buf

    def datRead(self):
        wifi_msg = self._checkData()
        return wifi_msg

    def send(self, send_dat):
        self.client.send(send_dat)

    def gatePlate(self, plt="京123456"):
        # 道闸显示车牌信息
        # if len(plt) > 6:
        #
        #     log.info("--plate_len_err!!")
        # else:
        plate = list(map(ord, plt))
        dat = 0x01
        for i, str in enumerate(plate_label):
            if str == plate[0]:
                dat = hex(int(str(i), 16))

        a, b, c, d, e, f = plate
        send_dat = np.zeros((4,), np.uint8)
        send_dat[0] = 0x55
        send_dat[1] = 0xDD
        send_dat[2] = 0x01
        send_dat[3] = dat

        send_dat[4] = a
        send_dat[5] = b
        send_dat[6] = c
        send_dat[7] = d
        send_dat[8] = e
        send_dat[9] = f

        send_dat[10] = 0x01
        send_dat[11] = 0xBB

        self.send(send_dat)

if __name__ == "__main__":
    import time
    wifi = WifiConfig()
    while True:
        time.sleep(0.3)
        wifi.gatePlate()