from base.components.config import ai_cfg
from tools.log import log
import cv2
from base.components.utlis import DetRecFunctions, draw_ocr
from tools.config import config


DET_PATH = '../resource/model_zoo/det_model.onnx'
SMALL_REC_PATH = '../resource/model_zoo/rec_model.onnx'
LARGE_REC_PATH = '../resource/model_zoo/rec_model.onnx'
PPOCR_KEYS_PATH = '../resource/model_zoo/ppocr_keys_v1.txt'

class OcrRec(object):
    def __init__(self, det_file=DET_PATH, small_rec_file=SMALL_REC_PATH,
                 large_rec_file=LARGE_REC_PATH, ppocr_keys=PPOCR_KEYS_PATH):
        # OCR-检测-识别
        self.ocr_sys = DetRecFunctions(det_file=det_file, small_rec_file=small_rec_file,
                                  large_rec_file=large_rec_file, ppocr_keys=ppocr_keys)

        self.predictions = []


    def inference(self, img):
        txts = scores = []
        filter_boxes, filter_rec_res = [], []
        # 得到检测框
        dt_boxes = self.ocr_sys.get_boxes(img)

        if config.OCR_REC:
            # 识别 results: 单纯的识别结果，results_info: 识别结果+置信度
            results, results_info = self.ocr_sys.recognition_img(img, dt_boxes)

            for box, rec_reuslt in zip(dt_boxes, results):
                text, score = rec_reuslt
                if score >= 0.5:
                    filter_boxes.append(box)
                    filter_rec_res.append(rec_reuslt)

            txts = [filter_rec_res[i][0] for i in range(len(filter_rec_res))]
            scores = [filter_rec_res[i][1] for i in range(len(filter_rec_res))]
        self.predictions = [filter_boxes, txts, scores]
        return self.predictions

def recImgDis(img, predictions):
    results = []
    if predictions:
        dt_boxes, txts, scores = predictions

        img = draw_ocr(img, dt_boxes, txts, scores, font_path="../resource/font/simfang.ttf")
    return img, results

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    ocr_rec = OcrRec()

    while True:
        ret, frame = cap.read()
        img = cv2.resize(frame, (640, 480))
        ocr_pricet = ocr_rec.inference(img)
        img, ocr_str = recImgDis(img, ocr_pricet)
        cv2.imshow("landmark_rec", img)
        cv2.waitKey(10)
