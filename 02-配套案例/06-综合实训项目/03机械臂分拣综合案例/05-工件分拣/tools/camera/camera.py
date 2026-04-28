# encoding:utf-8
import cv2
import time
import threading
import numpy as np
from tools.camera.search_camera import setCamera
from tools.config import config

class Camera:
    def __init__(self, resolution=(640, 480), calibration_param_path=None):
        self.cap = None
        self.width = resolution[0]
        self.height = resolution[1]
        self.frame = None
        self.opened = False

        self.camera_location_flag = False  # 摄像头位置调整标志位

        # 加载参数
        self.param_data = np.load(calibration_param_path)
        
        # 获取参数
        self.mtx = self.param_data['mtx_array']
        self.dist = self.param_data['dist_array']
        self.newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist,
                                                               (self.width, self.height),
                                                               0, (self.width, self.height))

        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None,
                                                           self.newcameramtx, (self.width,self.height), 5)
        
        self.th = threading.Thread(target=self.camera_task, args=(), daemon=True)
        self.th.start()

    def camera_open(self):
        try:
            self.cap = setCamera(config.CAMERA_MODE)
            # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_SATURATION, 40)
            self.opened = True
        except Exception as e:
            print('打开摄像头失败:', e)

    def camera_close(self):
        try:
            self.opened = False
            time.sleep(0.2)
            if self.cap is not None:
                self.cap.release()
                time.sleep(0.05)
            self.cap = None
        except Exception as e:
            print('关闭摄像头失败:', e)

    def camera_task(self):
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()
                    if ret:
                        # frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
                        # 调整图像，进行ROI，获取分拣区域图像
                        frame_resize = frame_tmp[int(frame_tmp.shape[0] / 4.6): int(frame_tmp.shape[0] - frame_tmp.shape[0] / 2.7),
                                 int(frame_tmp.shape[1] / 3.4): int(frame_tmp.shape[1] - frame_tmp.shape[1] / 4.5)]
                        frame_resize = cv2.resize(frame_resize, (self.width, self.height), interpolation=cv2.INTER_NEAREST)

                        self.frame = cv2.remap(frame_resize, self.mapx, self.mapy, cv2.INTER_LINEAR)
                        if self.camera_location_flag:
                            h, w = self.frame.shape[:2]
                            cv2.line(self.frame, (0, int(h / 2)), (w, int(h / 2)), (0, 0, 255), 2)
                            cv2.line(self.frame, (int(w / 2), 0), (int(w / 2), h), (0, 0, 255), 2)
                    else:
                        print(1)
                        self.frame = None
                        cap = setCamera(config.CAMERA_MODE)
                        ret, _ = cap.read()
                        if ret:
                            self.cap = cap
                elif self.opened:
                    print(2)
                    cap = setCamera(config.CAMERA_MODE)
                    ret, _ = cap.read()
                    if ret:
                        self.cap = cap              
                else:
                    time.sleep(0.01)
            except Exception as e:
                print('获取摄像头画面出错:', e)
                time.sleep(0.01)


if __name__ == '__main__':
    my_camera = Camera(calibration_param_path="../CameraCalibration/calibration_param.npz")
    my_camera.camera_open()
    # my_camera.camera_location_flag = True
    while True:
        img = my_camera.frame
        if img is not None:
            cv2.imshow('img', img)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()
