
class AI_Config:
    # 基本设置
    window_name = "OCR_REC"

    CAM_HEIGHT = 480
    CAM_WIDTH = 640

    INPUT_SIZE = (240, 320)  # (h, w)

    LABELS_LIST = ['background', '有口罩', '无口罩']

    # 模型路径
    DET_PATH = './resource/model_zoo/det_model.onnx'
    SMALL_REC_PATH = './resource/model_zoo/rec_model.onnx'
    LARGE_REC_PATH = './resource/model_zoo/rec_model.onnx'
    PPOCR_KEYS_PATH = './resource/model_zoo/ppocr_keys_v1.txt'
    FONT_PATH = "./resource/font/simsun.ttc"
    FONT_SIZE = 30

ai_cfg = AI_Config()

