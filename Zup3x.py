#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    Zup3x Client
    Description: Hop3x Assistant Bot
    Author(s): TAHRI Ahmed
    Version: Alpha
    Notice: 
    
        This stand only for educational purposes, 
        we won't be held responsible for any damage or accident 
        you made with this tool.
    
    dep. pip install pyautogui, httplib2, xerox
'''

import subprocess 
import os
import glob
import pyautogui
import httplib2 
import json 
import time
import sys
import xerox
import xml.etree.cElementTree as ET
import math
from datetime import datetime

__author__ = "Ousret"
__date__ = "$19 sept. 2015 11:15:33$"

__VERSION__ = '0.1a' #Local Zup3x revision
ZUP3X_ROOT_PATH = 'java -Xmx512m -jar Hop3xEtudiant/hop3xEtudiant/lib/Hop3xEtudiant.jar'

SCREEN_X, SCREEN_Y = pyautogui.size()
BUTTON_TAB_SCROLL_MAX = 19

PROJECT_TYPE = 'C'
SESSIONS = []
PROJECT_FILELIST = []

ENABLE_GIT = False
ENABLE_LOCAL = True

LOCAL_PROJECTS = []

def getHop3xRepo(Username, Password):
    API_BB = httplib2.Http(".cache")
    API_BB.add_credentials(Username, Password) # Basic authentication
    resp, content = API_BB.request("https://api.bitbucket.org/1.0/user/repositories", "GET")
    repoList = json.loads(content.decode("utf-8"))
    return repoList
def closeContextMenu():
    pyautogui.press('esc')
    
def openContextMenuFile():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('f')
    
    pyautogui.keyUp('alt')
    pyautogui.keyUp('f')
    
def openContextMenuEdition():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('e')
    
    pyautogui.keyUp('alt')
    pyautogui.keyUp('e')
    
def openContextMenuTools():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('t')
    
    pyautogui.keyUp('alt')
    pyautogui.keyUp('t')

def openContextMenuAssist():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('a')
    
    pyautogui.keyUp('alt')
    pyautogui.keyUp('a')

def hitTabRange(NB_TIME):
    for i in range(NB_TIME):
        pyautogui.press('tab')
        time.sleep(0.2)

def createNewProject(PROJECT_NAME, TYPE):
    openContextMenuFile()
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep( 1 )
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
    time.sleep(0.2)
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep( 2 )
    pyautogui.typewrite(FILENAME, interval=0.2)
    
    #Next, select file type.
    hitTabRange(1)
    
    if (PROJECT_TYPE == 'C'):
        if (TYPE == 'C'):
            print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Select C Source file type.')
            #Already checked. pass!
            #pyautogui.press('enter')
            hitTabRange(4)
        elif(TYPE == 'H'):
            print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> GUI Bot: Select C Header file type.')
            hitTabRange(1)
            pyautogui.press('space')
            hitTabRange(3)
        elif(TYPE == 'Makefile'):
            print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> GUI Bot: Select C Makefile file type.')
            hitTabRange(2)
            pyautogui.press('space')
            hitTabRange(2)
    
    pyautogui.press('space')

#Only meant for Windows OS (Fix for thoses who possese azerty keyboard)
def PasteBuffer(BUFFER):
    
    xerox.copy(BUFFER)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('v')
    
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('v')
    
def WhipeAll():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('a')
    
    pyautogui.press('\r')

def selectExplorerZone():
    pyautogui.moveTo(SCREEN_X/15, SCREEN_Y/3, 2)
    pyautogui.click()

def selectEditorZone():
    pyautogui.moveTo(SCREEN_X/2, SCREEN_Y/2, 2)
    pyautogui.click()

def deleteXMLTrace(SESSION):
    
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    
    for fl in glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/*.xml"):
        #Do what you want with the file
        os.remove(fl)

def checkFileHandled(SESSION, FILE_TARGET):
    #<E K="IT" T="1442754654817" H="20/09/15-15:10:54"><T>d</T><F>c1lstop.c</F><P>TDA-Annexes</P><N>501</N></E>
    
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    
    if (len(AVAILABLE_TRACE) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse trace folder !')
        return False
    
    with open (AVAILABLE_TRACE[-1], "r") as myfile:
        data=myfile.read()
    
    data += '</TRACE>'
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    
    lAttrib = root[-1].attrib
    
    if ((lAttrib['K'] == 'IT'  and str(root[-1][2].text) == FILE_TARGET) or (lAttrib['K'] == 'ST' and str(root[-1][3].text) == FILE_TARGET)):
        print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> IT Event on '+FILE_TARGET+' detected using XML parser.')
        return True
    else:
        #print ('<Debug> '+lAttrib['K']+' Event on '+str(root[-1][2].text)+' detected using XML parser.')
        return False

def isClientInitialized(SESSION):
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    
    if (len(AVAILABLE_TRACE) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse trace folder !')
        return False
    
    with open (AVAILABLE_TRACE[-1], "r") as myfile:
        data=myfile.read()
    
    data += '</TRACE>'
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'CONNECTION'):
        return True
    else:
        return False
    
def isClientDeconnected(SESSION):
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    
    if (len(AVAILABLE_TRACE) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse trace folder !')
        return False
    
    with open (AVAILABLE_TRACE[-1], "r") as myfile:
        data=myfile.read()
    
    data += '</TRACE>'
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'DECONNECTION'):
        return True
    else:
        return False

def isProjectCreated(SESSION):
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    
    if (len(AVAILABLE_TRACE) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse trace folder !')
        return False
    
    with open (AVAILABLE_TRACE[-1], "r") as myfile:
        data=myfile.read()
    
    data += '</TRACE>'
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'AP'):
        return True
    else:
        return False

def isFileCreated(SESSION):
    CLIENT_NAME = os.listdir("Hop3xEtudiant/data/trace/")
    AVAILABLE_TRACE = sorted(glob.glob("Hop3xEtudiant/data/trace/"+CLIENT_NAME[0]+"/"+SESSION+"/" + "*.xml"), key=os.path.getctime)
    
    if (len(AVAILABLE_TRACE) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse trace folder !')
        return False
    
    with open (AVAILABLE_TRACE[-1], "r") as myfile:
        data=myfile.read()
    
    data += '</TRACE>'
    
    tree = ET.ElementTree(ET.fromstring(data))
    root = tree.getroot()
    
    if (len(root) == 0):
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'>> Enable to parse XML, tree is empty, see ['+AVAILABLE_TRACE[-1]+']')
        return False
    
    lAttrib = root[-1].attrib
    
    if (lAttrib['K'] == 'AF'):
        return True
    else:
        return False

def simulatePerfectStudent(BUFFER, FILE_EXTENSION):
    
    selectEditorZone()
    WhipeAll() #Delete default text provided by Hop3x
    
    #We need to detect /* */ if file extention == C or H
    
    bufSize = len(BUFFER)
    EnableCodeC = False
    MakefileCode = False
    
    Win32Host = False
    
    if sys.platform ==  'win32':
        Win32Host = True
    
    if (FILE_EXTENSION == 'C' or FILE_EXTENSION == 'H'):
        EnableCodeC = True
    elif(FILE_EXTENSION == 'Makefile'):
        MakefileCode = True
    
    FixMultipleLineComment = False
    C_CommentSlashAsterix = False
    OneLineAcol = False
    
    MakeBackSlash = False
    
    pos = 0
    
    for c in BUFFER:
        
        #Detection of multiple line comment /* */ and one line { .. }
        if (EnableCodeC and pos+1 < bufSize and BUFFER[pos] == '/' and BUFFER[pos+1] == '*'):
            C_CommentSlashAsterix = True
        elif(EnableCodeC and c == '{'):
            OneLineAcol = True
        
        if (c == '\n'):
            pyautogui.press('enter')
            if (C_CommentSlashAsterix == True):
                FixMultipleLineComment = True
            elif(OneLineAcol == True):
                OneLineAcol = False
            elif(MakeBackSlash == True):
                pyautogui.press('backspace')
                MakeBackSlash = False
        elif(c == '\t'):
            if (EnableCodeC == False and MakefileCode == False):
                pyautogui.press('\t')
                MakeBackSlash = True
        elif(c == ' '):
            pyautogui.press('space')
        elif(c == '\\' and Win32Host == True):
            PasteBuffer('\\')
        elif(c == '|' and Win32Host == True):
            PasteBuffer('|')
        elif(c == '/'):
            
            if (C_CommentSlashAsterix == True and pos-1 >= 0 and BUFFER[pos-1] == '*'):
                C_CommentSlashAsterix = False
                if (FixMultipleLineComment == False):
                    pyautogui.press('/')
                else:
                    FixMultipleLineComment = False
            else:
                pyautogui.press('/')
                
        elif(c == '_' and Win32Host == True):
            PasteBuffer('_')
        elif(c == '[' and Win32Host == True):
            PasteBuffer('[')
        elif(c == ']' and Win32Host == True):
            PasteBuffer(']')
        elif(c == '(' and Win32Host == True):
            PasteBuffer('(')
        elif(c == ')' and Win32Host == True):
            PasteBuffer(')')
        elif(c == '{' and Win32Host == True):
            PasteBuffer('{')
        elif(c == '}'): 
            if (EnableCodeC == True and OneLineAcol == False):
                pyautogui.press('down')
                pyautogui.press('enter')
            else:
                PasteBuffer('}')
        elif(c == '"' and Win32Host == True):
            PasteBuffer('"')
        elif(c == '#' and Win32Host == True):
            PasteBuffer('#')
        elif(c == '<' and Win32Host == True):
            PasteBuffer('<')
        elif(c == '!' and Win32Host == True):
            PasteBuffer('!')
        elif(c == '&' and Win32Host == True):
            PasteBuffer('&')
        elif(c == ':' and Win32Host == True):
            PasteBuffer(':')
        elif(c == '*'):
            
            if (FixMultipleLineComment == True and pos+1 < bufSize and BUFFER[pos+1] == '/'):
                pyautogui.press('down')
                pyautogui.press('enter')
            else:
                if (FixMultipleLineComment == True and pos-1 >= 0 and BUFFER[pos-1] == '\n'):
                    pass
                else:
                    pyautogui.press('multiply')
        elif(c == '\xc3'):  
            pyautogui.press('e')
        else:
            pyautogui.typewrite(c, interval=0.05)
            
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

def projectExist(SESSIONS, PROJECT_NAME):
    
    for file in SESSIONS:
        if os.path.exists("Hop3xEtudiant/data/workspace/"+file+"/"+PROJECT_NAME) == True:
            return True
    
    return False

def getFileNameWithoutExtension(FILE_NAME):
    filename, file_extension = os.path.splitext(FILE_NAME)    
    return filename

def getFileExtension(FILE_NAME):
    if (FILE_NAME == 'Makefile' or FILE_NAME == 'makefile'):
        return 'Makefile'
    else:
        filename, file_extension = os.path.splitext(FILE_NAME)
        return file_extension

def getFileLanguage(FILE_NAME):
    if (FILE_NAME == 'Makefile' or FILE_NAME == 'makefile'):
        return 'Makefile'
    
    Extention = getFileExtension(FILE_NAME)
    
    if (Extention == '.c' or Extention == '.C'):
        return 'C'
    elif(Extention == '.h' or Extention == '.H'):
        return 'H'
    elif(Extention == '.rb'):
        return 'Ruby'
    elif(Extention == '.py'):
        return 'Python'
    elif(Extention == '.class' or Extention == '.java'):
        return 'Java'
    else:
        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Unknown file extension for '+FILE_NAME)
        return 'Unknown'

def loadLocalProjects():
    return os.listdir("localProjects/")

def legacyQuitHop3x():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('q')
    
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('q')
    
    pyautogui.press('enter')

def getArgValue(target, argv):
    
    pos = 0;
    argSize = len(argv)
    
    for p in argv:
        if (p == '-'+target and pos+1 < argSize):
            return argv[pos+1]
        pos += 1
        
    return None

def searchFileExplorer(SESSION, FILE_TARGET, FILES_LIST):
    
    selectExplorerZone()
    
    #Be at the top of explorer selection
    for i in range(10):
        pyautogui.press('up')
    
    for file in FILES_LIST:
        
        pyautogui.press('down')
        selectEditorZone()
        pyautogui.press('d')
        time.sleep(1)
        pyautogui.press('backspace')
        if (checkFileHandled(SESSION, FILE_TARGET) == True):
            return True
        selectExplorerZone()
    
    return False

def Zup3x_CORE(username, password, Hop3x_Instance, remoteGit = False):
    
    print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Hop3x should be loading..')
    #Handle Hop3x login applet
    time.sleep( 5 ) #Wait for it..
    #Hop3x_Instance.terminate()
    print('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Automatic login')
    setHop3xLogin(username, password)
    
    #Select session
    time.sleep( 2 )
    print('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Session automatic selection..')
    selectHop3xSession(1)
    time.sleep( 10 )

    #Get session name by parsing workspace rep.
    print('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Parsing available session directory :')
    SESSIONS = parseSession()
    print ('<Dump> Sessions = '+str(SESSIONS))

    if (isClientInitialized(SESSIONS[0]) == False):
        print ('<Fatal '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Hop3x is not connected')
        Hop3x_Instance.terminate()
        return -1

    #Find local project if any
    print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Parsing local project(s) from localProjects/')
    LOCAL_PROJECTS = loadLocalProjects()

    if (len(LOCAL_PROJECTS) == 0):
        print ('<Fatal '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Zup3x does not see any local project..')
        return -2

    print('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Project(s) = '+str(LOCAL_PROJECTS))

    for project in LOCAL_PROJECTS:

        print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Processing '+project)

        #Do we have to create a new project ?
        if (projectExist(SESSIONS, project) == False):
            print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> '+project+' does not exist, GUI Bot: Create project')
            createNewProject(project, 'C+Make')
            if (isProjectCreated(SESSIONS[0]) == False):
                print('<Fatal '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Failed to create project.. Abord!')
                Hop3x_Instance.terminate()
                return -3
        else:
            print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> '+project+' project directory already exist.')

        #Load local project files list
        print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Parsing project files..')
        files = os.listdir("localProjects/"+project)
        if (len(files) == 0):
            print('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Project '+project+' seem to be empty.')
            continue

        print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Files to process: '+str(files))

        for file in files:
            #Check file
            if (os.path.isdir("localProjects/"+project+"/"+file) == False):

                #Hop3xEtudiant\data\workspace\2015-Travail-Personnel\TDA-Annexes
                if (os.path.exists("Hop3xEtudiant/data/workspace/"+SESSIONS[0]+"/"+project+"/"+file) == False):
                    print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Creating '+file+'..')
                    createNewFile(getFileNameWithoutExtension(file), 'C', getFileLanguage(file))

                    if (isFileCreated(SESSIONS[0]) == False):
                        print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> GUI Bot: Failed to create '+file+', abord..!')
                        Hop3x_Instance.terminate()
                        return -4

                    #Create buffer with target file.
                    with open ("localProjects/"+project+"/"+file, "r") as myfile:
                        data=myfile.read()

                    #Start writing code..!
                    simulatePerfectStudent(data, getFileLanguage(file))

                    #Save current state
                else:
                    #Test if any differences
                    remoteSize = os.path.getsize("Hop3xEtudiant/data/workspace/"+SESSIONS[0]+"/"+project+"/"+file)
                    localSize = os.path.getsize("localProjects/"+project+"/"+file)
                    
                    #Non viable methode for changes detections, need to be reviewed!
                    if (math.fabs(remoteSize - localSize) > 50):
                        print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> File '+file+' has been changed, will be rewrited.')
                        #Search for file in Hop3x explorer
                        if (searchFileExplorer(SESSIONS[0], file, files) == True):
                            print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> File '+file+' has been found in Hop3x editor')
                            
                            #Create buffer with target file.
                            with open ("localProjects/"+project+"/"+file, "r") as myfile:
                                data=myfile.read()

                            #Start writing code..!
                            simulatePerfectStudent(data, getFileLanguage(file))
                            
                        else:
                            print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Bot wasn\'t able to found '+file+' in Hop3x editor, sorry!')
                    else:
                        print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> '+file+' already up to date in Hop3x')
                    
                    

            else:
                print ("<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> localProjects/"+file+" is a directory !")
                
    return 0

def getRemoteRepository(bb_user, bb_pass):
    
    print ('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Trying to update remote repository from BitBucket API')
    listRe = getHop3xRepo(bb_user, bb_pass)
    
    for racine in listRe:
        print (racine['name']+' -- '+'https://bitbucket.org'+racine['resource_uri'])
        if ( (os.path.exists('localProjects/'+racine['name']) == False)):
            if ((racine['name'][:5] == 'hop3x')):
                print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Zup3x has detected new repository named '+racine['name'])
                try:
                    subprocess.Popen(['git', 'clone', 'https://'+bb_user+':'+bb_pass+'@bitbucket.org/'+bb_user+'/'+racine['name']+'.git', 'localProjects/'+racine['name']])
                except:
                    print ('<Fatal '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Git is not installed or is not in path (Windows case)')
            else:
                print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> '+racine['name']+' is not meant to be cloned.')
        else:
            #Git pull
            print ('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Zup3x does not known how to update '+racine['name']+', sorry!')

if __name__ == "__main__":
    
    print ('<Info> Zup3x is starting..')
    
    if len(sys.argv) < 5:
        print ('<Info> usage: Zup3x.py -u [Hop3xUser] -p [Hop3xPass] [Optional: -ugit [BitBucketUser] -pgit [BitBucketPass] -sID [SessionID]]')
        
        username = pyautogui.prompt(text='Please provide Hop3x username', title='Zup3x Login' , default='')
        password = pyautogui.password(text='Please type your password', title='Zup3x Login', default='', mask='*')
        
        choise = pyautogui.confirm(text='Do you want to enable git support ?', title='Zup3x Git', buttons=['Yes', 'No'])
        if (choise == 'Yes'):
            bb_user = pyautogui.prompt(text='Please provide BitBucket username', title='Bitbucket login' , default='')
            bb_pass = pyautogui.password(text='Please type your password', title='Bitbucket login', default='', mask='*')
		else:
			bb_user = None
			bb_pass = None
        
    else:
        
        username = getArgValue('u', sys.argv)
        password = getArgValue('p', sys.argv)
        
        bb_user = getArgValue('ugit', sys.argv)
        bb_pass = getArgValue('pgit', sys.argv)
        
        sessionID = getArgValue('sID', sys.argv)
    
    if (username is None or password is None):
        print ('<Fatal '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Hop3x credentials are needed!')
        exit()
    
    #Run without interuptions
    while (True):
        
        t1 = datetime.now()
        
        if (bb_user is None or bb_pass is None):
            print ('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> You must provide bitbucket login/password to handle remote work')
        else:
            getRemoteRepository(bb_user, bb_pass)
        
        print('<Info '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Core: Create subprocess for Hop3x')
        FNULL = open(os.devnull, 'w')
        Hop3x_Instance = subprocess.Popen(['java', '-Xmx512m', '-jar', 'hop3xEtudiant/lib/Hop3xEtudiant.jar'], stdout=FNULL, stderr=FNULL)
        
        res = Zup3x_CORE(username, password, Hop3x_Instance)
        waitNextIter = 0
        
        if (res == 0):
            waitNextIter = randrange(3600, 6600)
            print ("<Notice> Next iteration in %i sec." % waitNextIter)
        elif(res < 0):
            waitNextIter = 25
            print ("<Reset> Next iteration in %i sec after bad issue" % waitNextIter)
        
        legacyQuitHop3x()
        print('<Notice '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> You should be deconnected from Hop3x')
        
        SESSIONS = parseSession()
        
        #If there aren't any DECONNECTION symbol on XML trace
        if (isClientDeconnected(SESSIONS[0]) == False):
            print('<Warning '+time.strftime('%Y/%m/%d-%H:%M:%S')+'> Failed to quit Hop3x, force quit instead..!')
            Hop3x_Instance.terminate()
        
        t2 = datetime.now()
        delta = t2 - t1
        
        print ('<Info> Zup3x have worked for '+str(delta.total_seconds())+' sec.')
        
        time.sleep(waitNextIter)
