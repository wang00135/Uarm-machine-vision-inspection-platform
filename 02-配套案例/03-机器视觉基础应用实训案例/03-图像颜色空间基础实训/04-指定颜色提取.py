#ex13 提取指定颜色

import cv2 as cv
# 1、载入图像
img_src = cv.imread('color.jpg')
# 2、转换空间转换
hsv_src = cv.cvtColor(img_src, cv.COLOR_BGR2HSV)

# 3、设置红色在HSV当中高低阈值
red_low_hsv1 = (156, 43, 46)
red_high_hsv1 = (180, 255, 255)
red_low_hsv2 = (0, 43, 46)
red_high_hsv2 = (10, 255, 255)

# 4、分割颜色获得掩模
mask_red1 = cv.inRange(hsv_src, red_low_hsv1, red_high_hsv1)
mask_red2 = cv.inRange(hsv_src, red_low_hsv2, red_high_hsv2)

# 5、掩模和原图进行位与
mask_red = cv.add(mask_red1,mask_red2)
red = cv.bitwise_and(hsv_src,hsv_src,mask = mask_red)
red = cv.cvtColor(red,cv.COLOR_HSV2BGR)

# 6、显示图像
cv.imshow('src', img_src)
cv.imshow('red', red)
cv.imshow('mask_red1', mask_red1)
cv.imshow('mask_red2', mask_red2)
cv.imwrite('mask_red1.jpg',mask_red1)
cv.imwrite('mask_red2.jpg',mask_red2)
cv.imwrite('mask_red.jpg',mask_red)
cv.imwrite('red.jpg', red)
cv.waitKey(0)
cv.destroyAllWindows()
