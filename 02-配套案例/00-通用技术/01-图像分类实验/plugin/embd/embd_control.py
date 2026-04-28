from base.embedded.embedded_drive import embeddedDataThreadRun
from base.embedded import clientMode
import multiprocessing as mp
from tools.log import log
from tools.databus.bus import workFlow

class DataReadSend(object):
    def __init__(self):
        pass

    def onExit(self):
        pass

    # 执行函数，
    def worker(self, q_send:mp.Queue, full_data=None):
        clien = clientMode()
        embeddedDataThreadRun(clien, q_send, full_data)
        log.info("数据接收与发送进程启动成功！！")

# 构建plugin
def emdPluginRegist(q_send:mp.Queue, full_dict=None):
    img_get_plugin = DataReadSend()
    workFlow.registBus(img_get_plugin.__class__.__name__,
                       img_get_plugin.worker,
                       (q_send, full_dict),
                       img_get_plugin.onExit)
