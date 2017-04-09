import numpy as np
import cv2
import setLines
import time
import timer
import os

icp = 1000
icf = 1000


def cropAndSavePositive(img, x, y):
    global icp
    # crop_img = img[y - 64:y + 128, x - 64:x + 128].copy()

    path_output_dir = 'images/positive'
    img_name = os.path.join(path_output_dir, '%d.png') % icp
    icp += 1
    print img_name
    cv2.imwrite(os.path.join(path_output_dir, '%d.png') % icp, img)


def cropAndSaveFalse(img, x, y):
    global icf

    # crop_img = img[y - 64:y + 128, x - 64:x + 128].copy()
    path_output_dir = 'images/false'
    img_name = os.path.join(path_output_dir, '%d.png') % icf
    icf += 1
    print img_name
    cv2.imwrite(os.path.join(path_output_dir, '%d.png') % icf, img)
    # cv2.imwrite(img_name, img)


def chooseImages(img, x, y):
    # cv2.rectangle(img, (x - 64, y - 64), (x + 64, y + 64), (255, 0, 0), 2)
    # crop_img = img[y - 64:y + 128, x - 64:x + 128].copy()

    # roi = fgmask[y - deltaY:y - deltaY + 80, x - deltaX:x - deltaX + 80]
    while True:
        cv2.imshow("Choose false or positive", img)
        k = cv2.waitKey(0)

        if k == 102:
            cropAndSaveFalse(img, x, y)
            break
        elif k == 112:
            cropAndSavePositive(img, x, y)
            break
        elif k == 113:
            print 'Exit...'
            os._exit(1)
        elif k == 32:
            print 'Skipping image'
            break


def drawStartAndFinishLines(points, frame):
    frame = cv2.line(frame, (points[0][0], points[0][1]),
                     (points[0][2], points[0][1]), (0, 255, 0), 3)
    frame = cv2.line(frame, (points[0][0], points[0][3]),
                     (points[0][2], points[0][3]), (255, 255, 255), 5)
    return frame


def run():
    prevCnts = []
    cap = cv2.VideoCapture('../videos/3.mp4')

    font = cv2.FONT_HERSHEY_SIMPLEX
    # MOG 2 background substraction
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    if not cap.isOpened():
        print "Error: Video device or file couldn't be opened"
        exit()

    print "Press space to choose start/finish line"

    # Retrieve an image and Display it.
    retval, img = cap.read()
    if not retval:
        print "Error:Cannot capture frame device"
        exit()

    # Start time
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(
            fps)
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(
            fps)

    print fps
    isTimerStarted = False
    isTimerFinished = False
    timePassed = 0
    frameCounter = 0
    isRaceFinished = False
    while True:
        if 'cntsNew' in locals():
            prevCnts = cntsNew
        # read frame
        ret, frame = cap.read()

        if not ret:
            print "Error: Cannot capture frame device"
            os._exit(1)
        # frame = cv2.resize(frame, (640, 480))
        # BGR to gray

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #denoised = cv2.fastNlMeansDenoising(gray, 10, 21, 7)
        blur = cv2.GaussianBlur(gray, (5, 5), 2)
        # MOG mask
        fgmask = fgbg.apply(blur)

        im2, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        cntsNew = []
        for key in contours:
            #epsilon = 0.05 * cv2.arcLength(key, True)
            approx = cv2.approxPolyDP(key, 1, True)
            # print approx
            # print "_______________"
            if cv2.contourArea(approx) > 20 and cv2.arcLength(key, True) > 30:
                cntsNew.append(approx)
        for j in prevCnts:
            for i in cntsNew:
                if (cv2.arcLength(i, True) - cv2.arcLength(j, True)) < 50:
                    if (cv2.contourArea(i) - cv2.contourArea(j)) < 50:
                        # compute the center of the contour
                        iM = cv2.moments(i)
                        cXiM = int(iM["m10"] / iM["m00"])
                        cYiM = int(iM["m01"] / iM["m00"])

                        jM = cv2.moments(j)
                        cXjM = int(jM["m10"] / jM["m00"])
                        cYjM = int(jM["m01"] / jM["m00"])

                        if (cXiM - cXjM) < 20 and (cYiM - cYjM) < 20:
                            # cv2.circle(frame, (cXjM, cYjM), 50, (0, 0, 255), 2)

                            x, y, w, h = cv2.boundingRect(i)

                            deltaX = int((80 - w) / 2)
                            deltaY = int((80 - h) / 2)

                            if (y - deltaY < 0 or x - deltaX < 0 or
                                    x - deltaX + 80 > len(frame[0]) or
                                    y - deltaY + 80 > len(frame)):
                                continue
                            roi = frame[y - deltaY:y - deltaY + 80, x - deltaX:
                                        x - deltaX + 80]

                            chooseImages(roi, cXjM, cYjM)

        # cv2.drawContours(frame, cntsNew, 0, (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
            os._exit(1)
    os._exit(1)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    run()
