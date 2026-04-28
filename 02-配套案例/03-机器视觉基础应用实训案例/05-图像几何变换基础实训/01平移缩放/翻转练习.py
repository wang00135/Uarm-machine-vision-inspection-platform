#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

img = cv.imread('./test.png')
rows, cols = img.shape[:2]

M = np.float32([[1, 0, cols], [0, 1, 0]])
dst4 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4, borderMode = cv.BORDER_DEFAULT)
M = np.float32([[1, 0, 0], [0, 1, rows]])
dst5 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4, borderMode = cv.BORDER_DEFAULT)
M = np.float32([[1, 0, cols], [0, 1, rows]])
dst6 = cv.warpAffine(img, M, (cols, rows), flags = cv.INTER_LANCZOS4, borderMode = cv.BORDER_DEFAULT)

cv.imwrite('./outputs/fig.jpg', dst4)
cv.imwrite('./outputs/fig_1.jpg', dst5)
cv.imwrite('./outputs/fig_2.jpg', dst6)
