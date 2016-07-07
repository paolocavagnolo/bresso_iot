import sys
import time
import os

from datetime import datetime

import plotly
from plotly.graph_objs import *

SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
ENERGY_FILE = SYSTEM_PATH + fkeylines[7].split('\n')[0]
fkey.close()

ERR_THS = 3

def readFromFile():
  arduFile = ENERGY_FILE
  lines = []
  with open(arduFile, "r") as f:
      lines = f.readlines()
  lines = map(lambda x: x.rstrip(), lines)
  return lines

while True:

    lines = readFromFile()

    xA = []
    xB = []
    xC = []

    yA = []
    yB = []
    yC = []


    for line in lines:
        fase_tmp = line.split(',')[1]
        if fase_tmp == 'a':
            xA.append(line.split(',')[0])
            yA.append(line.split(',')[2])
        elif fase_tmp == 'b':
            xB.append(line.split(',')[0])
            yB.append(line.split(',')[2])
        elif fase_tmp == 'c':
            xC.append(line.split(',')[0])
            yC.append(line.split(',')[2])
        else:
            print "errore, lettera non presente tra a,b e c"

    print "inizio fase 2"
    print "a"

    dxA = []
    i = 1
    for x in xA[1:]:
        if i==1:
            d0 = datetime.strptime(xA[i-1], '%Y-%m-%d %H:%M:%S.%f')
        else:
            d0 = d1
        d1 = datetime.strptime(xA[i], '%Y-%m-%d %H:%M:%S.%f')
        delta = d1 - d0
        delta_c = float(delta.seconds) + float(delta.microseconds)/1000000
        dxA.append( 3600/(delta_c*1000)*10000 )
        if delta_c < ERR_THS:
            dxA.pop()
            xA.pop(i)
        else:
            i=i+1

    dxB = []
    i = 1
    for x in xB[1:]:
        if i==1:
            d0 = datetime.strptime(xB[i-1], '%Y-%m-%d %H:%M:%S.%f')
        else:
            d0 = d1
        d1 = datetime.strptime(xB[i], '%Y-%m-%d %H:%M:%S.%f')
        delta = d1 - d0
        delta_c = float(delta.seconds) + float(delta.microseconds)/1000000
        dxB.append( 3600/(delta_c*1000)*10000 )
        if delta_c < ERR_THS:
            dxB.pop()
            xB.pop(i)
        else:
            i=i+1

    print "c"

    dxC = []
    i = 1
    for x in xC[1:]:
        if i==1:
            d0 = datetime.strptime(xC[i-1], '%Y-%m-%d %H:%M:%S.%f')
        else:
            d0 = d1
        d1 = datetime.strptime(xC[i], '%Y-%m-%d %H:%M:%S.%f')
        delta = d1 - d0
        delta_c = float(delta.seconds) + float(delta.microseconds)/1000000
        dxC.append( 3600/(delta_c*1000)*10000 )
        if delta_c < ERR_THS:
            dxC.pop()
            xC.pop(i)
        else:
            i=i+1


    traceA = Scatter(
        x=xA,
        y=dxA,
        name = 'Illuminazione Piano Terra'
    )

    traceB = Scatter(
        x=xB,
        y=dxB,
    )

    traceC = Scatter(
        x=xC,
        y=dxC,
    )


    data = Data([traceA,traceB,traceC])

    # Edit the layout
    layout = dict(title = 'Consumo Elettrico nella Scuola di Bresso',
                  xaxis = dict(title = 'Tempo'),
                  yaxis = dict(title = 'Potenza espressa in Watt'),
                  )

    fig = dict(data=data, layout=layout)

    plotly.offline.plot(fig, filename = 'energy.html')

    commandString = "sudo cp energy.html /var/www/html/"
    os.system(commandString)
    commandString = "sudo rm /var/www/html/index.html"
    os.system(commandString)
    commandString = "sudo mv /var/www/html/energy.html /var/www/html/index.html"
    os.system(commandString)

    time.sleep(60)
