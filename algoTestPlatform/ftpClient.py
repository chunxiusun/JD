#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import datetime,time
import logging
import logging.handlers
from ftplib import FTP

ftpServer = "10.182.8.219"
ftpPort = 22220
ftpUser = "qmartqa"
ftpPasswd = "qmartqa"

ftp_logger = logging.getLogger("SeverLogger.ftp")
#os.system("mkdir -p ./logs")
#log_name = "./logs/ftpClient.log"
handler = logging.StreamHandler()
#handler = logging.handlers.RotatingFileHandler(log_name,
 #           maxBytes = 20971520, backupCount = 5)
logging_format = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(logging_format)
ftp_logger.addHandler(handler)
ftp_logger.setLevel(logging.DEBUG)

#def ftpClient(host, username, password):
def ftpClient(remotepath,localpath,operation):
    ftp = FTP()
    #ftp.set_debuglevel(2)
    try:
        ftp.connect(ftpServer, ftpPort)
    except Exception,e:
        return 1,"connect ftpServer failed"
    try:
        ftp.login(ftpUser, ftpPasswd)
    except Exception,e:
        ftp.quit
        return 1,"user login failed"
    try:
        if operation == "upload":
            uploadfile(ftp, remotepath, localpath)
        elif operation == "download":
            downloadfile(ftp, remotepath, localpath)
        ftp.quit
        return 0,"%s success" % operation
    except Exception,e:
        return 1,"%s failed,%s" % (operation,e.message)

def uploadfile(ftp, remotepath, localpath):
    pwd_path = ftp.pwd()
    #ftp_logger.info("Current path:%s" % pwd_path)
    uploadpath = os.path.join(pwd_path,remotepath)
    ftp_logger.info("Upload Path:%s" % uploadpath)
    #all_dir = ftp.dir()
    try:
        ftp_logger.info("Create directory:%s" % uploadpath)
        ftp.mkd(uploadpath)
    except Exception,e:
        msg = "Directory already exists:%s" % uploadpath
        ftp_logger.info(msg)
        #ftp.cwd(uploadpath)

    if os.path.isdir(localpath):
        for parent in os.listdir(localpath):
            child = os.path.join(localpath,parent)
            if os.path.isdir(child):
                sub_remotepath = os.path.join(remotepath,parent)
                uploadfile(ftp, sub_remotepath, child)
            else:
                upload(ftp, uploadpath, child)
    else:
        upload(ftp, uploadpath, localpath)

def downloadfile(ftp, remotepath, localpath):
    if not os.path.exists(localpath):
        ftp_logger.info("Directory does not exist,Create directory:%s"%localpath)
        os.system("mkdir -p %s"%localpath)

    pwd_path = ftp.pwd()
    downloadpath = os.path.join(pwd_path,remotepath)
    ftp_logger.info("Download Path:%s" % downloadpath)
    file_list = ftp.nlst(downloadpath)
    if len(file_list) == 0:
        msg = "Wrong directory or the directory is empty:%s"%downloadpath
        ftp_logger.info(msg)
    for parent in file_list:
        if "." not in parent.split("/")[-1]:
            child = parent.split(downloadpath)[-1]
            sub_localpath = os.path.join(localpath,child)
            sub_remotepath = os.path.join(remotepath,child)
            downloadfile(ftp, sub_remotepath, sub_localpath)
        else:
            download(ftp, parent, localpath)

def upload(ftp, remotepath, localpath):
    file_name = localpath.split("/")[-1]
    file_path = os.path.join(remotepath,file_name)
    try:
        bufsize = 1024
        fp = open(localpath, 'rb')
        ftp.storbinary('STOR ' + file_path, fp, bufsize)
        fp.close()
    except Exception,e:
        msg = "Upload Failed:%s %s" % (localpath,e.message)
        ftp_logger.info(msg)

def download(ftp, remotepath, localpath):
    file_name = remotepath.split("/")[-1]
    file_path = os.path.join(localpath,file_name)
    try:
        bufsize = 1024
        fp = open(file_path, 'wb')
        ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        ftp.set_debuglevel(0)
        fp.close()
    except Exception,e:
        msg = "Download Failed:%s %s" % (file_path,e.message)
        ftp_logger.info(msg)

if __name__ == "__main__":
    #ftpClient("sunsun/","/export/sun/FlaskServer/hehe","upload")
    ftpClient("sun/sun1.jpg","/export/sun/FlaskServer/hello","download")
