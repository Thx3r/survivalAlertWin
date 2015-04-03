#!/usr/bin/env python

#PYTHON 3 only

# Sample Windows Startup check -- Mail alert
# SurvivalAlert v1.0
# By thxer.com
# N-pn.fr Community and Hexpresso CTF team

import os
import socket
import ctypes
import smtplib


#Global Variables
HOSTNAME = str(socket.gethostname())
IPLAN = str(socket.gethostbyname(socket.gethostname()))
AUTHORIZE_USER = ['Users','Utilisateur'] #User wich are allow to use computers
LIMIT_FREE_HDD_SPACE = 11 # Limit of free HDD space alert in GB
#Email Settings
TO = "admin@1337.com"   # User who recept mail alert
USER = "smtp_user@1337.com"
PWD = "smtp_passwd"
SMTPSERV = "smtp.server_addres.com"

#Check HDD Status

def check_hdd():
    """Check HDD disk with windows tools """
    Hdd_status = os.popen("wmic diskdrive get status").read()
    for word in Hdd_status.split():
        if not word in ["Status", "OK"]:
            ctypes.windll.user32.MessageBoxW(None, u"ALERT: HDD ERROR", u"ERROR CONTACT ADMIN NOW !", 0)
            send_mail("Warning HDD not SAFE !","Windows claims About unsafe HDD !")
    return Hdd_status

def get_free_space():
    """ Test first Drive Free space then alert < LIMIT_HDD_FREE_SPACE """
    free_space = round(int(os.popen("wmic logicaldisk get freespace").read().split()[1])/1024/1024/1024)
    if free_space < LIMIT_FREE_HDD_SPACE :
        ctypes.windll.user32.MessageBoxW(None, u"ALERT: HDD FREE SPACE ERROR", u"ERROR CONTACT ADMIN NOW !", 0)
        msg = "Warning Free space is : " + str(free_space) + "GB"
        send_mail("Warning C: Free SPACE !",msg)
    return free_space

def whois_log():
    """ Get user Login name and alert if not in AUTHORIZE_USER list """
    if not os.getlogin() in  AUTHORIZE_USER :
        msg = "SUSPECT Login IN : " + os.getlogin()
        send_mail("SUSPECT LOGIN",msg)
    
def send_mail(subject,message):
    subject = str(subject)
    message = str(message)
    server = smtplib.SMTP(SMTPSERV,25) # 587 for STARTLS
    server.ehlo()
    #server.starttls() # Un comment for use STARTTLS
    server.login(USER, PWD)
    header = 'TO:' + TO + '\n' + 'From: ' + USER + '\n' + 'Subject:'+ HOSTNAME + " | " + IPLAN + " " + subject +'\n'
    mail = header + '\n' + "PC : " + HOSTNAME + " IP LAN : " + IPLAN + "\n" + message + '\n\n'
    server.sendmail(USER, TO, mail )
    server.close()
    
    
    
if __name__ == '__main__':
    # Uncomment for test mail configuration
    #send_mail("Send a Test Mail","1337 Are In place N-pn")
    whois_log()
    get_free_space()
    check_hdd()
