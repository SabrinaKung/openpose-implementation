import sys
import cv2
import imutils
import os
from sys import platform
import argparse
import numpy as np

def wxfopenpose(i):
	try:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		try:
			sys.path.append('../../python')
			from openpose import pyopenpose as op
		except ImportError as e:
			print(
					'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
			raise e
		parser = argparse.ArgumentParser()
		args = parser.parse_known_args()
		params = dict()
		params["model_folder"] = "../../../models/"
		params["face"] = True
		params["hand"] = True
		for i in range(0, len(args[1])):
			curr_item = args[1][i]
			if i != len(args[1]) - 1:
				next_item = args[1][i + 1]
			else:
				next_item = "1"
			if "--" in curr_item and "--" in next_item:
				key = curr_item.replace('-', '')
				if key not in params:  params[key] = "1"
				elif "--" in curr_item and "--" not in next_item:
					key = curr_item.replace('-', '')
				if key not in params: params[key] = next_item
		opWrapper = op.WrapperPython()
		opWrapper.configure(params)
		opWrapper.start()
		datum = op.Datum()
		#imageToProcess = cv2.imread('../../examples/media/COCO_val2014_000000000241.jpg')
		datum.cvInputData = i
		#opWrapper.emplaceAndPop([datum])
		opWrapper.emplaceAndPop(op.VectorDatum([datum]))
		# print(f"I defind -> type of body keypoints = {type(datum.poseKeypoints)}")
		# print("Body keypoints: \n" + str(datum.poseKeypoints))
		# print("Face keypoints: \n" + str(datum.faceKeypoints))
		# print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
		# print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
		# cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", datum.cvOutputData)
		# cv2.waitKey(0)
		return datum
	except Exception as e:
		print(e)
		sys.exit(-1)

# 打開鏡頭
capture = cv2.VideoCapture(0)

# 設定影像尺寸
width = 1280
height = 960

# 設定擷取影像的尺寸大小
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

pic_taken = 1

while(True):

	# input image
	ret, frame = capture.read()

	# 轉換成有骨架的frame
	a = wxfopenpose(frame)
	frame2 = a.cvOutputData

	cv2.rectangle(frame2, (50,50), (400,300), (255,255,255), thickness=5)
	cv2.putText(frame2,"Smile!", (150, 30),cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

	if_pic_taken = 0
	
	# 判斷骨架的座標點是否在熱區內
	for i in range(0,25):
		# 身體骨架座標點
		if (50<=a.poseKeypoints[0][i][0]<=400 and 50<=a.poseKeypoints[0][i][1]<=300):
			print(pic_taken,"photo taken!")
			cv2.imwrite('./photo_shoot/'+str(pic_taken)+'.jpg',frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			if_pic_taken = 1
			print("=++++++++++++++++++++++++++++++++++++++")
			break
	
	for i in range(0,20):
		# 第二個人的手部骨架座標點
		if(50<=a.handKeypoints[1][0][i][0]<=400 and 50<=a.handKeypoints[1][0][i][1]<=300):
			cv2.imwrite('./photo_shoot/'+str(pic_taken)+'.jpg',frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			print(pic_taken,"photo taken!")
			if_pic_taken = 1
			print("=++++++++++++++++++++++++++++++++++++++")
			break
			print("=++++++++++++++++++++++++++++++++++++++")
		
		# 第一個人的手部骨架座標點
		elif(50<=a.handKeypoints[0][0][i][0]<=400 and 50<=a.handKeypoints[0][0][i][1]<=300):
			print(pic_taken,"photo taken!")
			cv2.imwrite('./photo_shoot/'+str(pic_taken)+'.jpg',frame2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			if_pic_taken = 1
			print("=++++++++++++++++++++++++++++++++++++++")
			break
	
	if if_pic_taken:
		pic_taken += 1


	cv2.imshow('frame', frame2)
	if cv2.waitKey(1) == ord('q'):
		break