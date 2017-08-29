# import the necessary packages
import serial, time

_portBaudRate = '9600'
_portName = "COM6"

sp = serial.Serial(_portName, _portBaudRate)


def initRC():
    time.sleep(1)
    #Reset ports
    Stop()

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