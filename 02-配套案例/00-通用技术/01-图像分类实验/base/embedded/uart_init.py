import serial
import serial.tools.list_ports
from tools.log import log
from base.embedded.constant import *

class UartConfig(object):
    @staticmethod
    def _search_isenable_serial():
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            return None
        else:
            plist_0 = list(plist[0])
            return plist_0[0]

    def __init__(self, baud=115200, timeout=3):
        super(UartConfig, self).__init__()
        self.uart_baudrate = baud
        self.uart_timeout = timeout
        self._is_init = False
        self.uart_port = UartConfig._search_isenable_serial()
        try:
            self.uart_client = serial.Serial(self.uart_port,
                                             self.uart_baudrate,
                                             timeout=self.uart_timeout)
            log.info("串口初始化成功！！")
        except:
            log.error("uart_init_err!!")

    def _checkData(self, pack_length=FRAME_LEN):
        while True:
            dat_buf = self.uart_client.read(pack_length)
            print("dat_buf:", dat_buf)
            if len(dat_buf) == FRAME_LEN and dat_buf[0] == FRAME_HEAD:
                break
            else:
                print('skip error package')
        return dat_buf

    def datRead(self):
        uart_msg = self._checkData()
        return uart_msg

    def send(self, send_dat):
        self.uart_client.write(send_dat)
        self.uart_client.flush()
