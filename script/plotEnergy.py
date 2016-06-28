import fileinput
import time
import logging
import sys
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
logger = logging.getLogger()

SYSTEM_PATH = '/home/pi/Documents/'
# SYSTEM_PATH = '/Users/paolo/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
GDRIVE_API_KEY = SYSTEM_PATH + fkeylines[1].split('\n')[0]
MONGODB_CLIENT_MLAB = fkeylines[3].split('\n')[0]
TELEGRAM_BRIDGE = SYSTEM_PATH + fkeylines[5].split('\n')[0]
ENERGYLOG = SYSTEM_PATH + fkeylines[7].split('\n')[0]
LOGCONFIG = SYSTEM_PATH + fkeylines[9].split('\n')[0]
SYNC_TRIG = SYSTEM_PATH + fkeylines[13].split('\n')[0]
PANEL_HTML = SYSTEM_PATH + fkeylines[15].split('\n')[0]
fkey.close()

def data2web( data, a, b, c ):

    processing_foo1s = False
    last_row = "<tr><td>Data</td><td>A</td><td>B</td><td>C</td></tr>"
    full = "<tr><td>" + data + "</td><td>" + str(a) + "</td><td>" + str(b) + "</td><td>" + str(c) + "</td></tr>"

    for line in fileinput.input(PANEL_HTML, inplace=1):
      if line.startswith(last_row):
        processing_foo1s = True
      else:
        if processing_foo1s:
          print full
        processing_foo1s = False
      print line,

def readFromFile():
  buffer_file = ENERGYLOG
  lines = []
  with open(buffer_file, "r") as f:
      lines = f.readlines()
  # with open(buffer_file, "w") as f:
  #     f.truncate()
  f.close()
  lines = map(lambda x: x.rstrip(), lines)
  return lines


while True:
    if os.path.isfile(ENERGYLOG):
        logger.debug("trovato file energia")
        lines = readFromFile()
        RM_FILE_COMMAND = "sudo rm " + ENERGYLOG
        os.system(RM_FILE_COMMAND)
        i=0
        for line in lines:
            data = lines[i].split(',')[0]
            idphase = lines[i].split(',')[1]
            count = lines[i].split(',')[2]
            if idphase == 'a':
                data2web(data,count,' ',' ')
            elif idphase == 'b':
                data2web(data,' ',count,' ')
            elif idphase == 'c':
                data2web(data,' ',' ',count)
            i=i+1

        logger.debug('Copy file to the apache server index.html')
        copy_string = 'sudo cp ' + PANEL_HTML + ' /var/www/html/'
        os.system(copy_string)
        os.system('sudo rm /var/www/html/index.html')
        os.system('sudo mv /var/www/html/panel.html /var/www/html/index.html')

        logger.debug('Starting from a new file')
        new_file = 'sudo rm ' + PANEL_HTML
        os.system(new_file)
        copy_file = 'sudo cp ' + SYSTEM_PATH + 'techlab_iot/script/html/panel_init.html ' + PANEL_HTML
        os.system(copy_file)
