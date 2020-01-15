# Don't try to run this as a script or it will all be over very quickly  
# it won't do any harm though.  
# these are all the elements you need to control PWM on 'normal' GPIO ports  
# with RPi.GPIO - requires RPi.GPIO 0.5.2a or higher  
  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
import time
import pygame
  
pygame.init()
pygame.display.set_mode((100, 100))

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes. I use BCM  
  
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
  
while(True):

  for event in pygame.event.get():

    #mvt = input("Direction (zqsd) : ")

    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            FR.start(50)
            FL.start(50)
    elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
            FR.stop()
            FL.stop() 
 
    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            BR.start(50)
            BL.start(50)
    elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            BR.stop()
            BL.stop()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            FR.start(50)
            BL.start(50)
    elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            FR.stop()
            BL.stop()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            BR.start(50)
            FL.start(50)
    elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            BR.stop()
            FL.stop()

'''
    if(mvt == "z"):
        FR.start(50)
        FL.start(50)
        time.sleep(1)
        FR.stop()
        FL.stop()

    if(mvt == "s"):
        BR.start(50)
        BL.start(50)
        time.sleep(1)
        BR.stop()
        BL.stop()

    if(mvt == "q"):
        FR.start(50)
        BL.start(50)
        time.sleep(1)
        FR.stop()
        BL.stop()

    if(mvt == "d"):
        BR.start(50)
        FL.start(50)
        time.sleep(1)
        BR.stop()
        FL.stop()
'''
'''

    FR.start(50)             # start the PWM on 50 percent duty cycle  
    #BR.start(50)             # start the PWM on 50 percent duty cycle
    #BL.start(50)             # start the PWM on 50 percent duty cycle
    FL.start(50)             # start the PWM on 50 percent duty cycle
                        # duty cycle value can be 0.0 to 100.0%, floats are OK  
    time.sleep(2)  
    FR.ChangeDutyCycle(90)   # change the duty cycle to 90%  
    #BR.ChangeDutyCycle(90)   # change the duty cycle to 90% 
    #BL.ChangeDutyCycle(90)   # change the duty cycle to 90% 
    FL.ChangeDutyCycle(90)   # change the duty cycle to 90% 

    time.sleep(2)  
    FR.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)
    #BR.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)
    #BL.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)
    FL.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)  
                        # e.g. 100.5, 5.2  
    time.sleep(2)

    FR.stop()                # stop the PWM output  
    #BR.stop()                # stop the PWM output  
    #BL.stop()                # stop the PWM output  
    FL.stop()                # stop the PWM output  
'''
  
GPIO.cleanup()          # when your program exits, tidy up after yourself
