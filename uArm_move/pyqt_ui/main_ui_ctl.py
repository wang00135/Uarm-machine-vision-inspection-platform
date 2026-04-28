import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from pyqt_ui.bkrc_ui_lib.ui_bkrc import Ui_MainWindow
from pyqt_ui.bkrc_ui_lib.ai_table_ui import AiTableUi
from pyqt_ui.bkrc_ui_lib.arm_move_ctr_ui import ArmMoveTableUi
from pyqt_ui.bkrc_ui_lib.color_threshold_ui import ColorThresholdUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time

ui_window = Ui_MainWindow()   # 创建UI对象

# 静态载入
class MainWindow(QMainWindow):
    def __init__(self, full_dict=None):
        super(MainWindow, self).__init__()
        ui_window.setupUi(self)

        self.setWindowIcon(QIcon(':/images/images/bkrc.png'))
        self.setStyleSheet("QMainWindow{border-image: url(:/images/images/bj_1.jpg);}")

        ui_window.tabWidget.setCurrentIndex(0)  # 设置默认标签为第一个标签

        # 机械臂控制功能模块
        ArmMoveTableUi(ui_window, self.messageFrom, full_dict)

        # 图像识别分拣交互模块
        AiTableUi(ui_window, self.messageFrom, full_dict)

        # 颜色阈值调整模块
        ColorThresholdUi(ui_window, self.messageFrom, full_dict)

    def messageFrom(self, string):
        # 弹窗提示函数
        try:
            QMessageBox.about(self, "", string)
            time.sleep(0.01)
        except:
            pass

    # 键盘监听事件，当按下ctrl+Z的组合是，关闭窗口
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.close()


if __name__ == "__main__":
    import multiprocessing as mp
    from tools.config import config as cfg

    app = QtWidgets.QApplication(sys.argv)
    q_send = mp.Manager().Queue(maxsize=8)
    q_image = mp.Manager().Queue(maxsize=3)
    full_dict = mp.Manager().dict()       # 全局数据共享

    # full_dict[cfg.VOICE_INDEX] = 0

    # 图像识别模式  货物位置  仓库位置   搬运位置（模式 货物搬仓库，仓库搬货物，起始， 终止）
    full_dict[cfg.SORTING_VAL] = [0, [1, 2, 3], [1, 2, 3], [1, 1, 1]]

    # full_dict[cfg.NODE_STD] = [[1, 2, 0x1b], [1, 23]]


    myshow = MainWindow(q_image, q_send, full_dict)
    myshow.show()
    # window.ui.showFullScreen()  # 动态载入
    sys.exit(app.exec_())
