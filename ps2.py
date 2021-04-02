# USAGE
# python problem2.py --image image/image1.jpg

# import the necessary packages
import numpy as np
import argparse
from matplotlib import pyplot as plt
import math
import cv2

archive_name = "Input/k.jpg"

#Loading the image and making it a grey level one
image = cv2.imread(archive_name)
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(width, height) = grey.shape
filtered = grey

#As the problem requests we will it from n=0 to n=30
for i in range(0,31):

	#preallocate some memory
	cm_filtered = np.zeros((256, 256))
	cm_residual = np.zeros((256, 256))
	residual = grey - filtered;

	#Calculate the co-occurrence matrix
	for x in range(0,width-1):
		for y in range(0,height-1):
			#coocurrence matrix of the filtered image
			cm_filtered[filtered[x,y], filtered[x+1,y]] += 1
			cm_filtered[filtered[x,y], filtered[x-1,y]] += 1
			cm_filtered[filtered[x,y], filtered[x,y+1]] += 1
			cm_filtered[filtered[x,y], filtered[x,y-1]] += 1

			#Coocurrence matrix of the residual image
			cm_residual[residual[x,y], residual[x+1,y]] += 1
			cm_residual[residual[x,y], residual[x-1,y]] += 1
			cm_residual[residual[x,y], residual[x,y+1]] += 1
			cm_residual[residual[x,y], residual[x,y-1]] += 1

	#preallocate more memory
	homogeneity_filtered = 0
	homogeneity_residual = 0
	uniformity_filtered = 0
	uniformity_residual = 0
	#get the sum of the elements on coocurrence matrixes
	n_filtered = cm_filtered.sum()
	n_residual = cm_residual.sum()


	#Get some insight from the matrixes
	for x in range(0,256):
		for y in range(0,256):
			#As defined on the slides provided =
			p = cm_filtered[x,y]/n_filtered
			homogeneity_filtered += (p)/(1 + abs(x-y))
			uniformity_filtered += p ** 2

			p = cm_residual[x,y]/n_residual
			homogeneity_residual += (p)/(1 + abs(x-y))
			uniformity_residual += p ** 2

	#print it all as a CSV
	print(
		str(i) + "," + 
		str(homogeneity_filtered) + "," +
		str(uniformity_filtered) + "," + 
		str(homogeneity_residual) + "," + 
		str(uniformity_residual))

	#update the blurred image for the next iteration
	filtered = cv2.boxFilter(filtered, -1, (3,3))

cv2.imshow("Blurred", filtered)
cv2.imshow("Residual", residual)
cv2.waitKey(0)
cv2.destroyAllWindows()
