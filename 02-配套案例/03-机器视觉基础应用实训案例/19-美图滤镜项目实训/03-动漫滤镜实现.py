# 动漫滤镜实现
import cv2
import matplotlib.pyplot as plt
import numpy as np

# '1. 初始操作'，读取图像并显示
src = cv2.imread('Resources/src.jpg')
cloud = cv2.imread('Resources/cloud.jpg')
b, g, r = cv2.split(src)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()
b, g, r = cv2.split(cloud)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()

# '2. 转化为灰度图'
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

# '3. 增强HSV每个通道中的灰度值      分离->完成增强->合并'
h, s, v = cv2.split(hsv)
v = cv2.equalizeHist(v)
mergeimg = cv2.merge([h, s, v])

# '4. 颜色分割（分割出图像里的天空）'
# 通过查表法确定蓝色的阀值
minVal = np.array([100, 43, 46])
maxVal = np.array([124, 255, 255])
inRangimg = cv2.inRange(mergeimg, minVal, maxVal)
# 显示
plt.imshow(inRangimg,cmap='Greys')
plt.show()

def FindBigestContour(src):
    '''
    寻找最大轮廓
    :param src:传入二值化后图像
    :return: 输出图像
    '''
    imax = 0
    imaxcontours = -1
    # 查找最大轮廓，返回的是原图片，边界集合，轮廓的属性
    contours, hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        itemp = cv2.contourArea(contours[i])
        if (imaxcontours < itemp):
            imaxcontours = itemp
            imax = i

    return contours[imax]

# '5. 开操作（消除噪声）'
kernel = np.ones([5, 5], np.uint8)
imgdeal = cv2.dilate(cv2.erode(inRangimg, kernel), kernel, iterations=2)

# '6. 获得掩模图像的位置'
mask = imgdeal.copy()
maxCountour = FindBigestContour(mask)  # 查找最大轮廓

# '7. 获取原图像中心位置'
# 返回的是（x,y,w,h）四个参数
maxRect = cv2.boundingRect(maxCountour)
cloud = cv2.resize(cloud, (maxRect[2], maxRect[3]))
# 获得中心点坐标
center = (maxRect[2] // 2, maxRect[3] // 2)

# '8. 将天空融合到原图中——seamlessClone()函数
# 参数说明：1）天空图片   2）原图    3）粗糙掩模（可以为全白图像）  
# 4）源图像中心在目标图像中的位置  
# 5）克隆模式“NORMAL_CLONE”表示不保留原图像的texture细节，目标区域的梯度只由原图像决定。
out_put = cv2.seamlessClone(cloud, src, mask, center, cv2.NORMAL_CLONE)  # 图像叠加
b, g, r = cv2.split(out_put)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()

def EnhanceSatutrtion(src, alpha, bright):
    '''
    增强图像的对比度
    :param src: 输入图像
    :param alpha: 图像对比度
    :param bright: 亮度
    :return: 输出图像
    '''
    blank = np.zeros_like(src, src.dtype)
    dst = cv2.addWeighted(src, alpha, blank, 1 - alpha, bright)  # 增加对比度
    return dst

# '9. 双边滤波——消除图像噪声'
temp = cv2.bilateralFilter(out_put.copy(), 5, 10.0, 2.0)

# '10. 增强图像整体对比度'
matDst = EnhanceSatutrtion(temp, 1.5, 1.5)

# '12. 完成显示'
b, g, r = cv2.split(matDst)
img = cv2.merge([r, g, b])
plt.imshow(img)
plt.show()