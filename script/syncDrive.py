from theBrain import *
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
logger = logging.getLogger()


gUser = gDriveAPI('soci','tag_system')
gSes = gDriveAPI('open_session','tag_system')

dbMemb = mongoDB('members','techlab')

titoli =['id','tagNFC','Credits','Skills','Data richiesta','Data accettazione ','Tutore','Mail','Nome','Cognome','Data nascita','Luogo nascita','Residenza','CF','Qualifica','Quota 2015','Quota 2016','Data annullamento']



# first_setup(gUser, dbMemb)

def updateRow(row, gUser, dbMemb):
    logger.debug("line")
    userId = row
    logger.debug(userId)
    # update a Credit in User
    datiDrive = gUser.read_row(userId+3)
    logger.debug(datiDrive)
    # update mongoDB
    toFind = {}
    toFind['id'] = str(userId)
    count,doc = dbMemb.read(toFind)
    if count < 1:
        print "non ho trovatto nessuno"
    logger.debug(doc)
    i = 0
    for col in datiDrive:
        toChange = {}
        toChange[titoli[i]] = col
        i = i + 1
        logger.debug(str(toFind) + " " + str(toChange))
        dbMemb.update(toFind,toChange)

while True:
    time.sleep(10)

    if os.path.isfile(SYNC_TRIG):
        # start!
        # leggi tutte le linee dal file
        ftrig=open(SYNC_TRIG,'r+')
        ftrigLines=ftrig.readlines()
        # elimina il file
        RM_FILE_COMMAND = "sudo rm " + SYNC_TRIG
        os.system(RM_FILE_COMMAND)
        ftrig.close()
        logger.debug("ok file")

        for line in ftrigLines:
            command = line.split(',')[0]

            # 'u' means: Found the TAG in mongoDB, so just UPDATE the mongoDB with gDrive Data
            if command == 'u':
                row_id = int(line.split('\n')[0].split(',')[1])
                updateRow(row_id, gUser, dbMemb)

            # 'n' means: Not found anything in mongoDB, so it's a NEW tag. But: it is a new tag of an existing member or a new member?
            if command == 'n':
                tag = line.split('\n')[0].split(',')[1]
                colonna_tag = gUser.read_col(2)
                try:
                    # Trovi qualcosa su drive? se si segnati il numero della riga in cui trovi qualcosa
                    row = colonna_tag.index(tag) - 2

                except:
                    # Se non trovi nulla amen. Significa che e' stato appena passato, e qualcuno lo sta scrivendo su drive
                    logger.debug("Nuovo Tag!")

                else:
                    # Se invece hai trovato qualcosa, allora guarda l'id, e confrontalo con il massimo id che hai in mongo
                    lastid = int(dbMemb.read_last_N(1)[0]['id'])

                    if row > lastid:
                        # Nuovo membro al techlab,  aggiungi un posto a tavola!
                        nuovo = {'Luogo nascita': '', 'Residenza': '', 'Data accettazione ': '', 'Credits': '', 'Skills': '', 'Cognome': '', 'Nome': '', 'Qualifica': '', 'CF': '', 'Quota 2016': '', 'tagNFC': '',
                        'Data nascita': '', 'Data richiesta': '', 'Mail': '', 'Data annullamento': '', 'id': '', 'Quota 2015': '', 'Tutore': ''}

                        nuovo['id'] = str(lastid + 1)
                        nuovo['tagNFC'] = tag
                        dbMemb.write(nuovo)

                    else:
                        # Membro gia' esistente aggiorna solamente i parametri di mongo con quelli appena scritti sul drive
                        updateRow(row, gUser, dbMemb)


            # UPDATE DRIVE AFTER TICK
            if command == 't':
                toFind = {}
                toFind['tagNFC'] = line.split('\n')[0].split(',')[1]
                count, doc = dbMemb.read(toFind)
                gUser.write(int(doc[0]['id'])+3, 3, str(doc[0]['Credits']))
