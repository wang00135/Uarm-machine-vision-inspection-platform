#读取、显示、保存图片
import cv2 as cv
#读取名为test的png图片并转化为灰度图
path = "./test.png"
gray_img = cv.imread(path,cv.IMREAD_GRAYSCALE)

#新建一个名为Winname的窗口，属性设置为可手动调整大小
cv.namedWindow('Winname',cv.WINDOW_NORMAL)

#在Winname窗口上显示读取到的灰度图
cv.imshow('Winname',gray_img)

#保存灰度图为jpg类型,并设置其图像质量为100
cv.imwrite("./test_gray.jpg",gray_img,(cv.IMWRITE_JPEG_QUALITY,100))

#程序停止，一直等待按键
cv.waitKey(0)

