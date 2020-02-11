#!/usr/bin/env python3

#Auto drive example software made for the NeOCampus car
#Will follow a black line using the RPi camera module
#Code inspired by : http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
#Author: Sebastian Lucas - 2019-2020

##########################
##----USER SETTINGS----###
##########################

#Time to rev up the motors to overcome initial force (in seconds)
REVUP_TIME = 0.005

#REVUP speed PWM value
REVUP_SPEED = 90

##########################
##----END  SETTINGS----###
##########################

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


def auto_drive(FR,FL,BR,BL,auto_drive_on):

 #Values used for swaying the vehicule left-right in case we loose the line (see below)
 toggle_value = 0
 check_toggle = True

 #Setup the camera
 camera = PiCamera()
 camera.resolution = (160, 120)

 #Rotate camera if needed on another vehicule
 #camera.rotation = 180
 rawCapture = PiRGBArray(camera, size=(160, 120))
 time.sleep(0.1)

 for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
    frame = frame.array
 

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

 
        #Based on the line position we control the vehicule
        #Turn right
        if cx >= 120:

            print "Turn Right!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            BR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            BR.stop()
            FL.stop()
            BR.start(28)
            FL.start(28)

        #Foward slow
        if cx < 90 and cx > 70:

            print "On Track Slow!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            FR.stop()
            FL.stop()
            FR.start(22)
            FL.start(22)

        #Foward fast
        if cx < 120 and cx >= 90 and cx:

            print "On Track Fast!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME) 
            FR.stop()   
            FL.stop()
            FR.start(32)
            FL.start(32)

        #Foward slow
        if cx <= 70 and cx > 50:

            print "On Track Slow!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            FR.stop()   
            FL.stop()
            FR.start(22)
            FL.start(22)

        #Turn left
        if cx <= 50:

            print "Turn Left!"
            toggle_value = 0
            FR.stop()
            FL.stop()
            BR.stop()
            BL.stop()
            FR.start(REVUP_SPEED)
            BL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            FR.stop()   
            BL.stop()
            FR.start(28)
            BL.start(28)

    #No line to follow
    else:

        print "I don't see the line"

        #We stop moving
        FR.stop()
        FL.stop()
        BR.stop()
        BL.stop()

        #We sway the camera left-right and reverse the vehicule in an attempt to find the line again
        #If we don't find the line after 3 attempts we give up
        check_toggle = not check_toggle
        if(toggle_value < 3):
         BR.start(REVUP_SPEED)
         BL.start(REVUP_SPEED)
         time.sleep(REVUP_TIME)
         BR.stop()   
         BL.stop()
         BR.start(22)
         BL.start(22)
         time.sleep(0.2)
         FR.stop() 
         FL.stop()
         BR.stop()  
         BL.stop()
         if(check_toggle == False):
            FR.start(REVUP_SPEED)
            BL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            FR.stop()   
            BL.stop()
            FR.start(40)
            BL.start(40)
            time.sleep(0.2) 
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            BR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            BR.stop()   
            FL.stop()
            BR.start(40)
            FL.start(40)
            time.sleep(0.2)
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            toggle_value = toggle_value+1
         else:
            BR.start(REVUP_SPEED)
            FL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            BR.stop()   
            FL.stop()
            BR.start(40)
            FL.start(40)
            time.sleep(0.2)
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            FR.start(REVUP_SPEED)
            BL.start(REVUP_SPEED)
            time.sleep(REVUP_TIME)
            FR.stop()   
            BL.stop()
            FR.start(40)
            BL.start(40)
            time.sleep(0.2) 
            FR.stop()
            FL.stop()
            BR.stop()  
            BL.stop()
            toggle_value = toggle_value+1

    #Display the resulting frame (activate to see the camera output on attached display)

    #cv2.imshow('frame',crop_img)
    rawCapture.truncate(0)	

    #We check if the user still wants autonomous mode, if not we exit
    if auto_drive_on() == False: 
                camera.close()
                FR.stop()
                FL.stop()
                BR.stop()
                BL.stop()
                break
