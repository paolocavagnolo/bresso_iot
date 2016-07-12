import sys
import time
import os


from datetime import datetime
import dateutil.relativedelta as dateu
import plotly
from plotly.graph_objs import *
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF


SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
ENERGY_FILE = SYSTEM_PATH + fkeylines[7].split('\n')[0]
fkey.close()

ERR_THS = 8

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


    # traceA = Scatter(
    #     x=xA,
    #     y=dxA,
    #     name='Condizionatore'
    # )
    # traceB = Scatter(
    #     x=xB,
    #     y=dxB,
    #     name='Prese Elettriche'
    # )
    # traceC = Scatter(
    #     x=xC,
    #     y=dxC,
    #     name='Illuminazione'
    # )


    # data = Data([traceA,traceB,traceC])


    # Edit the layout
    # layout = dict(title = 'Consumo Elettrico nel TechLab',
    #               xaxis = dict(title = 'Tempo'),
    #               yaxis = dict(title = 'Potenza espressa in Watt'),
    #               margin = dict(t=75, l=50),
    #               height = 800
    #               )

    # fig = dict(data=data, layout=layout)

########################

    # Add table data
    now = datetime.now()

    pday = now - dateu.relativedelta(days=1)

    pweek = now - dateu.relativedelta(days=7)
    pweek_s = pweek.replace(pweek.year,pweek.month,pweek.day-pweek.weekday())
    pweek_e = pweek_s.replace(pweek_s.year,pweek_s.month,pweek_s.day+6)

    pmonth = now - dateu.relativedelta(months=1)

    en_pday_a = 0
    en_pday_b = 0
    en_pday_c = 0

    control_pday = []

    en_pweek_a = 0
    en_pweek_b = 0
    en_pweek_c = 0
    control_pweek = []

    en_pmonth_a = 0
    en_pmonth_b = 0
    en_pmonth_c = 0
    control_pmonth = []

    i = 0
    for x in xA:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        #ieri
        if d0.year == pday.year and d0.month == pday.month and d0.day == pday.day:
            en_pday_a = en_pday_a + 1
            # control_pday.append[yA[i]]

        #scorsa settimana
        if d0.year >= pweek_s.year and d0.year <= pweek_e.year and d0.month >= pweek_s.month and d0.month <= pweek_e.month and d0.day >= pweek_s.day and d0.day <= pweek_e.day:
            en_pweek_a = en_pweek_a + 1
            # control_pweek.append[yA[i]]

        #scorso mese
        if d0.year == pmonth.year and d0.month == pmonth.month:
            en_pmonth_c = en_pmonth_c + 1
            # control_pmonth.append[yA[i]]

        i = i + 1

    consumo_ieri_A = float(en_pday_a)/100
    consumo_settimana_A = float(en_pweek_a)/100
    consumo_mese_scorso_A = float(en_pmonth_c)/100

    i = 0
    for x in xB:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        #ieri
        if d0.year == pday.year and d0.month == pday.month and d0.day == pday.day:
            en_pday_b = en_pday_b + 1
            # control_pday.append[yB[i]]

        #scorsa settimana
        if d0.year >= pweek_s.year and d0.year <= pweek_e.year and d0.month >= pweek_s.month and d0.month <= pweek_e.month and d0.day >= pweek_s.day and d0.day <= pweek_e.day:
            en_pweek_b = en_pweek_b + 1
            # control_pweek.append[yB[i]]

        #scorso mese
        if d0.year == pmonth.year and d0.month == pmonth.month:
            en_pmonth_b = en_pmonth_b + 1
            # control_pmonth.append[yB[i]]

        i = i + 1

    consumo_ieri_B = float(en_pday_b)/100
    consumo_settimana_B = float(en_pweek_b)/100
    consumo_mese_scorso_B = float(en_pmonth_b)/100

    i = 0
    for x in xC:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        #ieri
        if d0.year == pday.year and d0.month == pday.month and d0.day == pday.day:
            en_pday_c = en_pday_c + 1
            # control_pday.append[yA[i]]

        #scorsa settimana
        if d0.year >= pweek_s.year and d0.year <= pweek_e.year and d0.month >= pweek_s.month and d0.month <= pweek_e.month and d0.day >= pweek_s.day and d0.day <= pweek_e.day:
            en_pweek_c = en_pweek_c + 1
            # control_pweek.append[yA[i]]

        #scorso mese
        if d0.year == pmonth.year and d0.month == pmonth.month:
            en_pmonth_c = en_pmonth_c + 1
            # control_pmonth.append[yA[i]]

        i = i + 1


    consumo_ieri_C = float(en_pday_c)/100
    consumo_settimana_C = float(en_pweek_c)/100
    consumo_mese_scorso_C = float(en_pmonth_c)/100

    table_data = [['Consumi [kWh]', 'Ieri', 'Settimana scorsa', 'Mese scorso'],
                  #['Condizionatore', consumo_ieri_A, consumo_settimana_A, consumo_mese_scorso_A],
                  #['Prese Elettriche', consumo_ieri_B, consumo_settimana_B, consumo_mese_scorso_B],
                  ['Illuminazione', consumo_ieri_A, consumo_settimana_A, consumo_mese_scorso_A]]

    # Initialize a figure with FF.create_table(table_data)
    figure = FF.create_table(table_data, height_constant=60)

    # Make traces for graph
    trace1 = go.Scatter(x=xA, y=dxA, xaxis='x2', yaxis='y2',
                    name='Illuminazione')
    trace2 = go.Scatter(x=xB, y=dxB, xaxis='x2', yaxis='y2',
                    name='Prese Elettriche')
    trace3 = go.Scatter(x=xC, y=dxC, xaxis='x2', yaxis='y2',
                    name='Illuminazione')

    # Add trace data to figure
    figure['data'].extend(go.Data([trace1, trace2, trace3]))

    # Edit layout for subplots
    figure.layout.yaxis.update({'domain': [0, .15]})
    figure.layout.yaxis2.update({'domain': [.24, 1]})
    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    figure.layout.yaxis2.update({'anchor': 'x2'})
    figure.layout.xaxis2.update({'anchor': 'y2'})
    figure.layout.yaxis2.update({'title': 'Potenza espressa in Watt'})
    # Update the margins to add a title and see graph x-labels.
    figure.layout.margin.update({'t':75, 'l':50})
    figure.layout.update({'title': 'Consumo elettrico linea illuminazione scuola Bresso'})
    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    figure.layout.update({'height':760})

####################

    plotly.offline.plot(figure, filename = 'energy.html')
    commandString = "sudo cp energy.html /var/www/html/"
    os.system(commandString)
    commandString = "sudo rm /var/www/html/index.html"
    os.system(commandString)
    commandString = "sudo mv /var/www/html/energy.html /var/www/html/index.html"
    os.system(commandString)

    time.sleep(60)
