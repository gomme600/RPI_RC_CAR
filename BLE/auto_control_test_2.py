from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
import numpy as np
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
import time
import cv2

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes. I use BCM  
  
GPIO.setup(38, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port  
GPIO.setup(36, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port
GPIO.setup(31, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port
GPIO.setup(29, GPIO.OUT) # set GPIO 25 as an output. You can use any GPIO port

FR = GPIO.PWM(38, 500)    # create an object p for PWM on port 25 at 50 Hertz
BR = GPIO.PWM(36, 500)    # create an object p for PWM on port 25 at 50 Hertz
FL = GPIO.PWM(29, 500)    # create an object p for PWM on port 25 at 50 Hertz
BL = GPIO.PWM(31, 500)    # create an object p for PWM on port 25 at 50 Hertz  
                        # you can have more than one of these, but they need  
                        # different names for each port   
                        # e.g. p1, p2, motor, servo1 etc. 

#video_capture = cv2.VideoCapture(-1)

#video_capture.set(3, 160)

#video_capture.set(4, 120)

toggle_value = 0
check_toggle = True

camera = PiCamera()
camera.resolution = (160, 120)
#camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(160, 120))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
    frame = frame.array
 

    # Capture the frames

    #ret, frame = video_capture.read()

 

    # Crop the image

    crop_img = frame[60:120, 0:160] #Top left is pixel 0, usage: frame[y1:y2, x1:x2]. We don't crop x as we need the image centered

 

    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

 

    # Gaussian blur

    blur = cv2.GaussianBlur(gray,(5,5),0)

 

    # Color thresholding

    frame,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

 

    # Find the contours of the frame

    img,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

 

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

 
        if(M['m00'] != 0):
            cx = int(M['m10']/M['m00'])

            cy = int(M['m01']/M['m00'])

 

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

 

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

 

        if cx >= 120:

            print "Turn Right!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            BR.start(28)
            FL.start(28)

        if cx < 90 and cx > 70:

            print "On Track Slow!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(22)
            FL.start(22)

        if cx < 120 and cx >= 90 and cx:

            print "On Track Fast!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()  
            FR.start(32)
            FL.start(32)

        if cx <= 70 and cx > 50:

            print "On Track Slow!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()  
            FR.start(22)
            FL.start(22)

        if cx <= 50:

            print "Turn Left!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(28)
            BL.start(28)

    else:

        print "I don't see the line"

        FR.stop()
        FL.stop()
        BR.stop()
        BL.stop()
        check_toggle = not check_toggle
        if(toggle_value < 3):
         BR.start(22)
         BL.start(22)
         time.sleep(0.2)
         FR.stop() 
         FL.stop()
         BR.stop()  
         BL.stop()
         if(check_toggle == False):
            FR.start(40)
            BL.start(40)
            time.sleep(0.2) 
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            BR.start(40)
            FL.start(40)
            time.sleep(0.2)
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            toggle_value = toggle_value+1
         else:
            BR.start(40)
            FL.start(40)
            time.sleep(0.2)
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            FR.start(40)
            BL.start(40)
            time.sleep(0.2) 
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            toggle_value = toggle_value+1

    #Display the resulting frame

    cv2.imshow('frame',crop_img)
    rawCapture.truncate(0)	

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
        FR.stop()
        FL.stop()
        BR.stop()
        BL.stop()
