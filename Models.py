import cv2
from handDetector import *

class Models():
	
	def __init__(self):	
		self.detector = handDetector()
		
		self.cap = cv2.VideoCapture(0)
		self.cap.set(3,1280)

		self.thickness = 10
		self.imgCanvas = np.zeros((720,1280,3),np.uint8)
		self.color =(255,0,0,0)
		self.px = -1
		self.py = -1

		self.mx = -1
		self.my = -1

		self.color_selected = 1
		self.shapeselected = 5


	def detect(self):
		self.success, self.img = self.cap.read()
		self.img = cv2.flip(self.img,1)

		self.img = self.detector.findHands(self.img)

		self.height, self.width = self.img.shape[:2]
		self.x = (self.width-5)/10

	def selectColor(self):
		if self.color_selected == 0:
			self.color = (0,0,0)
		if self.color_selected == 1:
			self.color = (0,0,255)
		if self.color_selected == 2:
			self.color = (0,255,0)
		if self.color_selected == 3:
			self.color = (255,0,255)
		if self.color_selected == 4:
			self.color = (0,0,0)

	def drawColor(self):
		self.img = cv2.rectangle(self.img,(int(self.color_selected)*int(self.x)+8+5,5+8),(int(self.color_selected+1)*int(self.x)-8,100-5-8),(255,255,0),10)
		self.img = cv2.rectangle(self.img,(0*int(self.x)+5+8,5+8),(1*int(self.x)-8,100-5-8),(0,0,0),-1)
		self.img = cv2.rectangle(self.img,(1*int(self.x)+8+5,5+8),(2*int(self.x)-8,100-5-8),(0,0,255),-1)
		self.img = cv2.rectangle(self.img,(2*int(self.x)+5+8,5+8),(3*int(self.x)-8,100-5-8),(0,255,0),-1)
		self.img = cv2.rectangle(self.img,(3*int(self.x)+8+5,5+8),(4*int(self.x)-8,100-5-8),(255,0,255),-1)

	def drawShape(self):
		self.img = cv2.rectangle(self.img,(int(self.shapeselected)*int(self.x)+8+5,5+8),(int(self.shapeselected+1)*int(self.x)-8,100-5-8),(255,255,0),10)
		
		self.img = cv2.rectangle(self.img,(5*int(self.x)+8+5,5+8),(6*int(self.x)-8,100-5-8),(0),-1)
		self.img = cv2.rectangle(self.img,(8*int(self.x)+8+5,5+8),(9*int(self.x)-8,100-5-8),(0),-1)
		self.img = cv2.rectangle(self.img,(6*int(self.x)+8+5,5+8),(7*int(self.x)-8,100-5-8),(0),-1)
		self.img = cv2.rectangle(self.img,(7*int(self.x)+8+5,5+8),(8*int(self.x)-8,100-5-8),(0),-1)
		self.img = cv2.rectangle(self.img,(9*int(self.x)+8+5,5+8),(10*int(self.x)-8,100-5-8),(0),-1)
		
		self.img = cv2.putText(self.img,"FH",(660,75),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3,cv2.LINE_AA)
		self.img = cv2.rectangle(self.img,(int(6)*int(self.x)+8+5+8,5+8+8),(int(6+1)*int(self.x)-8-8,100-5-8-8),(255,0,255),5)
		self.img = cv2.ellipse(self.img,(int(6)*int(self.x)+8+5+8+int(self.x+self.x/2)-18,30+5+8+8),(45,25),0,0,360,(255,0,255),5)
		self.img = cv2.line(self.img,(8*int(self.x)+8+5+10,5+8+10),(9*int(self.x)-8-10,100-15-8),(255,0,255),5)
		self.img = cv2.line(self.img,(9*int(self.x)+8+5+10,5+8+10),(10*int(self.x)-8-10,100-15-8),(255,0,255),5)
		self.img = cv2.line(self.img,(9*int(self.x)+8+5+10,5+8+50),(10*int(self.x)-8-10,100-15-8),(255,0,255),5)

	def drawUI(self):
		self.img = cv2.rectangle(self.img,(5,5),(self.width-5,self.height-5),(50,50,50),10)
		self.img = cv2.rectangle(self.img,(5,5),(self.width-5,100),(50,50,50),-1)
		self.drawColor()
		self.drawShape()

	def convertCanvas(self):	
		self.imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
		self._, self.imgINV = cv2.threshold(self.imgGray,50,255,cv2.THRESH_BINARY_INV)
		self.imgINV= cv2.cvtColor(self.imgINV, cv2.COLOR_GRAY2BGR)
		self.img = cv2.bitwise_and(self.img,self.imgINV)

		self.img = cv2.bitwise_or(self.img,self.imgCanvas)

		cv2.imshow("Image",self.img)

	def input(self):
		k = cv2.waitKeyEx(1)
		if k==27:
			exit()
		if k==97:
			self.imgCanvas = np.zeros((720,1280,3),np.uint8)

		if k==2490368:
			if self.thickness<15 :
				self.thickness += 1
		
		if k==2621440:
			if self.thickness>5:
				self.thickness -= 1

	def movement(self):
		coList = self.detector.findPosition(self.img,draw=False)
		if coList:
			up = self.detector.fingersUp()

			index_finger = (up[1]==1)
			middle_finger = (up[2]==1)


			self.mx = (coList[8][1])
			self.my = (coList[8][2])

			if index_finger:
				if not middle_finger:
					pass
				else:
					if self.my>100:
						pass
					elif self.mx<4*self.x:
						self.color_selected = int(self.mx/self.x)
					elif self.mx>5*self.x and self.mx<10*self.x:
						self.shapeselected = int(self.mx/self.x)	


			if index_finger and not middle_finger:
				if self.shapeselected == 5:
					if self.my>100:
						if self.mx!=-1 and self.px!=-1 and self.mx!=-1 and self.py!=-1:
							self.imgCanvas = cv2.line(self.imgCanvas,(self.mx,self.my),(self.px,self.py),self.color,self.thickness)
					self.px = self.mx
					self.py = self.my

				if self.shapeselected == 6:
					if self.my>100:
						if self.px == -1 and self.py == -1:
							self.px = self.mx
							self.py = self.my
						if self.mx!=-1 and self.px!=-1 and self.mx!=-1 and self.py!=-1:
							self.img = cv2.rectangle(self.img,(self.mx,self.my),(self.px,self.py),self.color,self.thickness)

				if self.shapeselected == 7:
					if self.my>100:
						if self.px == -1 and self.py == -1:
							self.px = self.mx
							self.py = self.my
						if self.mx!=-1 and self.px!=-1 and self.mx!=-1 and self.py!=-1:
							if self.mx>self.px and self.my>self.py:
								self.img = cv2.ellipse(self.img,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.mx-self.px)/2),int((self.my-self.py)/2)),0,0,360,self.color,self.thickness)

							if self.mx>self.px and self.my<self.py:
								self.img = cv2.ellipse(self.img,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.mx-self.px)/2),int((self.py-self.my)/2)),0,0,360,self.color,self.thickness)

							if self.mx<self.px and self.my>self.py:
								self.img = cv2.ellipse(self.img,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.px-self.mx)/2),int((self.my-self.py)/2)),0,0,360,self.color,self.thickness)

							if self.mx<self.px and self.my<self.py:
								self.img = cv2.ellipse(self.img,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.px-self.mx)/2),int((self.py-self.my)/2)),0,0,360,self.color,self.thickness)


				if self.shapeselected == 9:
					if self.my>100:
						if self.px == -1 and self.py == -1:
							self.px = self.mx
							self.py = self.my
						if self.mx!=-1 and self.px!=-1 and self.mx!=-1 and self.py!=-1:
							self.img = cv2.line(self.img,(self.mx,self.my),(self.px,self.my),self.color,self.thickness)
							self.img = cv2.line(self.img,(int((self.mx+self.px)/2),self.py),(self.mx,self.my),self.color,self.thickness)
							self.img = cv2.line(self.img,(int((self.mx+self.px)/2),self.py),(self.px,self.my),self.color,self.thickness)

				if self.shapeselected == 8:
					if self.my>100:
						if self.px == -1 and self.py == -1:
							self.px = self.mx
							self.py = self.my

						if self.mx!=-1 and self.px!=-1 and self.mx!=-1 and self.py!=-1:
							self.img = cv2.line(self.img,(self.mx,self.my),(self.px,self.py),self.color,self.thickness)


			else:
				if self.shapeselected == 6 and self. px!=-1 and self.py!=-1:
					self.imgCanvas = cv2.rectangle(self.imgCanvas,(self.mx,self.my),(self.px,self.py),self.color,self.thickness) 
				if self.shapeselected == 7 and self. px!=-1 and self.py!=-1:
					if self.mx>self.px and self.my>self.py:
						self.imgCanvas = cv2.ellipse(self.imgCanvas,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.mx-self.px)/2),int((self.my-self.py)/2)),0,0,360,self.color,self.thickness)

					if self.mx>self.px and self.my<self.py:
						self.imgCanvas = cv2.ellipse(self.imgCanvas,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.mx-self.px)/2),int((self.py-self.my)/2)),0,0,360,self.color,self.thickness)

					if self.mx<self.px and self.my>self.py:
						self.imgCanvas = cv2.ellipse(self.imgCanvas,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.px-self.mx)/2),int((self.my-self.py)/2)),0,0,360,self.color,self.thickness)

					if self.mx<self.px and self.my<self.py:
						self.imgCanvas = cv2.ellipse(self.imgCanvas,(int((self.mx+self.px)/2),int((self.my+self.py)/2)),(int((self.px-self.mx)/2),int((self.py-self.my)/2)),0,0,360,self.color,self.thickness)

				if self.shapeselected == 8 and self. px!=-1 and self.py!=-1:
					self.imgCanvas = cv2.line(self.imgCanvas,(self.mx,self.my),(self.px,self.py),self.color,self.thickness)
				if self.shapeselected == 9 and self. px!=-1 and self.py!=-1:
					self.imgCanvas = cv2.line(self.imgCanvas,(int((self.mx+self.px)/2),self.py),(self.mx,self.my),self.color,self.thickness)
					self.imgCanvas = cv2.line(self.imgCanvas,(int((self.mx+self.px)/2),self.py),(self.px,self.my),self.color,self.thickness)
					self.imgCanvas = cv2.line(self.imgCanvas,(self.px,self.my),(self.mx,self.my),self.color,self.thickness)
				self.px = -1
				self.py = -1

	def run(self) :
		self.detect()
		self.selectColor()
		self.drawUI()
		self.input()
		self.movement()
		self.convertCanvas()
		