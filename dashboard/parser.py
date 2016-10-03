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
import plotly.tools as pyt

pyt.set_credentials_file(username='paoloc', api_key='ee28u45bns')

def readFromFile():
  arduFile = "energyBuffer.log"
  lines = []
  try:
      with open(arduFile, "r") as f:
          lines = f.readlines()
      lines = map(lambda x: x.rstrip(), lines)
      return lines
  except:
      return lines

lines = readFromFile()

xA = []
xB = []
xC = []

yA = []
yB = []
yC = []

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
        print "errore, id non presente tra 2 e 3"

traceY = Scatter(
    x=xA,
    y=yA,
    name='Raw'
)

# Calcolo Potenza Istantanea in Watt
yyA = []
yyB = []

for y in yA:
    yyA.append(3600000/float(y))
for y in yB:
    yyB.append(3600000/float(y))




# # Calcolo ritardo
# eA = []
# i = 1
#
# for x in xA[1:]:
#     d0 = datetime.strptime(xA[i-1], '%Y-%m-%d %H:%M:%S.%f')
#     d1 = datetime.strptime(xA[i], '%Y-%m-%d %H:%M:%S.%f')
#     eA.append((d1 - d0).total_seconds()*1000 - float(yA[i]))
#     i = i + 1
#
# traceE = Scatter(
#     x=xA,
#     y=eA,
#     name='errore'
# )

now = datetime.now()

yesterday = now - dateu.relativedelta(days=1)

p_this_week_s = now - dateu.relativedelta(days=now.weekday())
p_this_week_s = p_this_week_s.replace(hour=00,minute=00,second=00,microsecond=00)

last_week = now - dateu.relativedelta(days=7)

p_last_week_s = last_week.replace(last_week.year,last_week.month,last_week.day - last_week.weekday(),hour=00,minute=00,second=00,microsecond=00)
p_last_week_e = p_last_week_s + dateu.relativedelta(days=6)
p_last_week_e = p_last_week_e.replace(hour=23,minute=59,second=59,microsecond=9999)


last_year = now - dateu.relativedelta(year=1)

this_W = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_W = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
this_M = 0.0
last_M = 0.0
this_Y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_Y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

this_W2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_W2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
this_M2 = 0.0
last_M2 = 0.0
this_Y2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_Y2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

monday = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
monday2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

# Selezione delle x solamente dell'ultima settimana
# scorsa settimana

i = 0

for x in xA:

    try:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
    except:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if d0 >= p_this_week_s:
        # sono nei giorni di questa settimana
        this_W[d0.weekday()] = this_W[d0.weekday()] + 0.001

    if d0 >= p_last_week_s and d0 <= p_last_week_e:
        # sono nei giorni della scorsa settimana
        last_W[d0.weekday()] = last_W[d0.weekday()] + 0.001
        if d0.day == p_last_week_s.day:
            monday[d0.hour] = monday[d0.hour] + 0.001

    if d0.year == now.year:
        this_Y[d0.month-1] = this_Y[d0.month-1] + 0.001

    if d0.year == last_year.year:
        last_Y[d0.month-1] = last_Y[d0.month-1] + 0.001

    i = i + 1

i = 0
for x in xB:

    try:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
    except:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if d0 >= p_this_week_s:
        # sono nei giorni di questa settimana
        this_W2[d0.weekday()] = this_W2[d0.weekday()] + 0.001

    if d0 >= p_last_week_s and d0 <= p_last_week_e:
        # sono nei giorni della scorsa settimana
        last_W2[d0.weekday()] = last_W2[d0.weekday()] + 0.001
        if d0.day == p_last_week_s.day:
            monday2[d0.hour] = monday2[d0.hour] + 0.001

    if d0.year == now.year:
        this_Y2[d0.month-1] = this_Y2[d0.month-1] + 0.001

    if d0.year == last_year.year:
        last_Y2[d0.month-1] = last_Y2[d0.month-1] + 0.001



    i = i + 1

this_W_SUM = [this_W[i]+this_W2[i] for i in xrange(len(this_W))]
last_W_SUM = [last_W[i]+last_W2[i] for i in xrange(len(last_W))]
this_Y_SUM = [this_Y[i]+this_Y2[i] for i in xrange(len(this_Y))]
last_Y_SUM = [last_Y[i]+last_Y2[i] for i in xrange(len(last_Y))]
monday_SUM = [monday[i]+monday2[i] for i in xrange(len(monday))]

traceMONDAY = go.Bar(
    y = monday,
    name = "Illuminazione Piano Terra"
)

traceMONDAY2 = go.Bar(
    y = monday2,
    name = "Illuminazione Cucina"
)


traceLASTWEEK = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W,
    name = "Illuminazione Piano Terra"
)
traceLASTWEEK2 = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W2,
    name = "Illuminazione Cucina"
)

traceTHISWEEKSUM = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = this_W_SUM,
    name = "Settimana attuale"
)
traceLASTWEEKSUM = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W_SUM,
    name = "Settimana scorsa"
)

traceTHISYEARSUM = go.Bar(
    x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu',
       'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
    y=this_Y_SUM,
    name='Anno attuale'
)
traceLASTYEARSUM = go.Bar(
    x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu',
       'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
    y=last_Y_SUM,
    name='Anno scorso'
)

## Week vs. Last Week
data = Data([traceTHISWEEKSUM,traceLASTWEEKSUM])
layout = dict(title = 'Confronto consumi settimana attuale e settimana passata',
              xaxis = dict(title = 'giorni'),
              yaxis = dict(title = 'kWh'),
              barmode='group'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'week_last_week.html')

## Year vs. Last Year
data = Data([traceTHISYEARSUM,traceLASTYEARSUM])
layout = dict(title = 'Confronto consumi anno attuale e anno passato',
              xaxis = dict(title = 'mesi'),
              yaxis = dict(title = 'kWh'),
              barmode='group'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'year_last_year.html')

## Last week: General vs. Kitchen
data = Data([traceLASTWEEK,traceLASTWEEK2])
layout = dict(title = 'Consumo elettrico giornaliero, da Lunedi ' + p_last_week_s.strftime("%d/%m/%y") + ' a Venerdi ' + p_last_week_e.strftime("%d/%m/%y"),
              xaxis = dict(title = 'Mesi'),
              yaxis = dict(title = 'kWh'),
              barmode='stack'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'ground_vs_kitchen.html')

## Last Monday!
data = Data([traceMONDAY,traceMONDAY2])
layout = dict(title = 'Consumo elettrico durante lunedi ' + p_last_week_s.strftime("%d/%m/%y"),
              xaxis = dict(title = 'ore del giorno'),
              yaxis = dict(title = 'kWh'),
              barmode='stack'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'last_monday.html')
