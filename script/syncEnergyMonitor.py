from theBrain import *
import serial

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=.5)

def goReal(msgOut):

    ser.write('i'+str(msgOut.idr)+'\0')
    ser.flush()
    time.sleep(1)

    ser.write('j'+str(msgOut.payload_out)+'\0')
    ser.flush()
