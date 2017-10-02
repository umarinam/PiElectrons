# -*- coding: utf-8 -*-
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import sys
import RPi.GPIO as gpio
from time import time
#from sendingtextviasocket import *
from motorcontrolviapi import *
#Variables for socket connection to windows pc
#HOST, PORT = '192.168.8.100', 8000
# Create a socket (SOCK_STREAM means a TCP socket)
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((HOST,PORT))
#connection = client_socket.makefile('wb')
interCount = 0

def search(interCount):
    if(interCount > 20):
        left (3 * 0.1)
    else:
        stop(1)
        


try:
#while True:
    res_width=640
    res_height=480
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (res_width, res_height)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(res_width, res_height))
    
     
    # allow the camera to warmup
    time.sleep(0.1)

    greenLower = (50, 93,47)
    greenUpper = (94,247,243)
    starttime = time.time()
    
    # capture frames from the camera
    for capturedframe in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            print "Start Loop"
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            frame = capturedframe.array
            
            #Electrons logic below strats
            
            frame = cv2.flip( frame, 0)
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)            
            
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
         
                # only proceed if the radius meets a minimum size
                if radius > 20:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    interCount = 0
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    #connection.sendall(center, res_width/2)
                    messageToSend = str(center[0])
                    #print messageToSend
                    #print "Hello"
                    SendCommandToRemote(messageToSend)
                    #print "world"
                else:
                    interCount = interCount + 1
                    search(interCount)
            else:
                interCount = interCount + 1
                search(interCount)
                    
            cv2.imshow("Frame", frame)     
            endtime = time.time()
            duration = endtime-starttime
            print endtime-starttime
            delay = 0.0
            if (duration <  delay):
                time.sleep (delay - duration)
            starttime = time.time()
                 # show the frame
            key = cv2.waitKey(1) & 0xFF
     
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            #print "truncate"
     
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    break
finally:
    print "finally"
    camera.close()#release()
    cv2.destroyAllWindows()
    
