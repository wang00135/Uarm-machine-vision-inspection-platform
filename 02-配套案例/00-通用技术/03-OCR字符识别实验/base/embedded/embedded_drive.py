import time
from tools.log import log
import threading
import multiprocessing as mp
import numpy as np
from tools.config import config as cfg

def controlEmbedded(embd_drive, rec_data):

    """
    根据模型识别结果控制嵌入式设备
    :param rec_data: AI模型识别结果
    :return: 所执行的控制指令
    """
    embd_drive.buzzer(rec_data)

def getEmbeddedData(data_msg=None):
    """
    获取嵌入式设备的数据（根据功能提取数据）
    :return: 解析的数据
    """
    """
    0x55 0xCC（包头）
    0xXX（温度整数）
    0xXX（温度小数）
    0xBB（包尾）
    """
    temp = str(data_msg[2]) + "." + str(data_msg[3])
    print("temp:", temp)
    return temp

class DataReadThread(threading.Thread):
    def __init__(self, client, full_data=None):
        """
        嵌入式系统数据接收线程
        :param client: wifi/usart的对象 用于获取datRead函数
        """
        threading.Thread.__init__(self)
        self.full_data = full_data
        self.client = client
        self.flag = True

    def setFlag(self, flag:bool):
        self.flag = flag

    def run(self):
        while self.flag:
            time.sleep(0.2)
            dat_msg = self.client.datRead()

            # 获取温度传感器数据
            self.full_data[cfg.TEMP_VALUE] = getEmbeddedData(dat_msg)
            log.info(self.full_data[cfg.TEMP_VALUE])

class DataSendThread(threading.Thread):
    def __init__(self, client, q_send: mp.Queue):
        """
        嵌入式系统控制指令发送线程
        :param client: wifi/usart的对象 用于获取send函数
        """
        threading.Thread.__init__(self)
        self.q_send = q_send
        self.client = client
        self.flag = True

    def setFlag(self, flag: bool):
        self.flag = flag

    def run(self):
        # 获取消息队列并发送
        while self.flag:
            if self.q_send.empty():
                continue
            else:
                dat = self.q_send.get()
                log.info(dat)
                self.client.send(dat)

def embeddedDataThreadRun(client, q_send=None, full_data=None):
    """
    嵌入式系统数据发送与接收线程启动
    :param client: wifi/usart的对象
    :param q_send: 发送数据的消息队列
    :param full_data: 全局共享数据dict
    :return:
    """
    try:
        read_thread = DataReadThread(client, full_data)
        send_thread = DataSendThread(client, q_send)
        read_thread.start()
        send_thread.start()
        log.info("嵌入式系统数据接收和发送线程启动成功！！")
    except:
        log.error("嵌入式系统数据接收和发送线程启动失败!!")

class EmbdDrive(object):
    def __init__(self, q_send:mp.Queue, with_flag=True):
        """
        无人车运动控制及沙盘标志物控制函数
        :param q_send: 用于传达发送控制数据（此消息队列通过线程的方式自动发送）
        :param with_flag: 是否开启
        """
        self.with_flag = with_flag
        self.q_send = q_send

    def datSend(self, comm1):
        send_dat = np.zeros((4,), np.uint8)
        send_dat[0] = 0x55
        send_dat[1] = 0xDD
        send_dat[2] = comm1
        send_dat[3] = 0xBB
        if not self.q_send.full():
            self.q_send.put(send_dat)

    """
    嵌入式系统控制指令
    """
    def buzzer(self, dat=0):
        """
		0x55 0xDD（包头）
		0xXX（0x01：蜂鸣器报警：0x00：蜂鸣器关闭）
		0xBB（包头）
        """
        send_dat = np.zeros((4,), np.uint8)
        send_dat[0] = 0x55
        send_dat[1] = 0xDD
        send_dat[2] = dat
        send_dat[3] = 0xBB

        if not self.q_send.full():
            self.q_send.put(send_dat)

if __name__ == "__main__":
    import time
    from base.embedded import clientMode
    clien = clientMode(cline_mode="uart")
    q_send = mp.Manager().Queue(2)
    full_dict = mp.Manager().dict()       # 全局数据共享

    emb_dat = EmbdDrive(q_send)
    embeddedDataThreadRun(clien, q_send, full_dict)

    while True:
        time.sleep(0.5)
        emb_dat.buzzer(1)