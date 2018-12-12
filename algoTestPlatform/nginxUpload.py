#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests,os
import logging


nginx_logger = logging.getLogger("SeverLogger.nginx")
#os.system("mkdir -p ./logs")
#log_name = "./logs/nginxClient.log"
handler = logging.StreamHandler()
#handler = logging.handlers.RotatingFileHandler(log_name,
 #           maxBytes = 20971520, backupCount = 5)
logging_format = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(logging_format)
nginx_logger.addHandler(handler)
nginx_logger.setLevel(logging.DEBUG)


def nginx_upload_module(): #nginx upload module
    UPLOAD_URL = "http://10.182.8.219:22221/upload"
    file_dir = './hehe/hehe.txt'
    fd = open(file_dir, 'rb')
    files = {'attachment_file': (file_dir, fd, 'hehe.txt', {})}
    r1 = requests.post(UPLOAD_URL, files=files)
    print(r1.text)
    print r1.status_code
    fd.close()

def nginx_upload(filename,filebytes):
    local_root_path = "/export/algorithmTest/algorithmTestData/"
    http_root_path = "http://10.182.42.117:22221/algorithmTestData/"
    http_path = http_root_path + filename
    try:
        local_path = os.path.join(local_root_path,filename)
        filebytes.save(local_path)
        nginx_logger.info("upload success:%s"%http_path)
        return 0, "upload success", http_path
    except Exception,e:
        msg = e.message
        nginx_logger.error("upload failed:%s"%msg)
        return 1, "upload failed:%s" % msg, ""
    

if __name__ == '__main__':
    nginx_upload("sun.jpg",'')
 
