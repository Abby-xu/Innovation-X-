from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2
import json
import base64

def process_image(filename):

	# load the image and perform pyramid mean shift filtering
	# to aid the thresholding step
	# image = cv2.imread(args["image"])

	img = cv2.imread(filename)
	# with open("imageToSave.png", "wb") as fh:
	# 	fh.write(base64.decodebytes(ident))
	# img = cv2.imread('imageToSave.png')
	image = cv2.resize(img, None, fx=22, fy=22)
	shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)


	# convert the mean shift image to grayscale, then apply
	# Otsu's thresholding
	gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
	# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	ret, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
	#cv2.imshow("gray", gray)
	#cv2.imshow("blurred", blurred)
	#cv2.imshow("Thresh", thresh)

	# compute the exact Euclidean distance from every binary
	# pixel to the nearest zero pixel, then find peaks in this
	# distance map
	D = ndimage.distance_transform_edt(thresh)
	localMax = peak_local_max(D, indices=False, min_distance=150,
		labels=thresh)

	# perform a connected component analysis on the local peaks,
	# using 8-connectivity, then appy the Watershed algorithm
	markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
	labels = watershed(-D, markers, mask=thresh)

	#print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

	# loop over the unique labels returned by the Watershed
	# algorithm
	peaks_arr = []
	for label in np.unique(labels):
		# if the label is zero, we are examining the 'background'
		# so simply ignore it
		if label == 0:
			continue
		# otherwise, allocate memory for the label region and draw
		# it on the mask
		mask = np.zeros(gray.shape, dtype="uint8")
		mask[labels == label] = 255
		# detect contours in the mask and grab the largest one
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
		# draw a circle enclosing the object
		((x, y), r) = cv2.minEnclosingCircle(c)
		center_pixel = image[int(y), int(x)]
		lum = (int(center_pixel[0]) + int(center_pixel[1]) + int(center_pixel[2])) / 3
		if (lum >= 30) and (int(r) < 900) and (int(r) > 120):
			cv2.circle(image, (int(x), int(y)), int(0.3*r), (0, 255, 0), 2)
		#get pixel colors
		if lum >= 30: #cutoff threshold for blob
			peaks_arr.append(lum)

		cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

	#show luminance array
	# show the output image
	#cv2.imshow("Output", image)
	#cv2.waitKey(0)
	data_set = {'Count': f'{peaks_arr}'}
	json_dump = json.dumps(data_set)

	return json_dump
