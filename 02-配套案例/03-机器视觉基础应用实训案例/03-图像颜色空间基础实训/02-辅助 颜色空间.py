import glob

import cv2 as cv
import numpy as np

# global variable to keep track of
show = False


def onTrackbarActivity(x):
    global show
    show = True
    pass


if __name__ == '__main__':

    # Get the filename from the command line 
    files = glob.glob('images/rub*.jpg')
    files.sort()
    # load the image 
    original = cv.imread(files[0])
    # Resize the image
    rsize = 250
    original = cv.resize(original, (rsize, rsize))

    # position on the screen where the windows start
    initialX = 50
    initialY = 50

    # creating windows to display images
    cv.namedWindow('P-> Previous, N-> Next', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('SelectBGR', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('SelectHSV', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('SelectYCB', cv.WINDOW_AUTOSIZE)
    cv.namedWindow('SelectLAB', cv.WINDOW_AUTOSIZE)

    # moving the windows to stack them horizontally
    cv.moveWindow('P-> Previous, N-> Next', initialX, initialY)
    cv.moveWindow('SelectBGR', initialX + (rsize + 5), initialY)
    cv.moveWindow('SelectHSV', initialX + 2 * (rsize + 5), initialY)
    cv.moveWindow('SelectYCB', initialX + 3 * (rsize + 5), initialY)
    cv.moveWindow('SelectLAB', initialX + 4 * (rsize + 5), initialY)

    # creating trackbars to get values for YCrCb
    cv.createTrackbar('CrMin', 'SelectYCB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('CrMax', 'SelectYCB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('CbMin', 'SelectYCB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('CbMax', 'SelectYCB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('YMin', 'SelectYCB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('YMax', 'SelectYCB', 0, 255, onTrackbarActivity)

    # creating trackbars to get values for HSV
    cv.createTrackbar('HMin', 'SelectHSV', 0, 180, onTrackbarActivity)
    cv.createTrackbar('HMax', 'SelectHSV', 0, 180, onTrackbarActivity)
    cv.createTrackbar('SMin', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv.createTrackbar('SMax', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv.createTrackbar('VMin', 'SelectHSV', 0, 255, onTrackbarActivity)
    cv.createTrackbar('VMax', 'SelectHSV', 0, 255, onTrackbarActivity)

    # creating trackbars to get values for BGR
    cv.createTrackbar('BGRBMin', 'SelectBGR', 0, 255, onTrackbarActivity)
    cv.createTrackbar('BGRBMax', 'SelectBGR', 0, 255, onTrackbarActivity)
    cv.createTrackbar('BGRGMin', 'SelectBGR', 0, 255, onTrackbarActivity)
    cv.createTrackbar('BGRGMax', 'SelectBGR', 0, 255, onTrackbarActivity)
    cv.createTrackbar('BGRRMin', 'SelectBGR', 0, 255, onTrackbarActivity)
    cv.createTrackbar('BGRRMax', 'SelectBGR', 0, 255, onTrackbarActivity)

    # creating trackbars to get values for LAB
    cv.createTrackbar('LABLMin', 'SelectLAB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('LABLMax', 'SelectLAB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('LABAMin', 'SelectLAB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('LABAMax', 'SelectLAB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('LABBMin', 'SelectLAB', 0, 255, onTrackbarActivity)
    cv.createTrackbar('LABBMax', 'SelectLAB', 0, 255, onTrackbarActivity)

    # show all images initially
    cv.imshow('SelectHSV', original)
    cv.imshow('SelectYCB', original)
    cv.imshow('SelectLAB', original)
    cv.imshow('SelectBGR', original)
    i = 0
    while (1):

        cv.imshow('P-> Previous, N-> Next', original)
        k = cv.waitKey(1) & 0xFF

        # check next image in folder    
        if k == ord('n'):
            i += 1
            original = cv.imread(files[i % len(files)])
            original = cv.resize(original, (rsize, rsize))
            show = True

        # check previous image in folder    
        elif k == ord('p'):
            i -= 1
            original = cv.imread(files[i % len(files)])
            original = cv.resize(original, (rsize, rsize))
            show = True
        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

        if show:  # If there is any event on the trackbar
            show = False

            # Get values from the BGR trackbar
            BMin = cv.getTrackbarPos('BGRBMin', 'SelectBGR')
            GMin = cv.getTrackbarPos('BGRGMin', 'SelectBGR')
            RMin = cv.getTrackbarPos('BGRRMin', 'SelectBGR')
            BMax = cv.getTrackbarPos('BGRBMax', 'SelectBGR')
            GMax = cv.getTrackbarPos('BGRGMax', 'SelectBGR')
            RMax = cv.getTrackbarPos('BGRRMax', 'SelectBGR')
            minBGR = np.array([BMin, GMin, RMin])
            maxBGR = np.array([BMax, GMax, RMax])

            # Get values from the HSV trackbar
            HMin = cv.getTrackbarPos('HMin', 'SelectHSV')
            SMin = cv.getTrackbarPos('SMin', 'SelectHSV')
            VMin = cv.getTrackbarPos('VMin', 'SelectHSV')
            HMax = cv.getTrackbarPos('HMax', 'SelectHSV')
            SMax = cv.getTrackbarPos('SMax', 'SelectHSV')
            VMax = cv.getTrackbarPos('VMax', 'SelectHSV')
            minHSV = np.array([HMin, SMin, VMin])
            maxHSV = np.array([HMax, SMax, VMax])

            # Get values from the LAB trackbar
            LMin = cv.getTrackbarPos('LABLMin', 'SelectLAB')
            AMin = cv.getTrackbarPos('LABAMin', 'SelectLAB')
            BMin = cv.getTrackbarPos('LABBMin', 'SelectLAB')
            LMax = cv.getTrackbarPos('LABLMax', 'SelectLAB')
            AMax = cv.getTrackbarPos('LABAMax', 'SelectLAB')
            BMax = cv.getTrackbarPos('LABBMax', 'SelectLAB')
            minLAB = np.array([LMin, AMin, BMin])
            maxLAB = np.array([LMax, AMax, BMax])

            # Get values from the YCrCb trackbar
            YMin = cv.getTrackbarPos('YMin', 'SelectYCB')
            CrMin = cv.getTrackbarPos('CrMin', 'SelectYCB')
            CbMin = cv.getTrackbarPos('CbMin', 'SelectYCB')
            YMax = cv.getTrackbarPos('YMax', 'SelectYCB')
            CrMax = cv.getTrackbarPos('CrMax', 'SelectYCB')
            CbMax = cv.getTrackbarPos('CbMax', 'SelectYCB')
            minYCB = np.array([YMin, CrMin, CbMin])
            maxYCB = np.array([YMax, CrMax, CbMax])

            # Convert the BGR image to other color spaces
            imageBGR = np.copy(original)
            imageHSV = cv.cvtColor(original, cv.COLOR_BGR2HSV)
            imageYCB = cv.cvtColor(original, cv.COLOR_BGR2YCrCb)
            imageLAB = cv.cvtColor(original, cv.COLOR_BGR2LAB)

            # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results         
            maskBGR = cv.inRange(imageBGR, minBGR, maxBGR)
            resultBGR = cv.bitwise_and(original, original, mask=maskBGR)

            maskHSV = cv.inRange(imageHSV, minHSV, maxHSV)
            resultHSV = cv.bitwise_and(original, original, mask=maskHSV)

            maskYCB = cv.inRange(imageYCB, minYCB, maxYCB)
            resultYCB = cv.bitwise_and(original, original, mask=maskYCB)

            maskLAB = cv.inRange(imageLAB, minLAB, maxLAB)
            resultLAB = cv.bitwise_and(original, original, mask=maskLAB)

            # Show the results
            cv.imshow('SelectBGR', resultBGR)
            cv.imshow('SelectYCB', resultYCB)
            cv.imshow('SelectLAB', resultLAB)
            cv.imshow('SelectHSV', resultHSV)

    cv.destroyAllWindows()
