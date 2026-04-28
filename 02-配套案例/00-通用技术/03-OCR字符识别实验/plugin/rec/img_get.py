from tools.camera.search_camera import setCamera
from multiprocessing import Queue
import threading
import cv2
from tools.log import log
from base.components.config import ai_cfg
from tools.databus.bus import workFlow
from base.ocr_rec import recImgDis
from tools.config import config
from base.embedded.embedded_drive import controlEmbedded, EmbdDrive

class VideoThread(threading.Thread):
    def __init__(self, camera="0", q_flask:Queue=None, q_img:Queue=None,
                 q_rec:Queue=None, q_send=None, full_dict=None):
        threading.Thread.__init__(self)
        self.cap = setCamera(camera)    # 网络摄像头
        self.q_flask = q_flask          # 消息队列传递绘制识别结果后的图像到web显示插件
        self.q_img = q_img              # 消息队列传递原始图像到识别插件
        self.q_rec = q_rec              # 消息队列传递AI模型的推理结果

        self.full_dict = full_dict
        # self.embdDrive = EmbdDrive(q_send)

    def run(self):
        ocr_pricet = []
        while True:
            if self.cap != "":
                ret, frame = self.cap.read()
                frame = cv2.resize(frame, (ai_cfg.CAM_WIDTH, ai_cfg.CAM_HEIGHT))

                # 原始图像传递
                if not self.q_img.full() and not frame is None:
                    self.q_img.put(bytearray(frame))

                # 识别结果绘制
                if not self.q_rec.empty():
                    ocr_pricet = self.q_rec.get()

                frame, ocr_str = recImgDis(frame, ocr_pricet)

                self.full_dict[config.OCR_STR] = ocr_str

                print("frame_shape:", frame.shape)

                # 传递图像到web显示界面中
                if not self.q_flask.full() and not frame is None:
                    self.q_flask.put(bytearray(frame))

                if config.IMG_DIS_FLAGE:
                    cv2.imshow("frame", frame)
                c = cv2.waitKey(5) & 0xff
                if c == 27:
                    break

class ImageGet(object):
    def __init__(self):
        pass

    def onExit(self):
        pass

    def worker(self, q_flask:Queue=None, q_img:Queue=None, q_rec:Queue=None,
               q_send=None, full_dict=None):
        self.video_thread = VideoThread(config.USB_CAMERA_INDEX, q_flask, q_img,
                                        q_rec, q_send, full_dict)
        log.info("图像获取线程已启动！！")
        self.video_thread.start()

def imgGetPluginRegist(q_flask:Queue=None, q_img:Queue=None,
                       q_rec:Queue=None, q_send=None, full_dict=None):
    img_get_plugin = ImageGet()
    workFlow.registBus(img_get_plugin.__class__.__name__,
                       img_get_plugin.worker,
                       (q_flask, q_img, q_rec, q_send, full_dict),
                       img_get_plugin.onExit)

if __name__ == "__main__":
    import multiprocessing as mp

    q_flask = mp.Queue(1)
    q_img = mp.Queue(1)
    q_rec = mp.Queue(1)
    imageGet = ImageGet()
    imageGet.worker(q_flask, q_img, q_rec)
