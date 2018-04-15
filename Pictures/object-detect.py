'''Project: IP Camera OpenCV Monstrocity of Lost Souls
   A CrimsonHacks 2018 entry
   by Matthew Petry and Jonathan Blake

   Server script -- object detection (by color) and text messaging
   developed by Matthew Petry

   Various code snippets derived from the following URLs:

   https://thecodacus.com/opencv-object-tracking-colour-detection-python/
   https://www.learnopencv.com/blob-detection-using-opencv-python-c/
   https://www.makehardware.com/2016/05/19/blob-detection-with-python-and-opencv/

'''



# import the necessary packages
import numpy as np
import argparse
import cv2
import time
import os.path

from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "<SID here>"
# Your Auth Token from twilio.com/console
auth_token  = "<TOKEN here>"

smsclient = Client(account_sid, auth_token)

objectNames = ["CH Bag", "Paper Bag"]

# load the image
# define the list of boundaries
boundaries = [
	([17, 15, 180], [70, 90, 255]),
#	([80, 60, 0], [255, 200, 60]),
	([140, 140, 140], [255, 255, 255]),
]

detectParam = cv2.SimpleBlobDetector_Params()
detectParam.filterByColor = True
detectParam.blobColor = 0
detectParam.filterByArea = True
detectParam.filterByCircularity = False
detectParam.filterByConvexity = False
detectParam.filterByInertia = False
detectParam.minThreshold = 0
detectParam.maxThreshold = 256
detectParam.thresholdStep = 5
detectParam.minArea = 5000
detectParam.maxArea = 2000000
detector = cv2.SimpleBlobDetector_create(detectParam)


def messagealert(objects):
	print("Sending message...")
	smsclient.api.account.messages.create(
	       to="+12517692791",
	       from_="+12513877795",
	       body="Alert! You have left the following objects: "+objects)



# loop over the boundaries
def objectdetect():
	objects = [0,0]
	i = 0
	#imagefile = args["image"] + "/opencv.png"
	image = cv2.imread("opencv.png")
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)

		kernelOpen=np.ones((5,5))
		kernelClose=np.ones((20,20))

		maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
		maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
		maskClose = cv2.bitwise_not(maskClose)


		keypoints = detector.detect(maskClose)
		im_with_keypoints = cv2.drawKeypoints(maskClose, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)	
		if (len(keypoints) > 0):
			print("Object is still there!");
			objects[i] = 1
		else:
			print("Object is missing!");
			objects[i] = 0

		print(keypoints)
#		print(objects)
		i = i + 1

		# show the images
#		cv2.imshow("images", im_with_keypoints)
#		cv2.waitKey(0)
	return objects

#while True:
if (os.path.isfile("laststate")):
	f = open("laststate", 'r')
	laststate = [int(line.rstrip('\n')) for line in f]
	print("Last state: ")
	print(laststate)
objects = objectdetect()
print("Objects found:")
i = 0
objnum = len(objects)
for i in range(0, objnum):
	if objects[i] == 1:
		print(objectNames[i])
leftbehind = [0,0,0]
textobjects = []
if os.path.isfile("vacant.txt"):
	print("User has left. Will send text message if necessary.")
	for i in range(0, objnum):
		if (objects[i] == laststate[i]) and (objects[i] == 1):
			leftbehind[i] = 1
	print("Objects left behind: ")
	for i in range(0, objnum):
		if leftbehind[i] == 1:
			print(objectNames[i])
			textobjects.append(objectNames[i])
			objectstring = ", ".join(textobjects)
	messagealert(objectstring)
else:
	print("User is returning. Do not send text message.")

f = open("laststate", 'w')
for i in range(0, objnum):
	f.write(str(objects[i])+'\n')
f.close()
#else:
#	print("File currently being edited. Doing nothing on this iteration.")
#	time.sleep(6)
	
#smsclient.api.account.messages.create(
#	to="+12517692791",
#	from_="+12513877795",
#	body="Hello there!")	
