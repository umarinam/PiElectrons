#!/usr/bin/env python

import socket
import time


TCP_IP = '192.168.8.102'
TCP_PORT = 5005
BUFFER_SIZE = 20
#MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((TCP_IP, TCP_PORT))
print "Socket Initialized"
    

def SendCommandToRemote(messageToSend):   
    
    s.send(":" + messageToSend)#remember: max message size is BUFFER_SIZE
    print "Sent message:", messageToSend

    
def closeSocket():
    s.close()
    print "Socket Closed"
    #print "received data:", data
    




