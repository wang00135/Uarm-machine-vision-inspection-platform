import numpy as np

sampleNo = 1000
# 一维正态分布
# 下面三种方式是等效的
mu = 3
sigma = 0.1
np.random.seed(0)
s = np.random.normal(.5, .1, size = 9)
dst = s / sum(s)
dst_3x3 = dst.reshape(3, 3)

img = np.array([80, 73, 69, 77, 83, 74, 74, 79, 74], np.uint8).reshape(3, 3)
img_1 = np.array([80, 80, 73, 80, 80, 73, 77, 77, 76], np.uint8).reshape(3, 3)
resize = img * dst_3x3
resize_1 = img_1 * dst_3x3
print(img)
print('*' * 60)
print(dst_3x3)
print('*' * 60)
print(resize)
print(int(sum(resize.reshape(-1, ))))
print(int(sum(resize_1.reshape(-1, ))))
print(sum(dst))
