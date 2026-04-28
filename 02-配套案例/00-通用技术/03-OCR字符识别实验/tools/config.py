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
    LOG_SAVE_FLODER = os.path.join(BASE_PATH, "bkrc_log")
    LOG_FLAGE = False

    OCR_REC = True

    IMG_DIS_FLAGE = True
    USB_CAMERA_INDEX = "auto"
    CLINET_MODE = "uart"

    # 全局共享参数配置
    OCR_STR = "OCR_STR"  # 是否佩戴口罩

config = Config()
