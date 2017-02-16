import numpy as np
import cv2
import setLines

# cv2.namedWindow('edges')

#Creating Trackbars for Canny
# cv2.createTrackbar('CannyMin','edges',0,1000,nothing)
# cv2.createTrackbar('CannyMax','edges',0,1000,nothing)


boxes = []

def drawStartAndFinishLines(points, frame):
    print "points[0]", points[0]
    print "points[0][1]", points[0][1]
    frame = cv2.line(frame,(0,0),(511,511),(255,0,0),5)
    return frame


def run():
    prevCnts = []
    cap = cv2.VideoCapture('./videos/3.mp4')
    #MOG 2 background substraction
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    

    if not cap.isOpened():
        print "Error: Video device or file couldn't be opened"
        exit()

    print "Press space to choose start/finish line"

    while True:
        # Retrieve an image and Display it.
        retval, img = cap.read()
        if not retval:
            print "Error: Cannot capture frame device"
            exit()
        if(cv2.waitKey(10)==ord(' ')):
            break
        cv2.namedWindow("Image")
        cv2.imshow("Image", img)
    cv2.destroyWindow("Image")
    
    points = setLines.run(img)

    if not points:
        print "ERROR: No start and finish lines had been set."
        exit()
    print points
    while True:
        
        if 'cntsNew' in locals():
            prevCnts = cntsNew
            
        #read frame
        ret, frame = cap.read()
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
                        
        cv2.drawContours(frame, cntsNew, -1, (255,0,0), -1)

        frame = drawStartAndFinishLines(points, frame)

        cv2.imshow('frame',frame)
        # cv2.imshow('edges',edges)
        # cv2.imshow('fgbg',fgmask)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
