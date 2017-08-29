# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import serial, time
import pygame
from pygame.locals import *
import socket
import os
from RCControl import *

# Timeout for socket connection
waitForConn = 0.20

# Resolution width center
resWidthCenter = 300

# communication settings
TCP_IP = '192.168.8.101'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

cv2.namedWindow('Filters')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

def callbacked(s):
    return None

# Creating track bar
cv2.createTrackbar('hl', 'Filters', 0,179, callbacked)
cv2.createTrackbar('sl', 'Filters', 0,255, callbacked)
cv2.createTrackbar('vl', 'Filters', 0,255, callbacked)

cv2.setTrackbarPos('hl', 'Filters', 50)
cv2.setTrackbarPos('sl', 'Filters', 93)
cv2.setTrackbarPos('vl', 'Filters', 47)

cv2.createTrackbar('hh', 'Filters', 0,179, callbacked)
cv2.createTrackbar('sh', 'Filters', 0,255, callbacked)
cv2.createTrackbar('vh', 'Filters', 0,255, callbacked)

cv2.setTrackbarPos('hh', 'Filters', 94)
cv2.setTrackbarPos('sh', 'Filters', 247)
cv2.setTrackbarPos('vh', 'Filters', 243)


greenLower = (50, 93,47)
greenUpper = (94, 247, 243)
    
def Turn(cdCenter, frameCenter):
    if (cdCenter < frameCenter):
        Reverse(False)
        Forward(True)
        Left(False)
        Right(True)        
        print ('Right')
        time.sleep(0.1)
    elif (cdCenter   > frameCenter):
        Reverse(False)
        Forward(True)
        Right(False)
        Left(True)        
        print ('Left')
    else:
        Reverse(False)
        Forward(True)
        print("Forward")
        time.sleep(0.25)
        Stop()
        print("Stop")

#Initialize RC Controls
initRC() 

# Read Streaming Data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.settimeout(waitForConn)
s.listen(1)
   
#server_socket = socket.socket()
#server_socket.bind(('192.168.8.100', 8000)) #BentleyBackup
##server_socket.bind(('172.20.10.2', 8000)) # Mehreen
#server_socket.listen(0)

# accept a single connection
#connection = server_socket.accept()[0].makefile('rb')


while True:
    try:
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            Stop()
            break        
        if key == ord("s"):
            Stop()              
        if key == ord("f"):
            Reverse(False)
            Forward(True)
        if key == ord("b"):   #back         
            Forward(False)
            Reverse(True)
        if key == ord("l"):   #left
            Turn(100, resWidthCenter)
        if key == ord("r"):  #right 
            Turn(400, resWidthCenter)
        conn, addr = s.accept()
        #print 'Connection address:', addr
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        if(data):
            #print "received data:", data            
            Turn(int(data), resWidthCenter)

    except:
        print "Stoping! As no valid input recieved for " + str(waitForConn) + " seconds."
        Stop()
        continue


    conn.close()


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (29, 86, 6)
#greenUpper = (94, 255, 255)
#greenLower = (40, 45,75)
#greenUpper = (75, 240, 150)
#greenLower = (37, 38,70)
#greenUpper = (85, 255, 200)
#greenLower = (40, 45,75)
#greenUpper = (75, 240, 150)
#greenLower = (40, 45,110)
#greenUpper = (75, 240, 220)

pts = deque(maxlen=args["buffer"])

# Collect Images from stream

# collect images for training
print 'Start collecting images...'

# stream video frames one by one
try:
    stream_bytes = ' '
    frame = 1
    while True:  # TODO: Add check if we have data on socket
        stream_bytes += connection.read(1024)
        first = stream_bytes.find('\xff\xd8')
        last = stream_bytes.find('\xff\xd9')
        if first != -1 and last != -1:
            jpg = stream_bytes[first:last + 2]
            stream_bytes = stream_bytes[last + 2:]
            #image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
            frame = cv2.flip( frame, 0)
            #b, g, r = cv2.split(image)
            #for x in range(0, 640):
            #    for y in range(0, 479):
            #        image[x][y] = [0,b[x][y],0]
            #cv2.imshow('image', image)
            
            #cv2.imshow('roi_image', roi)
            #cv2.imshow('image', image)
            #frame = image

            hl = cv2.getTrackbarPos('hl','Filters')
            sl = cv2.getTrackbarPos('sl','Filters')
            vl = cv2.getTrackbarPos('vl','Filters')

            hh = cv2.getTrackbarPos('hh','Filters')
            sh = cv2.getTrackbarPos('sh','Filters')
            vh = cv2.getTrackbarPos('vh','Filters')

            greenLower = (hl, sl, vl)
            greenUpper = (hh, sh, vh)
            
            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600)
            if(False):
                picName = 'pic.bmp'
                cv2.imwrite(picName, image)

            xwidth, xheight, xchannel = frame.shape
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #cv2.imshow('image', hsv)
            #for x in range(0, 640):
            #    for y in range(0, 480):
            #        image[
            if(False):
                picName = 'pic.bmp'
                cv2.imwrite(picName, image)
         
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

            cv2.imshow("Frame", frame)
         
            # only proceed if at least one contour was found
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
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                else:
                    Stop()
                    continue
            else:
                Stop()
                continue

         
            # update the points queue
            
            pts.appendleft(center)
            
            # loop over the set of tracked points
            for i in xrange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    continue
         
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
                #cv2.putText(frame,str(pts[0][0]) + 'cd' + str(pts[0][1]),pts[0], cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
                #mrgba = frame.rgba
                cdWidth = pts[0][0]
                cv2.putText(frame,'o',(xheight/2, xwidth/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
                Turn(cdWidth, resWidthCenter)
         
            # show the frame to our screen
            
            key = cv2.waitKey(1) & 0xFF
         
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                Stop()
                break        
            if key == ord("s"):
                Stop()
                #greenLower = (int(raw_input("Enter greenLower[0].")), 45,75)
                #greenUpper = (int(raw_input("Enter greenUpper[0].")), 240, 220)
                #break                 
            if key == ord("f"):
                Reverse(False)
                Forward(True)
            if key == ord("l"):
                Right(False)
                Left(True)
                #break    
            if key == ord("r"):
                Left(False)
                Right(True)                          

finally:
    connection.close()
    server_socket.close()


cv2.destroyAllWindows()