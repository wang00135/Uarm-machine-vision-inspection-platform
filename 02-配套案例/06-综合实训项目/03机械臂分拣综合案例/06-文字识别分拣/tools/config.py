import os

labels = {
    # "fruits_labels": ["背景", "芒果", "苹果", "西兰花", "洋葱"],
    # "electronic_labels": ["背景", "电感", "电容", "电阻", "开关"],
    "electron_labels": ["电容", "电感", "发光二极管", "电阻", "开关", "蜂鸣器"],

    "commodity_labels": ["背景", "橙汁", "面条", "牛奶", "薯片", "雪碧"],

    "garbage_labels": ["背景", "菜叶", "大骨头", "电池", "废纸箱",
                       "筷子", "抹布", "牛奶盒", "苹果核",
                       "塑料瓶", "香蕉皮", "烟蒂", "药丸",
                       "易拉罐", "油漆桶", "鱼骨头", "注射器"],

    # "FRUITS_LABEL": [" ", "鸡", "狗", "牛", "苹果", "芒果", "石榴",
    #                  "白菜", "洋葱", "西兰花", "福特", "别克", "宝马",
    #                  "中国", "百科荣创", "人工智能", "ldentify", "quantity", "China"],
    "fruits_labels": [" ", " ", " ", " ", "苹果", "芒果", "石榴",
                      " ", " ", " ", " ", " ", " ",
                      " ", " ", " ", " ", " ", " "],

    "vegetables_labels": [" ", " ", " ", " ", " ", " ", " ",
                          "白菜", "洋葱", "西兰花", " ", " ", " ",
                          " ", " ", " ", " ", " ", " "],

    "animals_labels": [" ", "鸡", "狗", "牛", " ", " ", " ",
                       " ", " ", " ", " ", " ", " ",
                       " ", " ", " ", " ", " ", " "],

    "car_labels": [" ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", "福特", "别克", "宝马",
                   " ", " ", " ", " ", " ", " "],


    "Chinese_labels": [" ", " ", " ", " ", " ", " ", " ",
                       " ", " ", " ", " ", " ", " ",
                       "中国", "百科荣创", "人工智能", "ldentify", "quantity", "China"],

    "English_labels": [" ", " ", " ", " ", " ", " ", " ",
                       " ", " ", " ", " ", " ", " ",
                       " ", " ", " ", "ldentify", "quantity", "China"],

    "workpiece_labels":['齿轮', '销钉', '六角螺栓', '垫片', '螺钉', '螺柱', '螺母', 
        '膨胀螺丝钩', '铆钉', '双头螺栓'],


}

cfg = {
    # "electron_model_path": "./models/electron.tflite",
    # "electron_labels": labels["electron_labels"],
    #
    # "fruits_model_path": "./models/fruits_model.tflite",
    # "fruits_labels": labels["fruits_labels"],
    #
    # "vegetables_model_path": "./models/fruits_model.tflite",
    # "vegetables_labels": labels["vegetables_labels"],
    #
    # "animals_model_path": "./models/fruits_model.tflite",
    # "animals_labels": labels["animals_labels"],
    #
    # "car_model_path": "./models/fruits_model.tflite",
    # "car_labels": labels["car_labels"],

    "Chinese_model_path": "./resource/models/fruits_model.tflite",
    "Chinese_labels": labels["Chinese_labels"],

    "English_model_path": "./resource/models/fruits_model.tflite",
    "English_labels": labels["English_labels"],

    # # "electronic_model_path": "./models/electronic_model.tflite",
    # "garbage_model_path": "./models/garbage_model.tflite",
    # "garbage_labels": labels["garbage_labels"],
    #
    # "commodity_model_path": "./models/commodity.tflite",
    # "commodity_labels": labels["commodity_labels"],
    #
    # "workpiece_model_path": "./models/workpiece.tflite",
    # "workpiece_labels": labels["workpiece_labels"],

    "yolo_model_path": "./resource/models/yolox_nano_det.onnx",
    # "electronic_labels": labels["electronic_labels"],
    "camera_id": 0,
    "com_id": '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_95634303432351E0C221-if00',
    "top_left": (160, -60),
    "lower_right": (245, 60),
    "width": 224,
    "height": 224,
    "place_y": 165,
    "place_z": 53,
    "grab_z": 23,
    "place_x_orange": 3,
    "place_x_red": 85,
    "place_x_blue": 170,
    "place_x_green": 260,
    "color_channel": 3,
}

class Config:
    UART_BAUDRATE = 115200
    UART_TIMEOUT = 3
    IMG_SIZE = "IMG_SIZE"   # 图像大小

    LOG_LEVEL_STDOUT = "info"
    LOG_LEVEL_FILE = "info"
    # LOG_SAVE_FLODER = os.path.join(BASE_PATH, "bkrc_car_log")
    LOG_FLAGE = False

    IMG_DIS_FLAGE = True
    CAMERA_MODE = "auto"
    Uart_Port = "/dev/ttyS4"

    ORIGINAL_IMAGE = 'ORIGINAL_IMAGE'
    REC_IMAGE = "REC_IMAGE"

    # 机械臂参数校准   X    Y    Z    旋转角
    SERVO_START_MOVE = "SERVO_START_MOVE"   # 是否启动机械臂搬运
    SERVO_OBJ_VAL = [4.8, 11.5, 3.2, [810, 895, 970]]
    SERVO_LIB_VAL = [6 - 0.8, 25, 7, 500]
    SERVO_INIT_VAL = [90, 150, 10, 510]
    SERVO_PIDCH = -13  # 仓库3号位置俯仰角
    X_BIAS = 0  # 坐标映射X轴偏置
    Y_BIAS = 0  # 坐标映射Y轴偏置

    # 全局共享参数配置
    IMG_DET_XY = "IMG_DET_XY"  # 矩形框中心坐标位置映射

    SORTING_MODE = "SORTING_MODE"  # 分拣模式执行标志（[True/False 开启或关闭, 1(手动分拣) 2（自动分拣）]）
    SORTING_VAL = "SORTING_VAL"  # 分拣状态标志 ([1, 2, 3]货物, [1, 2, 3]仓库 [2, 1]搬运操作)

    IMG_COM = 0        # 图像识别模式索引
    CARGO_COM = 1      # 货物指令存放索引
    WAREHOUSE_COM = 2  # 仓库指令存放索引
    MOVE_COM = 3       # 移动指令存放索引

    MODE = 0       # 模式  （True为搬运到的位置）
    CARGO = 1      # 货物
    WAREHOUSE = 2  # 仓库

    ZOON_REC = 1   # 动物识别
    FRUIT_REC = 2  # 水果识别
    VEG_REC = 3    # 蔬菜识别
    CARLOGO_REC = 4  # 车标识别
    CH_REC = 5   # 汉字识别
    EN_REC = 6   # 英文识别

    DET_REC = 0        # 物体检测模式
    ELECTRON_REC = 1   # 电子元器件识别模式
    FRUITS_REC = 2     # 果蔬识别模式
    GARBAGE_REC = 3    # 垃圾分拣模式
    COLOR_REC = 4      # 色块分拣模式
    SHAPE_REC = 5      # 形状识别模式
    SIZE_REC = 6       # 尺寸测量模式
    ANGLE_REC = 7      # 角度测试模式
    AREA_REC = 8       # 面积测量模式
    COLOR_THE = -1     # 颜色阈值调整

    # 摄像头标定参数存储路径
    CALIBRATION_PARAM_PATH = "./tools/camera_calibration/calibration_param.npz"

    # 摄像头映射参数存储路径
    MAP_PARAM_PATH = "./tools/camera_calibration/map_param.npz"

    # lab颜色阈值
    LAB_FILE_PATH = './resource/lab_config.yaml'

config = Config()
