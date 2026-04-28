#/usr/bin/env python3
#coding=utf8

'''
交互式GrabCut算法，
首先按住右键选取矩形框；
‘N’键产生分割图；
按下‘0’键之后，鼠标左键选择背景区域
按下‘1’键之后，鼠标左键选择前景区域
'''
import cv2 as cv
import numpy as np

class App(object):
    """docstring for App"""
    BLUE = [255,0,0]        # rectangle color
    RED = [0,0,255]         # PR BG
    GREEN = [0,255,0]       # PR FG
    BLACK = [0,0,0]         # sure BG
    WHITE = [255,255,255]   # sure FG

    DRAW_BG = {'color' : BLACK, 'val' : 0}
    DRAW_FG = {'color' : WHITE, 'val' : 1}
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
    DRAW_PR_BG = {'color' : RED, 'val' : 2}

    rect = (0,0,1,1)
    drawing = False         # flag for drawing curves
    rectangle = False       # flag for drawing rect
    rect_over = False       # flag to check if rect drawn
    rect_or_mask = 100      # flag for selecting rect or mask mode
    value = DRAW_FG         # drawing initialized to FG
    thickness = 2           # brush thickness

    def __init__(self, filename):
        self.filename = filename
        self.mask = None
        self.user_mask = False

    def onmouse(self, event, x, y, flags, param):
        # 绘制矩形
        if event == cv.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x,y
            self.ox, self.oy = x,y
        elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
            cv.line(self.img_copy, (self.ox, self.oy), (x, y), (127, 127, 127), 3, 2)
            self.ox, self.oy = x, y     
        elif event == cv.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            self.img_copy = self.img.copy()
            cv.rectangle(self.img_copy, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))

        if event == cv.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print('需要先绘制一个矩形')
            else:
                self.drawing = True
                self.ox, self.oy = x, y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.line(self.img_copy, (self.ox, self.oy), (x, y), self.value['color'], 
                    self.thickness, 2)
                cv.line(self.mask, (self.ox, self.oy), (x, y), self.value['val'], 
                    self.thickness, 2)
                self.ox, self.oy = x, y

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                self.user_mask = True

    def run(self):
        self.img = cv.imread(self.filename)
        self.img_copy = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8)  # 初始化掩模
        self.output = np.zeros(self.img.shape, np.uint8)  # 前景分割输出图像
        cv.namedWindow('output')
        cv.namedWindow('input')
        cv.setMouseCallback('input', self.onmouse)
        cv.moveWindow('input', self.img.shape[1]+10,90)

        while True:
            k = cv.waitKey(1) & 0XFF
            if chr(k) == 'q' or k == 27:
                break
            elif chr(k) == '0':
                self.value = self.DRAW_BG
            elif chr(k) == '1':
                self.value = self.DRAW_FG
            elif chr(k) == 'n':
                print(self.rect)
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                if self.user_mask: 
                    # 使用掩模 
                    cv.grabCut(self.img, 
                                self.mask, 
                                self.rect, 
                                bgdmodel, 
                                fgdmodel, 
                                1, 
                                cv.GC_INIT_WITH_MASK)
                else:
                    # 使用矩形框
                    cv.grabCut(self.img, 
                                self.mask, 
                                self.rect, 
                                bgdmodel, 
                                fgdmodel, 
                                1, 
                                cv.GC_INIT_WITH_RECT)

                mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype(np.uint8)
                self.output = cv.bitwise_and(self.img, self.img, mask=mask2)
            elif chr(k) == 'r':
                self.img_copy = self.img.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8)
                self.user_mask = False
            elif chr(k) == 's':
                cv.imwrite('./outputs/input.jpg', self.img)
                cv.imwrite('./outputs/output.jpg', self.output)    

            cv.imshow('input', self.img_copy)
            cv.imshow('output', self.output)

if __name__ == '__main__':
    filename = 'test.png'
    App(filename).run()
    cv.destroyAllWindows()
