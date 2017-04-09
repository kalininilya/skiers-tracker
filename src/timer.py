import cv2
from sympy import Line, Point


def distance(p0, p1, p2):  # p3 is the point
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    nom = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denom = ((y2 - y1)**2 + (x2 - x1)**2)**0.5
    result = nom / denom
    return result


def isStarted(points, cX, cY):

    p1 = (points[0][0], points[0][1])
    p2 = (points[0][2], points[0][1])

    p3 = (cX, cY)
    dis = distance(p1, p2, p3)
    if (dis < 10):
        return True
    else:
        return False


def isFinished(points, cX, cY):
    p1 = (points[0][0], points[0][3])
    p2 = (points[0][2], points[0][3])
    p3 = (cX, cY)
    dis = distance(p1, p2, p3)
    if (dis < 10):
        return True
    else:
        return False