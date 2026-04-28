from tools.databus.bus import workFlow
from plugin.web.flask_app import flaskPluginRegist
from plugin.rec.img_get import imgGetPluginRegist
from plugin.rec.img_rec import imgRecPluginRegist
from plugin.embd.embd_control import emdPluginRegist
import multiprocessing as mp
from plugin.task_type import TaskType
from tools.log import log
from tools.config import config as cfg

if __name__ == "__main__":
    htop = "127.0.0.1"
    port = 8080

    q_flask = mp.Manager().Queue(1)  # 传递识别结果到网页
    q_img = mp.Manager().Queue(1)    # 获取摄像头图像
    q_rec = mp.Manager().Queue(1)    # 识别结果
    full_dict = mp.Manager().dict()  # 全局数据共享
    q_send = mp.Manager().Queue(2)   # 发送控制指令消息队列

    full_dict[cfg.FRUIT_LIAB] = "苹果"
    full_dict[cfg.PRESSURE_SENSOR_DATA] = 10

    mapOpenPlugin = dict()
    mapClosePlugin = dict()

    mapOpenPlugin[TaskType.IMAGE_GET_TASK] = (imgGetPluginRegist,        # 图像获取插件
                                              (q_flask, q_img, q_rec, full_dict))

    mapOpenPlugin[TaskType.IMAGE_REC_TASK] = (imgRecPluginRegist,        # 图像识别插件
                                              (q_img, q_rec))

    for plugin in mapOpenPlugin:
        log.info(str(plugin) + "启动成功~")
        taskFunc, taskArgs = mapOpenPlugin[plugin]
        taskFunc(*taskArgs)          # 提交任务
        workFlow.busStart()
