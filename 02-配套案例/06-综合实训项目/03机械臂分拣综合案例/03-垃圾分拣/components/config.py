
class AI_Config:
    # 基本设置
    window_name = "AI_RUN"

    CAM_HEIGHT = 480
    CAM_WIDTH = 640
    REC_INPUT_SIZE = (224, 224)
    BOX_INPUT_SIZE = (120, 160)  # (h, w)
    DET_INPUT_SIZE = (416, 416)

    HELMET_CLASSES = ("box", )
    BOX_CLASSES = ['background', 'box']

    # 模型标签
    GARBAGE_LABELS = ["菜叶", "大骨头", "电池", "废纸箱",
                     "筷子", "抹布", "牛奶盒", "苹果核",
                     "塑料瓶", "香蕉皮", "烟蒂", "药丸",
                     "易拉罐", "油漆桶", "鱼骨头", "注射器"]

    # 检测模型配置
    FEAT_STRIDE_FPN = [8, 16, 32]
    THRESHOLD = 0.5

    # YOLOX目标检测模型配置
    NMS_THR = 0.45
    SCORE_THR = 0.1
    DIS_THR = 0.3

    # SLIM-SSD目标检测模型配置
    # anchor配置
    MIN_SIZES = [[10, 16, 24], [32, 48], [64, 96], [100, 110, 128]]

    STEPS = [8, 16, 32, 64]
    MATCH_THRESH = 0.45
    VARIANCES = [0.1, 0.2]
    CLIP = False

    # 推理
    SCORE_THRESHOLD = 0.95   # 得分阈值
    NMS_THRESHOLD = 0.95     # nms阈值

    # 模型路径
    GARBAGE_REC_PATH = "./resource/model_zoo/garbage_model.tflite"
    BOX_DET_PATH = "./resource/model_zoo/box_160x120.tflite"


    FONT_PATH = "./resource/font/simsun.ttc"
    FONT_SIZE = 30

ai_cfg = AI_Config()
