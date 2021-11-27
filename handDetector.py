import cv2
import mediapipe as mp
import time
import math
import numpy as np
 
class handDetector():
	def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionCon = detectionCon
		self.trackCon = trackCon
 
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands,
		self.detectionCon, self.trackCon)
		self.mpDraw = mp.solutions.drawing_utils
		self.tipIds = [4, 8, 12, 16, 20]
		print(self.hands)
	 
	def findHands(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)
		# print(results.multi_hand_landmarks)
	 
		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(img, handLms,
					self.mpHands.HAND_CONNECTIONS)
	 
		return img
	 
	def findPosition(self, img, handNo=0, draw=True):
		xList = []
		yList = []
		bbox = []
		self.lmList = []
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]
			for id, lm in enumerate(myHand.landmark):
				# print(id, lm)
				h, w, c = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				xList.append(cx)
				yList.append(cy)
				# print(id, cx, cy)
				self.lmList.append([id, cx, cy])
				if draw:
					cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
		try:
			xmin, xmax = min(xList), max(xList)
			ymin, ymax = min(yList), max(yList)
			bbox = xmin, ymin, xmax, ymax
		except:
			bbox = (0,0)     
			xmin, ymin, xmax, ymax = 0,0,0,0
		if draw:
			cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
			(0, 255, 0), 2)
	 
		return self.lmList
	 
	def fingersUp(self):
		fingers = []
		# Thumb
		if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
			fingers.append(1)
		else:
			fingers.append(0)
	 
		# Fingers
		for id in range(1, 5):
			if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
				fingers.append(1)
			else:
				fingers.append(0)
	 
			 # totalFingers = fingers.count(1)
			 
	 
		return fingers