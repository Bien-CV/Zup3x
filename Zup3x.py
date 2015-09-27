#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    Zup3x Client
    Description: Hop3x Assistant Bot
    Author(s): TAHRI Ahmed
    Version: Delta (0.2.3)
    Notice: 
    
        This stand only for educational purposes, 
        we won't be held responsible for any damage or accident 
        you made with this tool.
    
    dep. pip install pyautogui, httplib2
'''

import subprocess 
import os
import glob
import pyautogui
import httplib2 
import json 
import time
import sys
#import xerox
import xml.etree.cElementTree as ET
import math
from datetime import datetime
import random
import logging
from logging.handlers import RotatingFileHandler
import difflib
import shutil
import zipfile
import signal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

__author__ = "Ousret"
__date__ = "$19 sept. 2015 11:15:33$"

__VERSION__ = '0.2.2' #Local Zup3x revision
ZUP3X_ROOT_PATH = 'java -Xmx512m -jar hop3xEtudiant/lib/Hop3xEtudiant.jar'

SCREEN_X, SCREEN_Y = pyautogui.size()
BUTTON_TAB_SCROLL_MAX = 19

PROJECT_TYPE = 'C'
SESSIONS = []
PROJECT_FILELIST = []

ENABLE_GIT = False
ENABLE_LOCAL = True

LOCAL_PROJECTS = []

#Logs params, don't change anything unless you known what you'r doing!
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('logs/Zup3x-'+time.strftime('%Y-%m-%d-%H-%M-%S')+'.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

allowFailure = 6

notifyStats = {'projectCreated':0, 'fileCreated':0, 'fileModified':0, 'fileDeleted':0, 'error':0, 'warning': 0, 'session':'Unknown', 'worktime': 0, 'nextIteration':0 }

if (sys.platform == 'darwin'):
    CTRL_SWAP = 'command'
    STARS_SWAP = '*'
else:
    CTRL_SWAP = 'ctrl'
    STARS_SWAP = 'multiply'

def signalHandle(signal, frame):
    logger.critical('Zup3x stopped with signal '+signal)

    if (sys.platform == 'win32'):
        logger.warning('Zup3x is trying to restore keyboard layout after incident.')
        win32api.LoadKeyboardLayout(originLayout, 1)

    raise Exception('Zup3x can\'t breathe anymore, try to reanimate it!')

if (sys.platform == 'win32'):
    signal.signal(signal.SIGBREAK, signalHandle)
else:
    signal.signal(signal.SIGTERM, signalHandle)

#GMail Notification zup3xbot@gmail.com
class Notify:
    
    def __init__(self, usr, password):
        self.username = usr
        self.password = password
        
    def send(self, title, message):

        AVAILABLE_LOGS = sorted(glob.glob("logs/" + "*.log"), key=os.path.getctime)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(self.username, self.password)
        except:
            logger.error('You need to activate low security level application on GMail for Zup3x!')
            return
        fromaddr = self.username + "@gmail.com"
        toaddr = self.username + "@gmail.com"
        sub = title
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = sub  
        msg.attach(MIMEText(message, 'plain'))
        if (len(AVAILABLE_LOGS) > 0):
            try:
                with open(AVAILABLE_LOGS[-1], "rb") as fic:
                    msgLog = MIMEApplication(fic.read(), 'log')
                    msgLog.add_header('Content-Disposition', 'attachment', filename=os.path.basename(AVAILABLE_LOGS[-1]))
                    msg.attach(msgLog)
            except:
                logger.error('Unable to attach <'+afile+'> for GMail notification')

        server.sendmail(fromaddr,toaddr,msg.as_string())
        server.quit()

def getHop3xRepo(Username, Password):
    API_BB = httplib2.Http(".cache")
    API_BB.add_credentials(Username, Password) # Basic authentication
    resp, content = API_BB.request("https://api.bitbucket.org/1.0/user/repositories", "GET")
    repoList = json.loads(content.decode("utf-8"))
    return repoList

def extractZip(filename, dest):
    logger.info('Extracting '+filename+' ..')
    
    try:
        with zipfile.ZipFile(filename, "r") as z:
            z.extractall(dest)
    except:
        logger.critical('Unable to extract '+filename+' !')
        return False
    return True

def getHop3x():
    logger.info('Downloading lastest Hop3x version from hop3x.univ-lemans.fr [...]')
    DOWNLOAD_HOP3X = httplib2.Http(".cache")
    resp, content = DOWNLOAD_HOP3X.request("http://hop3x.univ-lemans.fr/Hop3xEtudiant.zip", "GET")

    try:
        logger.info('Saving binaries to ./Hop3xEtudiant.zip')
        with open('Hop3xEtudiant.zip', 'wb') as f:
            f.write(content)

    except:
        logger.critical('Unable to create Hop3xEdudiant.zip')
        return False

    return extractZip('Hop3xEtudiant.zip', '')

def mergeFiles(filename1, filename2):
    
    try:
        f1 = open(filename1, 'r')
        f2 = open(filename2, 'r')
    except IOError as e:
        logger.critical('mergeFiles has failed with '+filename1+' and '+filename2+' with '+e.strerror)
        return None
    
    liste = list(difflib.ndiff(f1.readlines(),f2.readlines()))
    diff = list() # Contiendra les différences et les lignes

    for i,j in zip(range(liste.__len__()),liste):
        if j[0]=='-' or j[0]=='+':
            diff.append({i:j})

    return diff

def manualHotKey(primaryKey, secondaryKey, darwinSpecial = False):
    if (darwinSpecial == True):
        pyautogui.keyDown('ctrl')
    pyautogui.keyDown(primaryKey)
    pyautogui.keyDown(secondaryKey)

    if (darwinSpecial == True):
        pyautogui.keyUp('ctrl')
    pyautogui.keyUp(primaryKey)
    pyautogui.keyUp(secondaryKey)

def closeContextMenu():
    pyautogui.press('esc')
    
def openContextMenuFile():
    if (sys.platform == 'darwin'):
        manualHotKey('alt', 'f', True)
    else:
        manualHotKey('alt', 'f')
def openContextMenuEdition():
    if (sys.platform == 'darwin'):
        manualHotKey('alt', 'e', True)
    else:
        manualHotKey('alt', 'e')
    
def openContextMenuTools():

    if (sys.platform == 'darwin'):
        manualHotKey('alt', 't', True)
    else:
        manualHotKey('alt', 't')

def openContextMenuAssist():
    if (sys.platform == 'darwin'):
        manualHotKey('alt', 'a', True)
    else:
        manualHotKey('alt', 'a')
    
def saveCurrentFile():
    manualHotKey(CTRL_SWAP, 's')

def compileCurrentWork():
    openContextMenuTools()
    time.sleep(1)
    pyautogui.press('enter')

def executeCurrentWork():
    openContextMenuTools()
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')

def deleteCurrentFile():
    openContextMenuFile()
    time.sleep(1)
    for i in range(3):
        pyautogui.press('down')
        time.sleep(0.5)

    pyautogui.press('enter')

def hitTabRange(NB_TIME):
    for i in range(NB_TIME):
        pyautogui.press('tab')
        time.sleep(0.2)

def createNewProject(PROJECT_NAME, TYPE):
    openContextMenuFile()
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite(PROJECT_NAME, interval=0.2)
    
    #Next, select project type
    #Java, Ruby, C, C+Make, Nxc, SpiC, Python
    hitTabRange(1)
    
    if (TYPE == 'Java'):
        pyautogui.press('space')
        hitTabRange(8)
    elif (TYPE == 'Ruby'):
        hitTabRange(1)
        pyautogui.press('space')
        hitTabRange(7)
    elif (TYPE == 'C'):
        hitTabRange(2)
        pyautogui.press('space')
        hitTabRange(6)
    elif (TYPE == 'C+Make'):
        hitTabRange(3)
        pyautogui.press('space')
        hitTabRange(5)
    elif (TYPE == 'Nxc'):
        hitTabRange(4)
        pyautogui.press('space')
        hitTabRange(4)
    elif (TYPE == 'SpiC'):
        hitTabRange(5)
        pyautogui.press('space')
        hitTabRange(3)
    elif (TYPE == 'Python'):
        hitTabRange(6)
        pyautogui.press('space')
        hitTabRange(2)
    
    pyautogui.press('space')
    
def createNewFile(FILENAME, PROJECT_TYPE, TYPE):
    openContextMenuFile()
    time.sleep(0.5)
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep( 2 )
    pyautogui.typewrite(FILENAME, interval=0.2)
    
    #Next, select file type.
    hitTabRange(1)
    
    if (PROJECT_TYPE == 'C'):
        if (TYPE == 'C'):
            logger.info('Zup3x is trying to select <Source C> type for new file')
            #Already checked. pass!
            #pyautogui.press('enter')
            hitTabRange(4)
        elif(TYPE == 'H'):
            logger.info('Zup3x is trying to select <Header C> type for new file')
            hitTabRange(1)
            pyautogui.press('space')
            hitTabRange(3)
        elif(TYPE == 'Makefile'):
            logger.info('Zup3x is trying to select <Makefile> type for new file')
            hitTabRange(2)
            pyautogui.press('space')
            hitTabRange(2)
    
    pyautogui.press('space')

#Only meant for Windows OS (Fix for thoses who possese azerty keyboard)
def PasteBuffer(BUFFER):
    #xerox.copy(BUFFER)
    manualHotKey(CTRL_SWAP, 'v')
    
def WhipeAll():
    manualHotKey(CTRL_SWAP, 'a')
    pyautogui.press('backspace')

def selectExplorerZone():
    pyautogui.moveTo(int(SCREEN_X/15), int(SCREEN_Y/3), 2)
    pyautogui.click()

def selectEditorZone():
    pyautogui.moveTo(int(SCREEN_X/2), int(SCREEN_Y/2), 2)
    pyautogui.click()

def findXMLElement(TREE, TAG_TARGET):
    for child in TREE:
        if (child.tag == TAG_TARGET):
            return child.text
    return None

def deleteXMLTrace(SESSION):
    
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    
    for fl in glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/*.xml"):
        #Do what you want with the file
        os.remove(fl)

def getDeclaredFilesHop3x(XMLTREE):
    try:
        with open(XMLTREE, 'r') as f1:
            data = f1.read()
    except IOError as e:
        logger.error('Unable to read XML file tree, see <'+XMLTREE+'>')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        return False
    
    declaredFiles = []
    
    for child in root:
        declaredFiles.append(child.text)
        
    return declaredFiles

def getDeclaredFilesProject(SESSION, PROJECT_NAME):
    #hop3xEtudiant\data\workspace\2015-Travail-Personnel\TDA-Annexes
    return getDeclaredFilesHop3x('hop3xEtudiant/data/workspace/'+SESSION+'/'+PROJECT_NAME+'/'+PROJECT_NAME+'.xml')

def getLastestTraceBuffer(SESSION, CLIENT_NAME = False):

    if (CLIENT_NAME == False):
        CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
        AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    else:
        AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)

    if (len(AVAILABLE_TRACE) == 0):
        return False
    
    try:
        with open (AVAILABLE_TRACE[-1], "r") as myfile:
            data=myfile.read()
    except IOError as e:
        logger.error('Unable to open Hop3x XML trace <'+AVAILABLE_TRACE[-1]+'>')
        return False
    
    data += '</TRACE>'
    return data

def getActiveSession():
    CLIENTS_NAME = os.listdir("Hop3xEtudiant/data/trace/")

    for client in CLIENTS_NAME:
        SESSIONS_AVAILABLE = os.listdir('Hop3xEtudiant/data/trace/'+client+'/')
        for session in SESSIONS_AVAILABLE:
            logger.info('Probing <'+session+'> with <'+client+'>')
            XMLTrace = getLastestTraceBuffer(session, client)
            if (XMLTrace != False):
                tree = ET.ElementTree(ET.fromstring(XMLTrace))
                root = tree.getroot()

                if (len(root) > 0):
                    lAttrib = root[-1].attrib
                    #Search for event that aren't too old.
                    if (lAttrib['K'] == 'CONNECTION' and (((int(time.time()*1000) - int(lAttrib['T']))/1000) < 60)):
                        return {'client':client, 'session':session}
            else:
                logger.warning('Unable to get lastest trace buffer')
    
    logger.warning('Unable to get current active session')
    return None

def getFileHandled(SESSION):
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    
    lAttrib = root[-1].attrib

    if (lAttrib['K'] == 'IT' or lAttrib['K'] == 'ST' or lAttrib == 'AF'):
        return findXMLElement(root[-1], 'F')
    else:
        return False

def checkFileHandled(SESSION, FILE_TARGET):
    
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    
    lAttrib = root[-1].attrib

    if ((lAttrib['K'] == 'IT' or lAttrib['K'] == 'ST' or lAttrib == 'AF')  and findXMLElement(root[-1], 'F') == FILE_TARGET):
        logger.info(lAttrib['K']+' event on <'+FILE_TARGET+'> detected using XML parser.')
        return True
    else:
        return False

def getCurrentProject(SESSION):
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'IT' or lAttrib['K'] == 'ST'):
        return findXMLElement(root[-1], 'P')
    else:
        return 'Unknown'

def isClientInitialized(SESSION):
    
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'CONNECTION'):
        return True
    else:
        return False
    
def isClientDeconnected(SESSION):
    
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'DECONNECTION'):
        return True
    else:
        return False

def isProjectCreated(SESSION):
    
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'AP'):
        return True
    else:
        return False

def isFileCreated(SESSION):
    
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    #Fix when Hop3x insert default code with new file
    lAttrib = root[-2].attrib
    
    if (lAttrib['K'] == 'AF'):
        return True
    else:
        return False

def isFileDeleted(SESSION):
    data = getLastestTraceBuffer(SESSION)
    if (data == False):
        logger.warning('Unable to get lastest XML trace from trace folder !')
        return False
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        logger.error('Enable to parse XML, tree is empty, see trace file')
        return False
    #Fix when Hop3x insert default code with new file
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'SF'):
        return True
    else:
        return False

def botWriter(BUFFER, FILE_EXTENSION):
    
    selectEditorZone()
    WhipeAll() #Delete default text provided by Hop3x
    
    #We need to detect /* */ if file extention == C or H
    bufSize = len(BUFFER)
    EnableCodeC = False
    MakefileCode = False
    speedWriter = 0.2
    lastspeedUpdate = 0

    if (FILE_EXTENSION == 'C' or FILE_EXTENSION == 'H'):
        EnableCodeC = True
    elif(FILE_EXTENSION == 'Makefile'):
        MakefileCode = True
    
    FixMultipleLineComment = False
    C_CommentSlashAsterix = False
    OneLineAcol = False
    FixUnknownSpaceAfterMultipleLineComment = False #Hop3xGeniusBar
    
    MakeBackSlash = False
    pos = 0
    
    for c in BUFFER:
        
        #Detection of multiple line comment /* */ and one line { .. }
        if (EnableCodeC and pos+1 < bufSize and BUFFER[pos] == '/' and BUFFER[pos+1] == '*'):
            C_CommentSlashAsterix = True
        elif(EnableCodeC and c == '{'):
            OneLineAcol = True
        
        #Simulate afraid student of data loss..
        if (pos == bufSize/2):
            saveCurrentFile()
            logger.info('Zup3x trigger CTRL+S at half of the current work')
        elif(pos == bufSize/3):
            saveCurrentFile()
            logger.info('Zup3x trigger CTRL+S at one third of the current work')
        
        if (c == '\n'):
            pyautogui.press('enter')
            if (C_CommentSlashAsterix == True):
                FixMultipleLineComment = True
            elif(OneLineAcol == True):
                OneLineAcol = False
            elif(MakeBackSlash == True or FixUnknownSpaceAfterMultipleLineComment == True):
                pyautogui.press('backspace')
                MakeBackSlash = False
                FixUnknownSpaceAfterMultipleLineComment = False
            time.sleep(speedWriter)
        elif(c == '\t'):
            if (EnableCodeC == False and MakefileCode == False):
                pyautogui.press('\t')
                time.sleep(speedWriter)
                MakeBackSlash = True
        elif(c == ' '):
            pyautogui.press('space')
            time.sleep(speedWriter)
        elif(c == '/'):
            
            if (C_CommentSlashAsterix == True and pos-1 >= 0 and BUFFER[pos-1] == '*'):
                C_CommentSlashAsterix = False
                if (FixMultipleLineComment == False):
                    pyautogui.press('/')
                    time.sleep(speedWriter)
                else:
                    FixMultipleLineComment = False
                    FixUnknownSpaceAfterMultipleLineComment = True
            else:
                pyautogui.press('/')
                time.sleep(speedWriter)
        elif(c == '{'):

            #Take a rest if needed
            if ((random.randrange(int((pos/bufSize) *100), 100)) > 98):
                speedWriter = random.randrange(120, 600)
                if speedWriter < 340:
                    logger.info('Your assistant need to take a pee, let me '+str(speedWriter)+' sec. I\'ll be back !')
                else:
                    logger.info('Your assistant need to take a nap for '+str(speedWriter)+' sec. I\'ll be back !')

            pyautogui.press('{')
            time.sleep(speedWriter)
        elif(c == '}'): 
            if (EnableCodeC == True and OneLineAcol == False):
                pyautogui.press('down')
                pyautogui.press('enter')
            else:
                pyautogui.press('}')
            time.sleep(speedWriter)
        elif(c == '*'):
            
            if (FixMultipleLineComment == True and pos+1 < bufSize and BUFFER[pos+1] == '/'):
                pyautogui.press('down')
                pyautogui.press('enter')
            else:
                if (FixMultipleLineComment == True and pos-1 >= 0 and BUFFER[pos-1] == '\n'):
                    pass
                else:
                    pyautogui.press(STARS_SWAP)
                    time.sleep(speedWriter)
        elif(c == '\xc3'):  
            pyautogui.press('e')
            time.sleep(speedWriter)
        else:
            pyautogui.typewrite(c, interval=speedWriter)
        
        #Simulate human variations for typing.
        if (pos+1 < bufSize and BUFFER[pos] == BUFFER[pos+1]):
            speedWriter = 0.09
        elif (lastspeedUpdate+random.randrange(1, 25) == pos):
            lastspeedUpdate = pos
            speedWriter = random.uniform(0.15, 0.3)
        elif(speedWriter == 0.09):
            lastspeedUpdate = pos
            speedWriter = random.uniform(0.15, 0.3)
        elif(speedWriter >= 120):
            logger.info('This was refreshing. Thank you for letting me take a nap/rest.')
            speedWriter = random.uniform(0.15, 0.3)

        pos += 1
        

def setHop3xLogin(username, password):
    pyautogui.typewrite(username, interval=0.2)
    pyautogui.press('tab')
    pyautogui.typewrite(password, interval=0.2)
    pyautogui.press('enter')

def selectHop3xSession(SessionID = 1):
    for i in range(SessionID):
        pyautogui.press('down')
        time.sleep( 0.5 )
    pyautogui.press('enter')

def parseSession():
    return os.listdir("Hop3xEtudiant/data/workspace/")

def getTargetSession(SESSIONS, PROJECT_NAME):
    for session in SESSIONS:
        if (os.path.exists('Hop3xEtudiant/data/workspace/'+session+'/'+PROJECT_NAME) == True):
            return session

    return 'Unknown'

def projectExist(SESSION, PROJECT_NAME):
    if os.path.exists("Hop3xEtudiant/data/workspace/"+SESSION+"/"+PROJECT_NAME) == True:
        return True
    
    return False

def getFileNameWithoutExtension(FILE_NAME):
    filename, file_extension = os.path.splitext(FILE_NAME)    
    return filename

def getFileExtension(FILE_NAME):
    if (FILE_NAME.lower() == 'makefile'):
        return 'Makefile'
    else:
        filename, file_extension = os.path.splitext(FILE_NAME)
        return file_extension

def getFileLanguage(FILE_NAME):
    if (FILE_NAME.lower() == 'makefile'):
        return 'Makefile'
    
    Extention = getFileExtension(FILE_NAME)
    
    if (Extention.lower() == '.c'):
        return 'C'
    elif(Extention.lower() == '.h'):
        return 'H'
    elif(Extention.lower() == '.rb'):
        return 'Ruby'
    elif(Extention.lower() == '.py'):
        return 'Python'
    elif(Extention.lower() == '.class' or Extention.lower() == '.java'):
        return 'Java'
    else:
        logger.warning('Zup3x does not recognize file extension for <'+FILE_NAME+'>')
        return 'Unknown'

def loadLocalProjects():
    dirCotent = os.listdir("localProjects/")
    projectsList = []

    for element in dirCotent:
        if (os.path.isdir('localProjects/'+element) == True):
            projectsList.append(element)
    
    return projectsList

def loadWorkSpaceProjects(SESSION):
    dirCotent = os.listdir("hop3xEtudiant/data/workspace/"+SESSION+"/")
    projectsList = []

    for element in dirCotent:
        if (os.path.isdir('hop3xEtudiant/data/workspace/'+SESSION+'/'+element) == True):
            projectsList.append(element)

    projectsList.sort()
    return projectsList

def legacyQuitHop3x():
    manualHotKey(CTRL_SWAP, 'q')
    time.sleep(1) #Let messagebox appear on the screen
    pyautogui.press('enter')

def getArgValue(target, argv):
    
    pos = 0;
    argSize = len(argv)
    
    for p in argv:
        if (p == '-'+target and pos+1 < argSize):
            return argv[pos+1]
        pos += 1
        
    return None

def searchFileExplorer(SESSION, FILE_TARGET, FILES_LIST, PROJECT_TARGET):
    
    declaredFiles = getDeclaredFilesProject(SESSION, PROJECT_TARGET)

    #Test current file
    selectEditorZone()
    pyautogui.press('space')
    time.sleep(1)
    pyautogui.press('backspace')

    #Verify if we are on the right project
    currentProject = getCurrentProject(SESSION)
    projectsList = loadWorkSpaceProjects(SESSION)

    if (currentProject != PROJECT_TARGET):
        logger.info('Using smart move with Hop3x explorer to find <'+FILE_TARGET+'> on <'+SESSION+'>')
        for i in range(len(projectsList)+1):
            selectExplorerZone()

            #If not on the target project, we move!
            currentDeclaredFiles = getDeclaredFilesProject(SESSION, currentProject)
            if (currentDeclaredFiles == False):
                logger.error('Unable to get declared file(s) for <'+currentProject+'> in <'+SESSION+'>')
                return False
            logger.info('Project <'+currentProject+'> has '+str(len(currentDeclaredFiles)+1)+' file(s), moving..')

            if (currentProject < PROJECT_TARGET): #We go down!
                print (str(projectsList))
                if ((projectsList.index(currentProject)+1 <= len(projectsList)) and (getDeclaredFilesProject(SESSION, projectsList[projectsList.index(currentProject)+1]) == False)):
                    offset = 1
                else:
                    offset = 0
                for i in range(int(math.fabs(currentDeclaredFiles.index(getFileHandled(SESSION)) - currentDeclaredFiles.index(currentDeclaredFiles[-1]))) + 2 + offset):
                    pyautogui.press('down')
                    time.sleep(0.2)
            else: #Go up!
                
                if ((projectsList.index(currentProject)-1 >= 0) and (getDeclaredFilesProject(SESSION, projectsList[projectsList.index(currentProject)-1]) == False)):
                    offset = 1
                else:
                    offset = 0
                for i in range(int(math.fabs(currentDeclaredFiles.index(getFileHandled(SESSION)) - currentDeclaredFiles.index(currentDeclaredFiles[-1]))) + 1 + offset):
                    pyautogui.press('up')
                    time.sleep(0.2)

            #Test if we are on the target project
            selectEditorZone()
            time.sleep(1)
            pyautogui.press('space')
            time.sleep(1)
            pyautogui.press('backspace')
            time.sleep(2)

            if (getCurrentProject(SESSION) == currentProject):
                #If project was minimized..
                selectExplorerZone()
                if (currentProject < PROJECT_TARGET):
                    pyautogui.press('down')
                    time.sleep(0.2)

                selectEditorZone()
                time.sleep(1)
                pyautogui.press('space')
                time.sleep(1)
                pyautogui.press('backspace')
                time.sleep(2)

            #Verify if we are on the right project
            currentProject = getCurrentProject(SESSION)
            if (currentProject == PROJECT_TARGET):
                break
            

    #It can't be! Something wrong.. or missed!
    if (currentProject != PROJECT_TARGET):
        logger.error('Unable to find project <'+PROJECT_TARGET+'> on Hop3x explorer, our logic failed..')
        return False

    #If we are actually on the target file
    if (getFileHandled(SESSION) == FILE_TARGET):
        return True
    
    for i in range(len(declaredFiles)):
        
        selectExplorerZone()

        cfile = getFileHandled(SESSION)
        if (declaredFiles.index(cfile) < declaredFiles.index(FILE_TARGET)):
            for i in range(int(math.fabs(declaredFiles.index(cfile)-declaredFiles.index(FILE_TARGET)))):
                pyautogui.press('down')
        else:
            for i in range(int(math.fabs(declaredFiles.index(cfile)-declaredFiles.index(FILE_TARGET)))):
                pyautogui.press('up')

        selectEditorZone()
        time.sleep(1)
        pyautogui.press('space') #Stealth char
        time.sleep(1)
        pyautogui.press('backspace')
        time.sleep(2)
        #Check if we are on the target file
        if (getFileHandled(SESSION) == FILE_TARGET):
            return True
        #If not, well, let's continue..
        selectExplorerZone()
    
    return False

def Zup3x_CORE(username, password, Hop3x_Instance):
    
    logger.info('We are waiting for Hop3x applet to initialize (5s)')
    #Handle Hop3x login applet
    time.sleep( 8 ) #Wait for it..
    #Hop3x_Instance.terminate()
    logger.info('GUI Bot: Processing automatic login')
    setHop3xLogin(username, password)
    
    #Select session
    time.sleep( 2 )
    logger.info('GUI Bot: Session automatic selection')
    selectHop3xSession(1)
    time.sleep( 25 )
    
    #Get session name by parsing workspace rep.
    logger.info('Parsing available session folder(s)..')
    SESSIONS = parseSession()

    logger.info('Session(s) = '+str(SESSIONS))
    
    if (len(SESSIONS) == 0):
        logger.critical('There\'s no session available, something wrong!')
        Hop3x_Instance.terminate()
        notifyStats['error'] += 1
        return -1
    
    #Tolerance
    for i in range(allowFailure):

        currentSession = getActiveSession()

        if (currentSession is None):
            logger.warning('Unable to find any <CONNECTION> event on Hop3x XML Trace, trying again..')
            notifyStats['error'] += 1
            time.sleep(10)
        else:
            break
    
    if (currentSession is None):
        logger.critical('Zup3x failed to initialize Hop3x, user/mdp may be wrong!')
        Hop3x_Instance.terminate()
        notifyStats['error'] += 1
        return -1

    logger.info('Zup3x is binded to <'+currentSession['client']+'> with session <'+currentSession['session']+'>')

    LOCAL_PROJECTS = loadLocalProjects()
    logger.info('Target project(s) = '+str(LOCAL_PROJECTS))
    
    for project in LOCAL_PROJECTS:
        
        logger.info('Zup3x is now working on <'+project+'> project')
        #Search for current project name in sessions workspaces
        targetSession = getTargetSession(SESSIONS, project)

        if (targetSession != 'Unknown'):
            declaredFiles = getDeclaredFilesProject(targetSession, project)
            logger.info('Zup3x has detected project <'+project+'> in session ['+targetSession+'] with: '+str(declaredFiles))

        else:
            logger.info('Project <'+project+'> does not seem to be on Hop3x for now..')

        #Do we have to create a new project ?
        if (projectExist(currentSession['session'], project) == False):
            logger.warning('This session does not have any project named <'+project+'>')
            logger.info('Zup3x is now trying to create a new project in <'+currentSession['session']+'>')
            createNewProject(project, 'C+Make')
            time.sleep(2) #Let Hop3x time to create event on XML trace file
            #targetSession = getTargetSession(SESSIONS, project)
            time.sleep(2)

            for i in range(allowFailure):
                creationStatus = isProjectCreated(currentSession['session'])
                if (creationStatus == False):
                    logger.warning('Unable to find <AP> event, project isn\'t created yet, waiting..')
                    notifyStats['warning'] += 1
                    time.sleep(15)
                else:
                    break;

            #If we are unable to create a new project
            if (creationStatus == False):
                logger.critical('Unable to find <AP> event, Hop3x haven\'t created our project. What a shame!')
                Hop3x_Instance.terminate()
                notifyStats['error'] += 1
                return -3
            else:
                #targetSession = getTargetSession(SESSIONS, project)
                logger.info('Project <'+project+'> has been created in session ['+currentSession['session']+']')
                notifyStats['projectCreated'] += 1

        else:
            logger.info('Hop3x does have <'+project+'> in his local workspace, no need to create.')

        #Load local project files list
        logger.info('Loading files list in localProjects/'+project+'/*')
        files = os.listdir("localProjects/"+project)
        if (len(files) == 0):
            logger.warning('There\'s no file to work on with <'+project+'>')
            notifyStats['warning'] += 1
            continue
        
        logger.info('File(s) to process = '+str(files))

        deletedFiles = []
        #List of element to delete from Hop3x
        if (targetSession != 'Unknown' and declaredFiles != False and len(declaredFiles) > 0):
            for rfile in declaredFiles:
                if rfile not in files:
                    deletedFiles.append(rfile)

        #Part were we delete file that aren't needed anymore..!
        if (len(deletedFiles) > 0):
            logger.info('File(s) to delete = '+str(deletedFiles))

            for rfile in deletedFiles:
                logger.info('Zup3x is trying to delete <'+rfile+'> from Hop3x.')
                if (searchFileExplorer(currentSession['session'], rfile, declaredFiles, project) == True):
                    deleteCurrentFile()
                    time.sleep(2)
                    for i in range(allowFailure):
                        deleteStatus = isFileDeleted(currentSession['session'])
                        if (deleteStatus == False):
                            logger.warning('Unable to find <SF> event, file isn\'t deleted yet, waiting..')
                            notifyStats['warning'] += 1
                            time.sleep(15)
                        else:
                            break

                    if (deleteStatus == False):
                        logger.error('Unable to find <SF> event, this file could not be deleted, what a shame..!')
                        notifyStats['error'] += 1
                    else:
                        logger.info('<'+rfile+'> has been deleted from <'+currentSession['session']+'>')
                        notifyStats['deletedFiles'] += 1

                else:
                    logger.error('Unable to delete <'+rfile+'> from Hop3x, file not found !')
                    notifyStats['error'] += 1

        #Part were we edit files or create new ones
        for cfile in files:
            #Check file
            if (os.path.isdir("localProjects/"+project+"/"+cfile) == False):

                if (os.path.exists("Hop3xEtudiant/data/workspace/"+currentSession['session']+"/"+project+"/"+cfile) == False):
                    logger.info('<'+cfile+'> does not exist in Hop3x local workspace')
                    logger.info('Zup3x is trying to create <'+cfile+'> in Hop3x')
                    createNewFile(getFileNameWithoutExtension(cfile), 'C', getFileLanguage(cfile))
                    time.sleep(2) #Let Hop3x time to create event on XML trace file

                    for i in range(allowFailure):
                        creationStatus = isFileCreated(currentSession['session'])
                        if (creationStatus == False):
                            logger.warning('Unable to find <AF> event, file isn\'t created yet, waiting..')
                            notifyStats['warning'] += 1
                            time.sleep(15)
                        else:
                            break;


                    if (creationStatus == False):
                        logger.critical('Unable to find <AF> event, Hop3x haven\'t created our file <'+cfile+'>. What a shame!')
                        notifyStats['error'] += 1
                        Hop3x_Instance.terminate()
                        return -4
                    else:
                        logger.info('<'+cfile+'> has been created on project <'+project+'> with session <'+currentSession['session']+'>')
                        notifyStats['fileCreated'] += 1
                        
                    #Create buffer with target file.
                    with open ("localProjects/"+project+"/"+cfile, "r") as myfile:
                        data=myfile.read()

                    #Start writing code..!
                    botWriter(data, getFileLanguage(cfile))
                    #Save current state
                    saveCurrentFile()
                    logger.info('<'+cfile+'> is now up to date and saved with Hop3x.')
                else:
                    #Test if any differences
                    remoteSize = os.path.getsize("Hop3xEtudiant/data/workspace/"+currentSession['session']+"/"+project+"/"+cfile)
                    localSize = os.path.getsize("localProjects/"+project+"/"+cfile)
                    
                    #Non viable methode for changes detections, need to be reviewed!
                    if (math.fabs(remoteSize - localSize) > 50):
                        logger.info('<'+cfile+'> is newer than Hop3x local copy, Zup3x gonna update it! DiffSize = ('+str(math.fabs(remoteSize - localSize))+' octet(s))')
                        #Search for file in Hop3x explorer
                        if (searchFileExplorer(targetSession, cfile, files, project) == True):
                            logger.info('Zup3x is now ready to edit <'+cfile+'> in Hop3x editor, event IT/ST match file target!')
                            #Create buffer with target file.
                            with open ("localProjects/"+project+"/"+cfile, "r") as myfile:
                                data=myfile.read()

                            #Start writing code..!
                            botWriter(data, getFileLanguage(cfile))
                            notifyStats['fileModified'] += 1
                        else:
                            logger.error('Unable to find ST/IT event that match file target, Zup3x is unable to edit <'+cfile+'>')
                            notifyStats['error'] += 1
                    else:
                        logger.info('<'+cfile+'> is up to date, no need to change anything!')
                    
            else:
                logger.warning('Unable to process <localProjects/'+project+'/'+cfile+'>, Hop3x does not support dir creation!')
                notifyStats['warning'] += 1
                
    return 0

def getRemoteRepository(bb_user, bb_pass):
    
    logger.info('Trying to update remote repository from BitBucket API')
    listRe = getHop3xRepo(bb_user, bb_pass)
    
    for racine in listRe:
        if ( (os.path.exists('localProjects/'+racine['name']) == False)):
            if ((racine['name'][:5] == 'hop3x')):
                logger.info('Zup3x has detected new repository named '+racine['name'])
                try:
                    subprocess.Popen(['git', 'clone', 'https://'+bb_user+':'+bb_pass.replace('@', '%40')+'@bitbucket.org/'+bb_user+'/'+racine['name']+'.git', 'localProjects/'+racine['name']])
                except:
                    logger.error('Git is not installed on this machine!')
                    return
            else:
                logger.info('<'+racine['name']+'> is not meant to be cloned.')
        else:
            #Update current copy
            logger.info(racine['name']+' is being updated from lastest source available online')
            try:
                subprocess.Popen(['git', '-C', 'localProjects/'+racine['name'], 'pull', 'https://'+bb_user+':'+bb_pass.replace('@', '%40')+'@bitbucket.org/'+bb_user+'/'+racine['name']+'.git'])
            except:
                logger.error('Git is not installed on this machine!')
                return

if __name__ == "__main__":
    
    logger.info('Zup3x is waking up, collecting data..')
    
    if len(sys.argv) < 5:
        print ('usage: Zup3x.py -u [Hop3xUser] -p [Hop3xPass] [Optional: -ugit [BitBucketUser] -pgit [BitBucketPass] -sID [SessionID]]')
        logger.info('Starting GUI configuration..')
        
        username = pyautogui.prompt(text='Please provide Hop3x username', title='Zup3x Login' , default='')
        password = pyautogui.password(text='Please type your password', title='Zup3x Login', default='', mask='*')
        
        choise = pyautogui.confirm(text='Do you want to enable git support ?', title='Zup3x', buttons=['Yes', 'No'])
        if (choise == 'Yes'):
            bb_user = pyautogui.prompt(text='Please provide BitBucket username', title='Bitbucket' , default='')
            bb_pass = pyautogui.password(text='Please type your password', title='Bitbucket', default='', mask='*')
        else:
            bb_user = None
            bb_pass = None

        choise = pyautogui.confirm(text='Do you want to enable gmail notification', title='GMail', buttons=['Yes', 'No'])
        if (choise == 'Yes'):
            NotifyAccount = pyautogui.prompt(text='Please provide GMail username without @gmail.com', title='GMail' , default='')
            NotifyPassword = pyautogui.password(text='Please type your GMail password', title='GMail', default='', mask='*')
        else:
            NotifyAccount = None
            NotifyPassword = None

    else:
        
        username = getArgValue('u', sys.argv)
        password = getArgValue('p', sys.argv)
        
        bb_user = getArgValue('ugit', sys.argv)
        bb_pass = getArgValue('pgit', sys.argv)
        
        sessionID = getArgValue('sID', sys.argv)

        keyboardLayout = getArgValue('kl', sys.argv)

        NotifyAccount = getArgValue('nu', sys.argv)
        NotifyPassword = getArgValue('np', sys.argv)
    
    if (username is None or password is None):
        logger.critical('Hop3x credentials are needed! Unable to use Hop3x !')
        exit()
    if (keyboardLayout is None):
        logger.info('Set custom keyboard layout with [-kl], default is azerty.')
        keyboardLayout = 'azerty'

    #Download Hop3x is not available
    if (os.path.exists('hop3xEtudiant/') == False):
        if (getHop3x() == False):
            logger.critical('Unable to install Hop3x etudiant, Zup3x is unable to continue !')
            exit()

    #Ask pyautogui to switch to azerty layout
    logger.info('Set pyautogui keyboard layout as <'+keyboardLayout+'>')
    try:
        pyautogui.setKeyboardLayout(keyboardLayout)
    except:
        logger.warning('Cannot set keyboard layout, you may want to change it to QWERTY !')

    notifyHandle = Notify(NotifyAccount, NotifyPassword)
    #Full time job!
    while (True):
        
        t1 = datetime.now() #micro time begin
        
        #Download lastest source from Bitbucket
        if (bb_user is None or bb_pass is None):
            logger.info('Optional: You must provide bitbucket login/password to enable remote work')
        else:
            logger.info('Zup3x is trying to fetch lastest sources from your bitbucket space..')
            getRemoteRepository(bb_user, bb_pass)
        
        logger.info('Loading local project(s) list from localProjects/*')

        #Read local project(s) name(s) if any
        LOCAL_PROJECTS = loadLocalProjects()

        #If there's not local project to process
        if (len(LOCAL_PROJECTS) == 0):
            logger.warning('Unable to find local project, localProjects/ is empty. Your assistant gonna be unemployed! Do something..')

        #Test if Hop3x is already installed
        if (os.path.exists('hop3xEtudiant/lib/Hop3xEtudiant.jar') == False):
            logger.critical('Unable to find Hop3xEtudiant.jar in <hop3xEtudiant/lib/Hop3xEtudiant.jar>')
            logger.critical('Zup3x cannot continue, sorry!')
            exit()
        #Used to redirect Hop3x stdout, stderr stream
        FNULL = open(os.devnull, 'w')
        
        #Bot core, handle Hop3x like human being.
        if (len(LOCAL_PROJECTS) > 0):
            #Create subprocess of JRE with hop3x as executable
            logger.info('Zup3x is creating subprocess for Hop3x through JRE [-Xmx512m -jar]')

            try:
                Hop3x_Instance = subprocess.Popen(['java', '-Xmx512m', '-jar', 'hop3xEtudiant/lib/Hop3xEtudiant.jar'], stdout=FNULL, stderr=FNULL)
            except:
                logger.critical('Zup3x is unable to find Java runtime environement')
                exit()

            res = Zup3x_CORE(username, password, Hop3x_Instance)
        else:
            res = 1

        waitNextIter = 0
        
        #Check if bot has done his task (== 0) or if failed (< 0)
        if (res >= 0):
            logger.info('Zup3x have done his duty, everything should be fine.')
            waitNextIter = random.randrange(3600, 6600)
            logger.info("Next interation in %i sec" % waitNextIter)

            legacyQuitHop3x()
            time.sleep(5)

        elif(res < 0):
            waitNextIter = 25
            logger.warning("Next iteration in %i sec after issue(s), abord with code %i" % (waitNextIter, res))
        
        SESSIONS = parseSession()
        
        if (len(SESSIONS) != 0):
            #If there aren't any DECONNECTION symbol on XML trace
            if (isClientDeconnected(SESSIONS[0]) == False):
                logger.warning('Zup3x failed to quit Hop3x properly, SIGQUIT sended instead!')
                logger.warning('Failed to quit Hop3x properly, force quit instead..!')
                Hop3x_Instance.terminate()
        
        t2 = datetime.now()
        delta = t2 - t1

        if (NotifyAccount != None and NotifyPassword != None):
            statResume = '''Zup3x notify by your slave, heum.. I mean assistant!\n\n%i project(s) were created.
                        \n%i file(s) were created\n%i file(s) were modified\n%i file(s) were deleted\n\n
                        %i error(s) was faced and got %i warning(s)\n\n\nI attached the lastest log to be sure!''' % (notifyStats['projectCreated'], notifyStats['fileCreated'], notifyStats['fileModified'], notifyStats['fileDeleted'], notifyStats['error'], notifyStats['warning'])

            notifyHandle.send('[Zup3x] Instance ending ('+str(notifyStats['error'])+' error(s), '+str(notifyStats['warning'])+' warning(s))', statResume)

        logger.info('Zup3x have worked for '+str(delta.total_seconds())+' sec.')

        #Reset notifyStats
        notifyStats['projectCreated'] = 0
        notifyStats['fileCreated'] = 0
        notifyStats['fileModified'] = 0
        notifyStats['error'] = 0
        notifyStats['warning'] = 0

        FNULL.close()
        time.sleep(waitNextIter)