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
dbLog = mongoDB('radio_log','techlab') #work with the collection 'radio-logs' with the database 'techlab-db'
dbMemb = mongoDB('members','techlab')
dbSes = mongoDB('sessions','techlab')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
logger = logging.getLogger()

state = 0
id_session = int(read_last_id_session(dbSes))
logger.debug(id_session)

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
            elif readFromTelegram():    # Secondly, look at telegram
                logger.debug("read_telegram")
                msgIn = telegramPkt()
                state = 1

        ## PROCESS
        if state == 1:
            logger.debug(msgIn.__dict__)
            dbLog.write(msgIn.__dict__)   ## msg to mongo online database


            if msgIn.idm == 'n':      ## NFC from laser
                logger.debug("process_tag")
                msgOut = checkMember(msgIn, dbMemb)
                if msgOut > 0:
                    id_session = id_session + 1
                    openSession(msgIn, id_session, dbSes, dbMemb)
                    state = 2
                else:
                    state = 0

            elif msgIn.idm == 't':    ## Laser tick
                logger.debug("process_laser")
                msgOut = updateMember(msgIn, dbMemb, dbSes, id_session)
                state = 2

            elif msgIn.idm == 'e':    ## Energy tick
                logger.debug("process_energy")
                updateEnergy(msgIn)
                state = 0

            elif msgIn.idm == 'b':
                logger.debug("process_energy")
                if msgIn.cmd == '/door':  ## Door
                    logger.debug("APRO PORTA!")
                msgOut = telegramPrs(msgIn)
                state = 2

            elif msgIn.idm == 'd':
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
    dbMemb.close()
    dbSes.close()
    ser.close()
