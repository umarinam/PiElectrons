import RPi.GPIO as gpio
import time




def SendCommandToRemote(centroidPoint):
    img_center=300.0
    t=0.1
    x = 1.0
    print centroidPoint
    if (float(centroidPoint) + 50.0 < img_center):
        print "right"
        #x = (img_center - float(centroidPoint)) / 32
        right(x * t)
    elif float(centroidPoint) - 50 > img_center:
        print "left"
        #x = (float(centroidPoint) - img_center) / 32
        left(x * t)
    else:
        print "forward"
        forward(5*t)

def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(4, gpio.OUT)
 gpio.setup(17, gpio.OUT)
 gpio.setup(27, gpio.OUT)
 gpio.setup(22, gpio.OUT)

def reverse(tf):
 init()
 gpio.output(4, True)
 gpio.output(17, False)
 gpio.output(27, True) 
 gpio.output(22, False)
 time.sleep(tf)
 gpio.cleanup()

def forward(tf):
 #init()
 gpio.output(4, False)
 gpio.output(17, True)
 gpio.output(27, False) 
 gpio.output(22, True)
 #time.sleep(tf)
 #gpio.cleanup()

def stop(interCount):
    gpio.cleanup()

def right(tf):
 init()
 gpio.output(4, True)#turn other wheel backward
 gpio.output(17, False)
 gpio.output(27, False) 
 gpio.output(22, True)#turn left wheels forward
 time.sleep(tf)
 gpio.cleanup()


def left(tf):
 init()
 gpio.output(4, False)
 gpio.output(17, True)#turn right wheels forward
 gpio.output(27, True) #turn other wheel backward
 gpio.output(22, False)
 time.sleep(tf)
 gpio.cleanup()    


def forwardleft(tf):
 init()
 gpio.output(4, False)
 gpio.output(17, True)
 gpio.output(27, False) 
 gpio.output(22, False)
 time.sleep(tf)
 gpio.cleanup()

def reverseleft(tf):
 init()
 gpio.output(4, True)
 gpio.output(17, False)
 gpio.output(27, False) 
 gpio.output(22, False)
 time.sleep(tf)
 gpio.cleanup()


init()
left(0.4)
#forward(0.2)
#left(0.2)

#init()
gpio.cleanup()
#for i in range (1,10):
#print "test"
#forward(2)
#time.sleep(1)
#left(4)
#time.sleep(1)
#right(4)
#time.sleep(1)
#reverse(2)

#reverseright(2)
#forwardleft(2)
#reverseleft(2)
#reverse(2)
#print "forward"
#forward(4)
#print "backward"
#reverse(2)
