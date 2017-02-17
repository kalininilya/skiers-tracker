import cv2
from sympy import Line,Point


def isStarted(points, cnts):
    p1 = (points[0][0], points[0][1])
    p2 = (points[0][2], points[0][1])
    s = Line(p1, p2)
    for cnt in cnts:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        p3 = (cX, cY)
        distance = s.distance(p3)
        if (distance < 3):
            return True
        else:
            return False

def isFinished(points, cnts):
    p1 = (points[0][0], points[0][3])
    p2 = (points[0][2], points[0][3])
    s = Line(p1, p2)
    for cnt in cnts:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        p3 = (cX, cY)
        distance = s.distance(p3)
        if (distance < 5):
            return True
        else:
            return False