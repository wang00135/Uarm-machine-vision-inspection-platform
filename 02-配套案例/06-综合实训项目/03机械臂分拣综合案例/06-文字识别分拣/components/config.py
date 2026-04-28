
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
    ELECTRONIC_LABELS = ["背景", "电感", "电容", "电阻", "开关"]

    COMMODITY_LABELS = ["背景", "橙汁", "面条", "牛奶", "薯片", "雪碧"]

    GARBAGE_LABELS = ["背景", "菜叶", "大骨头", "电池", "废纸箱",
                     "筷子", "抹布", "牛奶盒", "苹果核",
                     "塑料瓶", "香蕉皮", "烟蒂", "药丸",
                     "易拉罐", "油漆桶", "鱼骨头", "注射器"]

    FRUITS_LABEL = [" ", " ", " ", " ", " ", " ", " ",
                    " ", " ", " ", " ", " ", " ",
                    "中国", "百科荣创", "人工智能", "ldentify", "quantity", "China"]

    # 检测模型配置
    FEAT_STRIDE_FPN = [8, 16, 32]
    THRESHOLD = 0.5

    # YOLOX目标检测模型配置
    NMS_THR = 0.45
    SCORE_THR = 0.1
    DIS_THR = 0.3

    # SLIM-SSD目标检测模型配置
    # anchor配置
    # MIN_SIZES = [[(9, 7), (24, 20), (39, 35)], [(54, 41), (65, 61), (81, 66)],
    #               [(94, 86), (113, 95), (131, 122)], [(137, 128), (172, 162), (176, 210)]]
    MIN_SIZES = [[10, 16, 24], [32, 48], [64, 96], [100, 110, 128]]

    STEPS = [8, 16, 32, 64]
    MATCH_THRESH = 0.45
    VARIANCES = [0.1, 0.2]
    CLIP = False

    # 推理
    SCORE_THRESHOLD = 0.95   # 得分阈值
    NMS_THRESHOLD = 0.95     # nms阈值
    # "max_number_keep": 200

    # 模型路径
    FRUIT_REC_PATH = "./resource/model_zoo/pt_fruits.tflite"
    BOX_DET_PATH = "./resource/model_zoo/box_160x120.tflite"


    FONT_PATH = "./resource/font/simsun.ttc"
    FONT_SIZE = 30

ai_cfg = AI_Config()
