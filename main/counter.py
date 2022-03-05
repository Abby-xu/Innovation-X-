import flask
import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


#api
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#db
class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	description = db.Column(db.String(20), nullable=True, default="dot.png")

	def __repr__(self):
		return f"{self.name} - {self.description}"

	

@app.route('/droplets/<ident>', methods=['GET', 'POST'])
def home_page(ident):
	import matplotlib
	matplotlib.use('Agg')

	# import the necessary packages
	from skimage.feature import peak_local_max
	from skimage.segmentation import watershed
	from scipy import ndimage
	import numpy as np
	import argparse
	import imutils
	import cv2
	import base64

	

	# load the image and perform pyramid mean shift filtering
	# to aid the thresholding step
	# image = cv2.imread(args["image"])

	img = cv2.imread('dots.png')
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
	data_set = {'Count': f'{peaks_arr}', 'id':ident}
	json_dump = json.dumps(data_set)

	return json_dump

@app.route('/droplets')
def get_pics():
	pics = Item.query.all()

	output = []
	for p in pics:
		pic_data = {'name': p.name, 'description': p.description}
		output.append(pic_data)
	
	return {"pics": output}

@app.route('/droplets/<id>')
def get_pic(id):
	pic = Item.query.get_or_404(id)
	return {"name": pic.name, "description": pic.description}

@app.route('/droplets', methods=['POST'])
def add_pic():
	content = request.get_json(force=True)
	pic = Item(name=content['name'], description=content["description"])
	db.session.add(pic)
	db.session.commit()
	return {'id': pic.id}

@app.route('/droplets/<ident>', methods=['DELETE'])
def del_pic(ident):
	pic = Item.query.get(ident)
	if pic is None:
		return 404
	db.session.delete(pic)
	db.session.commit()
	return "Deleted!"

if __name__ == "__main__":
    app.run(debug=True)