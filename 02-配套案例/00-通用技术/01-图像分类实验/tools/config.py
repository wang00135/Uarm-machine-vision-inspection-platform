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
    LOG_FLAGE = False  # log日志

    IMG_DIS_FLAGE = True  # 图像显示框
    USB_CAMERA_INDEX = "1"
    CLINET_MODE = "uart"

    # 全局共享参数配置
    PRESSURE_SENSOR_DATA = "pressure_sensor_data",  # 压力传感器数据
    FRUIT_DATA = "FRUIT_DATA"
    FRUIT_LIAB = "FRUIT_LIAB"

config = Config()
