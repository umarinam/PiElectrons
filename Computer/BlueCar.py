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
import datetime

# Timeout for socket connection
waitForConn = .25

# Resolution width center
resWidthCenter = 300

# communication settings
TCP_IP = '192.168.8.102'
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

cv2.createTrackbar('ld', 'Filters', 1, 100, callbacked)
cv2.createTrackbar('rd', 'Filters', 1, 100, callbacked)
cv2.createTrackbar('fd', 'Filters', 1, 100, callbacked)

cv2.setTrackbarPos('ld', 'Filters', 100)
cv2.setTrackbarPos('rd', 'Filters', 100)
cv2.setTrackbarPos('fd', 'Filters', 100)

cv2.resizeWindow('Filters', 600, 100)

greenLower = (50, 93,47)
greenUpper = (94, 247, 243)


    
def Turn(cdCenter, frameCenter):
    TurnPercent = 100 * abs(cdCenter - frameCenter) / frameCenter
    #CycleDuration = 0.1   #0.5
    #TurnTime = CycleDuration * TurnPercent / 100
    if (cdCenter  + 50 < frameCenter):
        CycleDuration = 0.2   #0.5
        TurnTime = CycleDuration * TurnPercent / 100
        Forward_Right(CycleDuration, TurnTime)
    elif (cdCenter - 50   > frameCenter):
        CycleDuration = 0.1   #0.5
        TurnTime = CycleDuration * TurnPercent / 100
        Forward_Left(CycleDuration, TurnTime)
    else:
        CycleDuration = 0.5   #0.5
        TurnTime = CycleDuration * TurnPercent / 100
        Forward_Forward(CycleDuration)

#Initialize RC Controls
initRC() 


#x=0.5
#print datetime.datetime.now() 
#Forward_Forward(x)
#Forward_Right(x,x)
#Forward_Forward(x)
#Forward_Left(x/2,x/2)
#Stop()
#print datetime.datetime.now() 
#x = 2

# Read Streaming Data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
#s.settimeout(waitForConn)
s.listen(1)
conn, addr = s.accept()
   
#server_socket = socket.socket()
#server_socket.bind(('192.168.8.100', 8000)) #BentleyBackup
##server_socket.bind(('172.20.10.2', 8000)) # Mehreen
#server_socket.listen(0)

# accept a single connection
#connection = server_socket.accept()[0].makefile('rb')

print "Listening!"
while True:
    #try:
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q") or key == ord("e") or key == 27 : #escape
        Stop()
        break        
    if key == ord("s") or key == 32: # Stop on s and space
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

    ld = cv2.getTrackbarPos('ld','Filters')
    rd = cv2.getTrackbarPos('rd','Filters')
    fd = cv2.getTrackbarPos('fd','Filters')
    #setLeftSleep(ld/10)
    #setRightSleep(rd/10)
    #setForwardSleep(fd/10)
    #conn, addr = s.accept()
    #print 'Connection address:', addr

    data = conn.recv(BUFFER_SIZE)
    if not data: break
    if(data):
        print "RaspberryPi says:", data
        rdata = data.rsplit(":",1)
        #print "Spliting:", rdata
        if(len(rdata) > 1):
            try:
                offset = int(rdata[1].replace(":",""))
                Turn(offset, 300)
                print "Last Point:", rdata[1]            
            except:
                print "Unable to split:", data  
                continue         
        #Turn(int(data), resWidthCenter)

    #except:
    #    #print "Stoping! As no valid input recieved for " + str(waitForConn) + " seconds."
    #    Stop()
    #    continue

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
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
            frame = cv2.flip( frame, 0)


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

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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