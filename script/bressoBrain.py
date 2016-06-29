from theBrain import *
import logging
import serial

# readFromSerial(RFmsg):

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=.5)

def readFromSerial():
    if ser.is_open:
        pl = ser.readline().rstrip()
        if len(pl) > 2 and pl[0] == '<' and pl[1] == ',':
                RFmsg = pl
                return (True, RFmsg)
        else:
            return (False, "")
    else:
        ser.open()
        readFromSerial(RFmsg)


# goReal(msgOut)

def goReal(msgOut):

    ser.write('i'+str(msgOut.idr)+'\0')
    ser.flush()
    time.sleep(1)

    ser.write('j'+str(msgOut.payload_out)+'\0')
    ser.flush()


# Check internet connection!
dbLog = mongoDB('radio_log','bresso') #work with the collection 'radio-logs' with the database 'techlab-db'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
logger = logging.getLogger()

state = 0

try:
    while True:
        # logger.debug("eccolo")
        ## INPUT - state 0 >> 1##
        if state == 0:
            RFmsg = ""
            newSerial = False
            newSerial, RFmsg = readFromSerial()
            if newSerial:   # First of all, look at the serial port for communication from moteino
                logger.debug("read_serial")
                logger.debug(RFmsg)
                msgIn = radioPkt(RFmsg)
                state = 1

        ## PROCESS
        if state == 1:
            logger.debug(msgIn.__dict__)
            dbLog.write(msgIn.__dict__)   ## msg to mongo online database

            if msgIn.idm == 'e':    ## Energy tick
                logger.debug("process_energy")
                updateEnergy(msgIn)
                state = 0

            else:
                logger.debug("lettera protocollare mancante!")
                logger.debug(msgIn.idm)
                state = 0


        ## OUTPUT
        if state == 2:
            logger.debug("Output")
            logger.debug(msgOut)
            #dbLog.write(msgOut.__dict__)   ## msg to mongo online database
            goReal(msgOut)
            state = 0

except Exception, e:
    logging.error(e, exc_info=True)
    logger.info("Game Over!", exc_info=True)
    dbLog.close()
    ser.close()
