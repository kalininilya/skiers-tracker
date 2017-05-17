import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('gftt.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

surf = cv2.SURF(400)
kp, des = surf.detectAndCompute(img, None)
img = cv2.drawKeypoints(gray, kp)
plt.imshow(img), plt.show()
