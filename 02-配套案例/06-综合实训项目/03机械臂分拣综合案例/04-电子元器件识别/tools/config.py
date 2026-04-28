import os

# 获取前一级路径
# BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 获取当前路径
BASE_PATH = os.path.dirname(__file__)


class Config:
    UART_BAUDRATE = 115200
    UART_TIMEOUT = 3

    LOG_LEVEL_STDOUT = "info"
    LOG_LEVEL_FILE = "info"
    LOG_SAVE_FLODER = os.path.join(BASE_PATH, "bkrc_car_log")
    LOG_FLAGE = False

    IMG_DIS_FLAGE = True
    CAMERA_MODE = "auto"
    Uart_Port = "/dev/ttyS4"

    ORIGINAL_IMAGE = 'ORIGINAL_IMAGE'
    REC_IMAGE = "REC_IMAGE"

    # 机械臂参数校准   X    Y    Z    旋转角
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
    CALIBRATION_PARAM_PATH = "./resource/camera_calibration/calibration_param.npz"

    # 摄像头映射参数存储路径
    MAP_PARAM_PATH = "./resource/camera_calibration/map_param.npz"

    # lab颜色阈值
    LAB_FILE_PATH = './embedded/HiwonderSDK/lab_config.yaml'


config = Config()
