#!/usr/bin/python3.5

import requests
import sys
import time
import smtplib
import shelve
import hashlib
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests.exceptions import HTTPError

urlList = ['http://','http://','https://',''] # Domains being monitored
dbfilename = 'domainVerify.db'
db = {}
dbDomains = []

def veriPyDomain(urlList):
  for url in urlList:
   try:
    r = requests.get(url, timeout=10)
    if r.status_code:
     hashO = hashlib.md5(r.content)
     hashObj = hashO.hexdigest()
     domLis = [url, r.status_code, hashObj]
     dbDomains.append(domLis)
   except requests.exceptions.RequestException as e:
    errData = {'Domain': '%s'%url, 'Error':'%s'%e}
    db[str(time.asctime().split()[3])] = errData
    storeDbase(db)
  return dbDomains

def smtpSender(sites):
  sender = "" #Email account from which alert is gonna be sent
  receiver = ["",""]#Email recipients
  try:
      msg = MIMEMultipart('alternative')
      msg['Subject'] = "Alert - Domain"
      msg['From'] = sender
      msg['To'] = ",".join(receiver)
      text = "These domains are responding with HTTP Codes!!\n\n\n%s" %sites
      s = smtplib.SMTP('....')# IP Address or hostname of SMTP server
      part1 = MIMEText(text, 'plain')
      msg.attach(part1)
      s.sendmail(sender, receiver, msg.as_string())
  except smtplib.SMTPException:
      print ("Error: unable to send email")


def storeDbase(dbErro):
  dbfile = open(dbfilename, 'a')
  for timek, value in dbErro.items():
     print(timek,'-->',value, file=dbfile)
     print('/n', file=dbfile)
  dbfile.close()


def save_Db(obj):
  db = shelve.open('fileHash.shelve')
  for (n, value) in obj:
   db[n] = value
  db.close()

def load_Db():
  db = shelve.open('fileHash.shelve')
  return db


if __name__ == '__main__':

   urlL = veriPyDomain(urlList)
   urlU = [[url[0],url[2]] for url in urlL]
   dict_ = dict((key, value) for (key, value) in urlU)
   file = Path('./fileHash.shelve')

   if file.is_file():
    fileHash = load_Db()
    dbLasList = []
    for key in fileHash.keys():
     if key in dict_.keys():
      if not dict_[key] == fileHash[key]:
       dbLasList.append([hash, dict_[hash]])
   else:
     dbSet = urlU
     smtpSender(dbSet)
     save_Db(dbSet)

   if dbLasList:
     dbSet = set(tuple(ite) for ite in dbLasList)
     smtpSender(dbSet)
     save_Db(dbSet)
