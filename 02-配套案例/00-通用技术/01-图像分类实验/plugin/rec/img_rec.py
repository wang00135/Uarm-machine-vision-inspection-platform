from multiprocessing import Queue
import threading
from tools.log import log
from tools.databus.bus import workFlow
import numpy as np
from base.components.config import ai_cfg
from base.fruits_detecte_rec import FruitDetect

class FruitDectectRecThread(threading.Thread):
    def __init__(self, q_img:Queue=None, q_rec:Queue=None, model_path=ai_cfg.FRUITS_MODEL_PATH):
        threading.Thread.__init__(self)
        self.q_img = q_img              # 消息队列传递 原始图像到识别插件
        self.q_rec = q_rec              # 消息队列传递 AI模型的推理结果
        self.fruit_detecte_rec = FruitDetect(model_path=model_path)  # 图像处理

    def run(self):
        while True:
            if self.q_img.empty():
                continue
            else:
                image = self.q_img.get()
                if image != False:
                    image = np.array(image).reshape(ai_cfg.CAM_HEIGHT, ai_cfg.CAM_WIDTH, 3)
                else:
                    break

            fruit_detecte_pricet = self.fruit_detecte_rec.inference(image)
            if self.q_rec.full():
                continue
            else:
                self.q_rec.put(fruit_detecte_pricet)


class ImageRec(object):
    def __init__(self):
        pass

    def onExit(self):
        pass

    def worker(self, q_img:Queue=None, q_rec:Queue=None):
        self.fruit_detecte_thread = FruitDectectRecThread(q_img, q_rec)
        log.info("图像识别线程已启动！！")
        self.fruit_detecte_thread.start()


def imgRecPluginRegist(q_img:Queue=None, q_rec:Queue=None):
    img_rec_plugin = ImageRec()
    workFlow.registBus(img_rec_plugin.__class__.__name__,
                       img_rec_plugin.worker,
                       (q_img, q_rec),
                       img_rec_plugin.onExit)


if __name__ == "__main__":
    import multiprocessing as mp
    q_img = mp.Queue(1)
    q_rec = mp.Queue(1)
    imageGet = ImageRec()
    imageGet.worker(q_img, q_rec)
