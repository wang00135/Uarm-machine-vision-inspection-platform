import numpy as np
from PIL import ImageFont, ImageDraw, Image
from base.components.config import ai_cfg

def putText(img, text, org=(0, 0), font_path=ai_cfg.FONT_PATH,
            color=(0, 0, 255), font_size=ai_cfg.FONT_SIZE):
    """
    在图片上显示文字
    :param img: 输入的img, 通过cv2读取
    :param text: 要显示的文字
    :param org: 文字左上角坐标
    :param font_path: 字体路径
    :param color: 字体颜色, (B,G,R)
    :return:
    """
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    b, g, r = color
    a = 0
    draw.text(org, text, font=ImageFont.truetype(font_path, font_size), fill=(b, g, r, a))
    img = np.array(img_pil)
    return img

def controlEmbedded(rec_data=None):
    """
    根据模型识别结果控制嵌入式设备
    :param rec_data: AI模型识别结果
    :return: 所执行的控制指令
    """
    pass


def getEmbeddedData(data_msg=None):
    """
    获取嵌入式设备的数据（根据功能提取数据）
    :return: 解析的数据
    """
    data = (data_msg[3] << 8) + data_msg[4]   # 解析压力传感器数据
    print("data", data)
    return data