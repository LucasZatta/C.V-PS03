import numpy as np
import argparse
import cv2
import sys
import random
import imutils
import math

# this variable will indicate when create a line segment 
#(after the second mouse click. 1st click to the 1st point and 2nd to the last point)
CLICK = -1 
# global X cordenate of mouse click
X = 0
# global Y cordenate of mouse click
Y = 0

#take the first parameter as the image size
size = 300

#some logging info
print('Creating image with size:' + str(size) + 'x' + str(size))

#preallocating some memory
image = np.full((size,size), 255, np.uint8)

#noisy generating function
def sp_noise(prob):
	global image
	output = np.zeros(image.shape,np.uint8)
	thres = 1 - prob
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			rdn = random.random()
			if rdn < prob:
				output[i][j] = 0
			else:
				output[i][j] = image[i][j]
	return output


#noisy line function
def sp_noise_line(prob, m,b,x_interval,y_interval):
	#xs = np.linspace(x_interval[0],x_interval[1],20)
	#ys = np.interp(xs, x_interval, y_interval)

	global image

	if x_interval[0] <= x_interval[1]:
		x1 = x_interval[0]
		x2 = x_interval[1]
	else:
		x1 = x_interval[1]
		x2 = x_interval[0]

	if y_interval[0] <= y_interval[1]:
		y1 = y_interval[0]
		y2 = y_interval[1]
	else:
		y1 = y_interval[1]
		y2 = y_interval[0]

	if((x2-x1)>(y2-y1)):
		for x in range(x1,x2):
				rdn = random.random()
				if rdn < prob:
					y = int(m*x + b)
					image[y+random.randint(1, 5)][x++random.randint(1, 3)] = 0
					image[y+random.randint(1, 5)][x++random.randint(1, 3)] = 0
	else:
		for y in range(y1,y2):
				rdn = random.random()
				if rdn < prob:
					x = int((y - b)/m)
					image[y+random.randint(1, 5)][x++random.randint(1, 3)] = 0
					image[y+random.randint(1, 5)][x++random.randint(1, 3)] = 0



def on_mouse_click(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		# load the image, convert it to grayscale, blur it slightly,
		# and threshold it
		global CLICK
		global X
		global Y
		global image


		CLICK = CLICK+1

		if(CLICK%2 == 0):
			print("Click on two points on the image to generate a line or press ENTER to quit")
			X = x
			Y = y
		else:
			if (x-X) == 0:
				x = x+1
			m =  float(y-Y)/(x-X)
			b = (-1*m*X)+Y
			print ("  f(x) = "+str(m)+"x"+" + "+str(b))
			sp_noise_line(0.8, m,b,[X,x],[Y,y])



		
		# show the image
		cv2.imshow("Image 1", image)

#defien the image
image = sp_noise(0.01)

#Create the windows
cv2.namedWindow('Image 1')

#Put mouse callback attached to the window
cv2.setMouseCallback('Image 1',on_mouse_click)

#wait for user input before continuing
while(1):
	cv2.imshow('Image 1',image)
	k = cv2.waitKey(0)
	if k:
		break

print ("\n\n\n")


#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
tret,thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)



#calculate the Loines by using the hough probabilistic algorithm
lines = cv2.HoughLinesP(image=thresh,rho=1,theta=np.pi/500, threshold=50, minLineLength=25, maxLineGap=25)

#Draw the lines
linesDrawing = np.ones((size,size,3))

#For each line in the resulting set
print(lines)
for line in lines:
	x1,y1,x2,y2 = line[0]
	print(str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2))
	cv2.line(linesDrawing,(x1,y1),(x2,y2),(0,255,0),2)


# show the images
cv2.imshow("Lines", linesDrawing)

cv2.waitKey(0)



#destroy all windows
cv2.destroyAllWindows()