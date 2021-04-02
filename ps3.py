import numpy as np
import argparse
from matplotlib import pyplot as plt
import math
import cv2


archive_name="gummy.jpg"
#Loading the image and making it a grey level one
image = cv2.imread(archive_name)
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#threshold the grey level image to make a better edge detection
tret,thresh = cv2.threshold(grey,220,255,cv2.THRESH_BINARY)

#Find all the edges and put them on screen
edged = cv2.Canny(thresh, 200, 210)
cv2.imshow("Edged Image", edged)

#Find the countours
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Sort the countours and prepare a mask
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
mask = np.ones(thresh.shape, dtype="uint8") * 255


# loop over the contours
for c in cnts:

	#Find the minimum encolsing circle
	(x,y),radius = cv2.minEnclosingCircle(c)
	center = (int(x),int(y))
	radius = int(radius)

	#If the radius of the minimum enclosing circles is too small
	#It's probavly an artifact so we will ignore it
	if radius > 20:
		#Find the moments
		M = cv2.moments(c)

		#Find the center of mass
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		#Find the direction
		rows,cols = image.shape[:2]
		[vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)

		#Find a bounding rectangle (auxiliar step to make it easir to draw the line)
		u,v,w,h = cv2.boundingRect(c)

		#Define the line cordinates
		line_x1 = int(x + radius*(vx)*1.1)
		line_y1 = int(y + radius*(vy)*1.1)

		line_x2 = int(x - radius*(vx)*1.1)
		line_y2 = int(y - radius*(vy)*1.1)

		#Find the ellipse (eccentricity)
		ellipse = cv2.fitEllipse(c)
		
		#Draw it all in the image
		cv2.ellipse(image,ellipse,(125,255,0),2)
		cv2.line(image,(line_x1,line_y1),(line_x2,line_y2),(70,125,180),2)
		cv2.circle(image,(cx, cy), 5, (255,0,0), -1)

		#Show it all on screen
		cv2.imshow("Original Image", image)
		cv2.imshow("Tresh Image", thresh)
		cv2.waitKey(0)


cv2.destroyAllWindows()
