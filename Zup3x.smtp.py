'''
    Zup3x Client
    Description: Zup3x Notification (Mail)
    Author(s): Jérémy SIMON
    Version: Stable
    Notice: This stand only for educational purposes, we won't be held responsible for any damage or accident you made with this tool.
    
    dep. pip install pyautogui, httplib2, git, xerox
'''

__author__ = "Jokoast"
__date__ = "$20 sept. 2015 15:21:57$"

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notify:
    
    smtp_host = 'smtp.gmail.com' #Tu peux config le SMTP que tu veux
    smtp_port = 587
    
    def __init__(self, usr, password):
        self.username = usr
        self.password = password
        
    def notify(self, title, message):
        server = smtplib.SMTP(host = smtp_host, port = smtp_port)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        fromaddr = config['email_user'] + "@gmail.com" #Et du coup prévoir l'ajout du @domainname
        toaddr = config['email_user'] + "@gmail.com"
        sub = title
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = sub  
        msg.attach(MIMEText(message, 'plain'))
        
        server.sendmail(config['email_user'],toaddr,msg.as_string())
        server.quit()
