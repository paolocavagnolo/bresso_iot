import sys
import time
import telepot
import pickle
import logging

SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
TELEGRAM_BRIDGE = SYSTEM_PATH + fkeylines[5].split('\n')[0]
TELEGRAM_KEY = fkeylines[11].split('\n')[0]
fkey.close()


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
logger = logging.getLogger()

print TELEGRAM_KEY

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    try:
        nome = msg['from']['first_name']
    except:
            nome = "utente che non hai inserito il suo nome in Telegram"

    print 'Got command: %s' % command
    logger.debug(chat_id)

    if command == '/door' and chat_id == -123571607:
        notizia = "ai tuoi ordini " + nome
        bot.sendMessage(chat_id, notizia)
        with open(TELEGRAM_BRIDGE, 'wb') as handle:
            pickle.dump(msg, handle)


bot = telepot.Bot(TELEGRAM_KEY)
bot.message_loop(handle)

while True:
    time.sleep(10)
