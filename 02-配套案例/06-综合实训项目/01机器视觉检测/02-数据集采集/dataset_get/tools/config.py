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

    # 摄像头标定参数存储路径
    CALIBRATION_PARAM_PATH = "./tools/CameraCalibration/calibration_param.npz"

    # 摄像头映射参数存储路径
    MAP_PARAM_PATH = "./tools/CameraCalibration/map_param.npz"

    # lab颜色阈值
    LAB_FILE_PATH = './embedded/HiwonderSDK/lab_config.yaml'

config = Config()
