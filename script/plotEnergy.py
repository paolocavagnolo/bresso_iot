import sys
import time
import os
from datetime import datetime
import dateutil.relativedelta as dateu

SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
ENERGY_FILE = SYSTEM_PATH + fkeylines[7].split('\n')[0]
fkey.close()

def readFromFile():
  arduFile = ENERGY_FILE
  lines = []
  try:
      with open(arduFile, "r") as f:
          lines = f.readlines()
      lines = map(lambda x: x.rstrip(), lines)
      return lines
  except:
      return lines

while True:

    lines = readFromFile()

    xA = []
    xB = []

    yA = []
    yB = []

    for line in lines:
        try:
            fase_tmp = line.split(',')[1]
        except:
            fase_tmp = '4'

        if fase_tmp == '2':
            xA.append(line.split(',')[0])
            yA.append(line.split(',')[2])
        elif fase_tmp == '3':
            xB.append(line.split(',')[0])
            yB.append(line.split(',')[2])
        else:
            print "errore, id non presente - solo 2 e 3"

    yyA = []
    yyB = []

    for y in yA:
        yyA.append(3600000/float(y))
    for y in yB:
        yyB.append(3600000/float(y))

    totA = 0
    for v in yyA[-10:]:
        totA = totA + v
    totA = totA / 10

    totB = 0
    for v in yyB[-10:]:
        totB = totB + v
    totB = totB / 10

    commandString = "sudo rm ~/Documents/bresso_iot/display/main.html"
    os.system(commandString)
    commandString = "sudo cp ~/Documents/bresso_iot/display/original.html ~/Documents/bresso_iot/display/main.html"
    os.system(commandString)
    

    commandString = "~/refresh.sh"
    os.system(commandString)
    time.sleep(60)

########################


####################

    # commandString = "sudo cp energy.html /var/www/html/"
    # os.system(commandString)
    # commandString = "sudo rm /var/www/html/index.html"
    # os.system(commandString)
    # commandString = "sudo mv /var/www/html/energy.html /var/www/html/index.html"
    # os.system(commandString)
    #
    #



#cosa deve fare il mio programma

# 1 leggere gli ultimi 10 valori di Potenza Istantanea
# 2 fare la media
# 3 sostituire l'html con il valore
