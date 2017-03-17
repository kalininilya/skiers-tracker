import numpy as np
import cv2
import setLines
import time
import timer
import os


def drawStartAndFinishLines(points, frame):
    frame = cv2.line(frame,(points[0][0],points[0][1]),(points[0][2],points[0][1]),(0,255,0),3)
    frame = cv2.line(frame,(points[0][0],points[0][3]),(points[0][2],points[0][3]),(255,255,255),5)
    return frame

def run():
    prevCnts = []
    cap = cv2.VideoCapture('../videos/3.mp4')

    font = cv2.FONT_HERSHEY_SIMPLEX
    #MOG 2 background substraction
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    
    if not cap.isOpened():
        print "Error: Video device or file couldn't be opened"
        exit()

    print "Press space to choose start/finish line"

    # Retrieve an image and Display it.
    retval, img = cap.read()
    if not retval:
        print "Error: Cannot capture frame device"
        exit()
    
    points = setLines.run(img)
    cv2.destroyWindow("Image")
    if not points:
        print "ERROR: No start and finish lines had been set."
        exit()

    # Start time
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)
     
    print fps
    isTimerStarted = False
    isTimerFinished = False
    timePassed = 0
    frameCounter = 0
    isRaceFinished = False
    while True:
        
        if 'cntsNew' in locals():
            prevCnts = cntsNew
            
        #read frame
        ret, frame = cap.read()

        if not ret:
            print "Error: Cannot capture frame device"
            os._exit(1)
        # frame = cv2.resize(frame, (640, 480))  
        #BGR to gray
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #denoised = cv2.fastNlMeansDenoising(gray, 10, 21, 7)
        blur = cv2.GaussianBlur(gray,(5,5),2)
        #MOG mask
        fgmask = fgbg.apply(blur)

        # __________________________
        #Canny filter
        # cannyMin = cv2.getTrackbarPos('CannyMin','edges')
        # cannyMax = cv2.getTrackbarPos('CannyMax','edges')
        # edges = cv2.Canny(fgmask,cannyMin,cannyMax)
        # __________________________

        im2, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        cntsNew = []
        for key in contours:
            epsilon = 0.05*cv2.arcLength(key,True)
            approx = cv2.approxPolyDP(key,1,True)
            #print approx
            #print "_______________"
            if (cv2.contourArea(approx) > 50 and cv2.arcLength(key,True) > 70):
                cntsNew.append(approx)
        for j in prevCnts:
            for i in cntsNew:
                if ((cv2.arcLength(i,True) - cv2.arcLength(j,True)) < 50):
                    if ((cv2.contourArea(i) - cv2.contourArea(j)) < 50):
                        # compute the center of the contour
                        iM = cv2.moments(i)
                        cXiM = int(iM["m10"] / iM["m00"])
                        cYiM = int(iM["m01"] / iM["m00"])

                        jM = cv2.moments(j)
                        cXjM = int(jM["m10"] / jM["m00"])
                        cYjM = int(jM["m01"] / jM["m00"])

                        if (((cXiM-cXjM) < 20) and ((cYiM-cYjM) < 20)):
                            cv2.circle(frame,(cXjM,cYjM), 50, (0,0,255), 2)
                        
        cv2.drawContours(frame, cntsNew, 0, (255,0,0), 2)
        if (timer.isStarted(points, cntsNew) and isTimerStarted==False):
            print "Started"
            isTimerStarted = True
        if (timer.isFinished(points, cntsNew) and isTimerFinished==False):
            print "Finished"
            isTimerFinished = True
        
        frame = drawStartAndFinishLines(points, frame)
        #timer
        if (isTimerStarted):
            frameCounter += 1
            timePassed = (frameCounter/fps)
            if (not(isRaceFinished)):
                print timePassed
                text = "Time: " + str(round(timePassed,3))
                cv2.putText(frame, text,(50,50), font, 1,(255,255,255),2)


        if (isTimerFinished and not(isRaceFinished)):
            print "Race time: {}", timePassed
            text = "Race finished with a race time: " + str(round(timePassed,3))
            cv2.putText(frame, text,(50,150), font, 1,(255,255,255),2)
            isRaceFinished = True
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 640,480)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
            os._exit(1)
    os._exit(1)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
