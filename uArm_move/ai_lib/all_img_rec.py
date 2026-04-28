from ai_lib.fruits_detecte_rec import FruitDetect
from ai_lib.electron_rec import ElectronRec
from ai_lib.garbage_rec import GarbageRec
from ai_lib.components.config import ai_cfg

class AllImgRec():
    def __init__(self):
        self.fruit_rec = FruitDetect(model_path=ai_cfg.FRUIT_REC_PATH)
        self.electron_rec = ElectronRec(model_path=ai_cfg.ELECTRON_REC_PATH)
        self.garbage_rec = GarbageRec(model_path=ai_cfg.GARBAGE_REC_PATH)

        self.allrec = [[], self.electron_rec, self.fruit_rec, self.garbage_rec]

    def run(self, index, img, auto=True):
        return self.allrec[index].inference(img, auto=auto)