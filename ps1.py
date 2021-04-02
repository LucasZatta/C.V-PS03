import numpy as np
import argparse
from matplotlib import pyplot as plt
import math
import cv2

img_name="gummy.jpg"

archive_name ="Input\{imgName}".format(imgName = img_name)

image = cv2.imread(archive_name)
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#threshold the grey level image to make it binary
tret,thresh = cv2.threshold(grey,127,255,cv2.THRESH_BINARY)
cv2.imwrite("Output\gray"+img_name,thresh)

#Count blackpixels
black_pixels = (thresh == 0).sum();

#The number of white pixels is the diference between total and blackpixels
print("Black Pixels Count: " + str(black_pixels))
print("White Pixels Count: " + str(thresh.size - black_pixels))

#edge detection on thresholded image
edged = cv2.Canny(thresh, 75, 200)

#find the countours
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#sort countours by size
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
print(len(cnts))

for c in cnts:
	#aux copy of image
	imgCopy = image.copy()
	print("\n\n\n")
	print("		COUNTOUR INFO")
	peri = c.size
	print("		Perimeter: " + str(peri))
	area = cv2.contourArea(c)
	print("		Area: " + str(math.ceil(area)))
	#Find the minimum enclosing circle
	(x,y),radius = cv2.minEnclosingCircle(c)
	center = (int(x),int(y))
	radius = int(radius)
	cv2.circle(imgCopy,center,radius,(0,0,255),2)
	print("		Diameter: " + str(2*radius))
	#draw all of that
	cv2.drawContours(imgCopy, c, -1, (0, 255, 0), 2)
	cv2.imshow("Original Image", imgCopy)
	cv2.waitKey(0)
cv2.destroyAllWindows()
