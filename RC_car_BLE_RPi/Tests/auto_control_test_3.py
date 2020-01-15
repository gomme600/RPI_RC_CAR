from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port  
GPIO.setup(36, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port
GPIO.setup(31, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port
GPIO.setup(29, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port

FR = GPIO.PWM(38, 1000)    # create an object p for PWM on port 25 at 50 Hertz
BR = GPIO.PWM(36, 1000)    # create an object p for PWM on port 25 at 50 Hertz
FL = GPIO.PWM(29, 1000)    # create an object p for PWM on port 25 at 50 Hertz
BL = GPIO.PWM(31, 1000)    # create an object p for PWM on port 25 at 50 Hertz  
                        # you can have more than one of these, but they need  
                        # different names for each port   
                        # e.g. p1, p2, motor, servo1 etc. 

camera = PiCamera()
camera.resolution = (640, 360)
#camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640, 360))
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	image = frame.array	
	Blackline = cv2.inRange(image, (0,0,0), (60,60,60))	
	kernel = np.ones((3,3), np.uint8)
	Blackline = cv2.erode(Blackline, kernel, iterations=5)
	Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
	img_blk,contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours_blk) > 0:	 
	 blackbox = cv2.minAreaRect(contours_blk[0])
	 (x_min, y_min), (w_min, h_min), ang = blackbox
	 if ang < -45 :
	  ang = 90 + ang
	 if w_min < h_min and ang > 0:	  
	  ang = (90-ang)*-1
	 if w_min > h_min and ang < 0:
	  ang = 90 + ang	  
	 setpoint = 320
	 error = int(x_min - setpoint) 
	 ang = int(ang)	 
	 box = cv2.boxPoints(blackbox)
	 box = np.int0(box)
	 cv2.drawContours(image,[box],0,(0,0,255),3)	 
	 cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
	 cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	 cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)
	
         if( (ang < -4) ):

            print("Turn Left")
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(25)
            BL.start(25)

         if( (ang > 4) ):

            print("Turn Right")
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            BR.start(25)
            FL.start(25)

         if( (ang < 4) & (ang > -4) ):

            print("Straight")
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()   
            FR.start(25)
            FL.start(25) 
	 
        else:
          print("Line not detected!")
          FR.stop()
          FL.stop()
          BR.stop()   
          BL.stop()
 	
	cv2.imshow("orginal with line", image)	
	rawCapture.truncate(0)

       		
	key = cv2.waitKey(1) & 0xFF	
	if key == ord("q"):
		break
