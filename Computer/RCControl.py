# import the necessary packages
import serial, time
import serial.tools.list_ports

_portBaudRate = '9600'

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    #if 'Arduino' in p.description
    if 'CH340' in p.description
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

#_portName = "COM6"
_portName = arduino_ports[0]
sp = serial.Serial(_portName, _portBaudRate)

LeftSleep = 0.1
RightSleep = 0.1
ForwardSleep = 0.1

def setForwardSleep (t1):
    ForwardSleep = t1

def setRightSleep (t1):
    RightSleep = t1

def setLeftSleep (t1):
    LeftSleep = t1

def initRC():
    time.sleep(1)
    #Reset ports
    Stop()

def Forward_Right(CycleDuration, TurnTime):
    print ('Forward-Right: ' + str(TurnTime))
    Reverse(False)
    Left(False)
    Forward(True)    
    Right(True)   
    time.sleep(TurnTime/RightSleep)     
    Right(False)    
    time.sleep(CycleDuration - TurnTime)  
    Forward(False)
    
def Forward_Left(CycleDuration, TurnTime):
    print ('Forward-Left: ' + str(TurnTime))
    Right(False)
    Reverse(False)
    Forward(True)    
    Left(True)   
    time.sleep(TurnTime/LeftSleep)     
    Left(False)    
    time.sleep(CycleDuration - TurnTime)  
    Forward(False)
    
    
def Forward_Forward(CycleDuration):
    Reverse(False)
    Forward(True)
    print("Forward")
    time.sleep(CycleDuration)
    Stop()
    print("Stop")

# To move Forward send 1
# To stop forward motion send 0
# <param name="bState"></param>
def Forward (bState):
    if ( bState ):
        sp.write("1")
    else:
        sp.write("0")

# To move Reverse send 3
# To stop Reverse motion send 2
# <param name="bState"></param>
def Reverse (bState):
    if ( bState ):
        sp.write("3")
    else:
        sp.write("2")      

# To move Left send 5
# To stop Left motion send 4
# <param name="bState"></param>
def Left (bState):
    if ( bState ):
        sp.write("5")
    else:
        sp.write("4")    

# To move Right send 7
# To stop Right motion send 6
# <param name="bState"></param>
def Right (bState):
    if ( bState ):
        sp.write("7")
    else:
        sp.write("6") 

# To move Car Right send 5
# To stop Car Right motion send 4
# <param name="bState"></param>
def RightCar (bState):
    if ( bState ):
        sp.write("5")
    else:
        sp.write("4")    

# To move Car Left send 7
# To stop Car Left motion send 6
# <param name="bState"></param>
def LeftCar (bState):
    if ( bState ):
        sp.write("7")
    else:
        sp.write("6") 

# To Stop send 8
def Stop ():
    sp.write("8")