import multiprocessing as mp
from embedded.auto_move import ArmServo
from multiprocessing import Process, Queue
from tools.config import config as cfg
from ai_lib.components.config import ai_cfg
from PyQt5 import QtWidgets
from pyqt_ui.main_ui_ctl import MainWindow
import sys
import time
import cv2

def embdTask(full_dict):
    # uArm机械臂控制
    arm_servo = ArmServo(full_dict, './resource/arm_polar.yaml')

    arm_std = full_dict['arm_ctr_val'][2]
    angle_buf = full_dict['arm_ctr_val'][1][-1]

    while True:
        arm_ctr_val = full_dict['arm_ctr_val']

        sorting_mode = full_dict[cfg.SORTING_MODE]
        sorting_val = full_dict[cfg.SORTING_VAL]


        # 机械臂分拣控制
        xya_val = full_dict[cfg.IMG_DET_XY]

        if xya_val and sorting_mode[0]:
            print("sorting_val[cfg.MOVE_COM][2]:", sorting_val[cfg.MOVE_COM][2])
            if not sorting_mode[1]:   # 自动执行模式
                print("-----自动执行模式！")
                arm_servo.imgRecCtr(xya_val[0], xya_val[1], auto=True)

            elif sorting_val[cfg.MOVE_COM][2] != -1:  # 手动执行模式
                print("-----手动执行模式！")
                arm_servo.imgRecCtr(xya_val[0], sorting_val[cfg.MOVE_COM][2], auto=False)
                sorting_val[cfg.MOVE_COM][2] = -1

            full_dict[cfg.IMG_DET_XY] = []
            full_dict['rec_index'] = -1
            full_dict[cfg.SORTING_VAL] = sorting_val
            full_dict['img_rec_flag'] = True

        # 机械臂控制
        if arm_ctr_val[0]:
            arm_ctr_val[0] = False

            # 提取控制参数
            x, y, z = arm_ctr_val[1][:3]
            angle = arm_ctr_val[1][-1]
            buzz, pump, gripper = arm_ctr_val[2]

            # 控制机械臂指定坐标移动
            arm_servo.servosMove((x, y, z), 15, False)

            # 角度控制
            if angle_buf != angle:
                angle_buf = angle
                arm_servo.servoAngle(angle, wait_flag=False)

            # 蜂鸣器、吸盘、电动夹控制
            if arm_ctr_val[2] != arm_std:
                arm_std = arm_ctr_val[2]
                arm_servo.armClampBlock(gripper, movetime=15)
                arm_servo.armClampBlock(pump, mode=2, movetime=15)
                if buzz:
                    arm_ctr_val[2][0] = False
                    arm_servo.armBuzzer(2)

            # 伺服电机断电控制
            arm_st = arm_ctr_val[3]
            if arm_st['std']:
                arm_st['std'] = False
                arm_servo.armServoSwitch(arm_st['val'][0])
                if arm_st['val'][0]:
                    print(arm_servo.armGetPolar())
                    yxz = arm_servo.armGetPolar()
                    xyz = [yxz[1], yxz[0], yxz[2]]
                    arm_servo.arm_polar_val[arm_st['val'][1]]['xyz'] = xyz
                    arm_servo.arm_polar_val[arm_st['val'][1]]['angle'] = angle
                    arm_servo.saveYamlData(arm_servo.arm_polar_val, './resource/arm_polar.yaml')
                    print("arm_servo.arm_polar_val:", arm_servo.arm_polar_val)

            full_dict['arm_ctr_val'] = arm_ctr_val


def aiTask(full_dict=None):
    from ai_lib.box_detect import BoxDetectRec, recImgDis
    from tools.camera.camera import Camera
    from ai_lib.color_rec import ColorRec
    from ai_lib.shapedetector import ShapeDetector
    from ai_lib.angle_det import AngleDetector
    from ai_lib.size_rec import SizeDetector
    from ai_lib.area_rec import AreaDetector

    camera = Camera(calibration_param_path="./resource/camera_calibration/calibration_param.npz")
    camera.camera_open()
    camera.camera_location_flag = False

    color_rec = ColorRec(map_param_path='./resource/camera_calibration/map_param.npz',
                         lab_file_path='./resource/lab_config.yaml')

    shape_det = ShapeDetector(lab_file_path='./resource/lab_config.yaml')
    angle_det = AngleDetector(lab_file_path='./resource/lab_config.yaml')
    size_det = SizeDetector(lab_file_path='./resource/lab_config.yaml')
    area_det = AreaDetector(lab_file_path='./resource/lab_config.yaml')
    box_det_rec = BoxDetectRec(ai_cfg.BOX_DET_PATH, cfg.MAP_PARAM_PATH)

    count = 0

    # color_flag = True

    while True:
        img = camera.frame

        if img is not None:
            full_dict[cfg.ORIGINAL_IMAGE] = img

            # cp_img = img.copy()
            sorting_mode = full_dict[cfg.SORTING_MODE]
            sorting_val = full_dict[cfg.SORTING_VAL]

            # print("sorting_val:", sorting_val)

            if full_dict['img_rec_flag'] or not sorting_mode[0]:
                if sorting_val[cfg.IMG_COM] in [cfg.DET_REC, cfg.ELECTRON_REC,
                                                cfg.FRUIT_REC, cfg.GARBAGE_REC]:
                    if sorting_val[cfg.IMG_COM] == cfg.DET_REC:
                        # 物体检测模式
                        box_pricet = box_det_rec.inference(img, False)
                    else:
                        # 图像分类识别模式
                        box_pricet = box_det_rec.inference(img, True, img_mode=sorting_val[cfg.IMG_COM])

                    img, box_std = recImgDis(img, box_pricet)
                    if box_std["std"] != "none":
                        if box_std["box_coordin"]:
                            count += 1
                            if count > 20:
                                count = 0
                                # sorting_val = full_dict[cfg.SORTING_VAL]
                                sorting_val[cfg.CARGO_COM] = box_std["box_index"]
                                sorting_val[cfg.MOVE_COM][1] = 0
                                full_dict[cfg.SORTING_VAL] = sorting_val
                                print("corrdin:", box_std['box_coordin'], " box_st", box_std["box_index"])

                                if not sorting_val[cfg.IMG_COM] == cfg.DET_REC:
                                    full_dict['rec_index'] = box_std["box_index"][0]

                                full_dict[cfg.IMG_DET_XY] = [box_std["box_coordin"],  box_std["box_index"]]
                                full_dict['img_rec_flag'] = False
                        else:
                            count = 0
                        # print(box_std["box_index"], box_std['box_label'])

                    if sorting_mode[2]:  # 摄像头位置校准函数
                        img, _ = box_det_rec.adjust(img, box_std['boxs'])

                elif sorting_val[cfg.IMG_COM] == cfg.COLOR_REC:
                    camera.camera_location_flag = False
                    cp_img = img.copy()
                    rec_val = color_rec.imgRec(cp_img)
                    img = cp_img
                    if not rec_val is None:
                        full_dict[cfg.IMG_DET_XY] = rec_val
                        full_dict['img_rec_flag'] = False

                elif sorting_val[cfg.IMG_COM] == cfg.SHAPE_REC:
                    # 形状识别
                    camera.camera_location_flag = False
                    cp_img = img.copy()
                    img = shape_det.imgRec(cp_img)

                elif sorting_val[cfg.IMG_COM] == cfg.ANGLE_REC:
                    # 角度测量
                    camera.camera_location_flag = False
                    cp_img = img.copy()
                    img = angle_det.imgRec(cp_img)

                elif sorting_val[cfg.IMG_COM] == cfg.AREA_REC:
                    # 面积测量
                    camera.camera_location_flag = False
                    cp_img = img.copy()
                    img = area_det.imgRec(cp_img,  full_dict['get_val'])
                    if full_dict['get_val']:
                        full_dict['get_val'] = False

                elif sorting_val[cfg.IMG_COM] == cfg.SIZE_REC:
                    # 尺寸测量
                    camera.camera_location_flag = False
                    cp_img = img.copy()
                    img = size_det.imgRec(cp_img,  full_dict['get_val'])
                    if full_dict['get_val']:
                        full_dict['get_val'] = False

            # full_dict[cfg.SORTING_VAL] = sorting_val
            full_dict[cfg.REC_IMAGE] = img   # 识别结果可视化图像
            key = cv2.waitKey(1)

            # cv2.imshow('img', img)

            if key == 27:
                break

    camera.camera_close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    full_dict = mp.Manager().dict()       # 全局数据共享

    full_dict[cfg.ORIGINAL_IMAGE] = None
    full_dict[cfg.REC_IMAGE] = None

    full_dict['arm_ctr_val'] = [False,                       # 机械臂控制状态
                                [90, 150, 50, 90],           # x(45~180)、y(115~350)、z(-50~150)和旋转角度(0~180)
                                [False, False, False],       # 蜂鸣器、吸盘、电动夹控制状态
                                {'std': False, 'val': [False, None]}]  # 机械臂坐标设置

    full_dict[cfg.SORTING_MODE] = [False, 0, False]   # 开启分拣模式 自动模式 关闭摄像头校准

    full_dict['rec_index'] = -1

    full_dict['get_val'] = False
    full_dict['img_rec_flag'] = True

    # 图像识别模式  货物位置  仓库位置   搬运位置（模式 货物搬仓库，仓库搬货物，起始， 终止）
    full_dict[cfg.SORTING_VAL] = [0, [], [0, 1, 2, 3], [0, 0, -1]]

    # 目标检测物体坐标位置及旋转角
    full_dict[cfg.IMG_DET_XY] = []

    p_embd_task = Process(target=embdTask, args=(full_dict,))
    p_embd_task.start()

    p_ai_task = Process(target=aiTask, args=(full_dict,))
    p_ai_task.start()

    # p_embd_task.join()

    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow(full_dict=full_dict)
    #myshow.show()
    myshow.showMaximized()
    # myshow.showFullScreen()
    app.exec_()

    p_embd_task.terminate()
    p_ai_task.terminate()
