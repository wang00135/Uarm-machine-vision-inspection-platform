
class AI_Config:
    # 基本设置
    window_name = "AI_RUN"

    CAM_HEIGHT = 480
    CAM_WIDTH = 640
    BOX_INPUT_SIZE = (120, 160)  # (h, w)

    BOX_CLASSES = ['background', 'box']


    # SLIM-SSD目标检测模型配置
    # anchor配置
    # MIN_SIZES = [[(9, 7), (24, 20), (39, 35)], [(54, 41), (65, 61), (81, 66)],
    #               [(94, 86), (113, 95), (131, 122)], [(137, 128), (172, 162), (176, 210)]]
    MIN_SIZES = [[10, 16, 24], [32, 48], [64, 96], [128, 192, 256]]

    STEPS = [8, 16, 32, 64]
    MATCH_THRESH = 0.45
    VARIANCES = [0.1, 0.2]
    CLIP = False

    # 推理
    SCORE_THRESHOLD = 0.86  # 得分阈值
    NMS_THRESHOLD = 0.6     # nms阈值

    # 模型路径
    BOX_DET_PATH = "./resource/model_zoo/box_160x120.tflite"

    FONT_PATH = "./resource/font/simsun.ttc"
    FONT_SIZE = 20

ai_cfg = AI_Config()
