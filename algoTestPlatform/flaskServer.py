#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, abort, request, jsonify, url_for
import ftpClient
import logging
import logging.handlers
import nginxUpload
from algorithmCheck import AlgorithmCheck

## init log
logger = logging.getLogger("ServerLogger")
#os.system("mkdir -p ./logs")
#log_name = "./logs/ftpClient.log"
#logging.basicConfig(level=logging.DEBUG,
 #          #format='[%(asctime)s %(name)s %(levelname)s] %(message)s',
  #         format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
           #datefmt='%Y-%m-%d %H:%M:%S',
   #        filename=log_name,
    #       filemode='aw')
#handler = logging.handlers.RotatingFileHandler(log_name,
 #           maxBytes = 20971520, backupCount = 5)
handler = logging.StreamHandler()
logging_format = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(logging_format)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
#logger.propagate = True


app = Flask(__name__)

@app.route('/HelloWorld')
def hello_world():
    return "Hello World!"

@app.route('/nginx/upload',methods=['post'])
def nginx_upload():
    filename = request.values.get('name')
    logger.info("interface params name:%s"%filename)
    filebytes = request.files["file"]#request.values.get('fileBytes')
    logger.info("interface params file:%s"%filebytes)
    if filebytes:
        code,message,img_url = nginxUpload.nginx_upload(filename,filebytes)
        return jsonify({"code": code, "msg":message, "fileUrl":img_url})
    else:
        return jsonify({"code":1, "msg":"文件为空!"})

@app.route('/check/recResult',methods=['get'])
def check_recResult():
    process_id = request.values.get('processId')
    algorithmCheck = AlgorithmCheck()
    data = algorithmCheck.recResultCheck(process_id)
    if isinstance(data,str):
        return jsonify({"code": 1, "msg":data})
    else:
        return jsonify({"code": 0, "msg":"success", "data":data})
    


@app.route('/mock',methods=['get'])
def mock():
    data_dict = {"checks": {"type": 2,
                            "label": "data.label",
                            "positive": 6,
                            "negative": 2
                           },
                 "resultTxt": "http://10.182.42.117:22221/algorithmTestData/mock.txt",
                 "code": 0,
                 "msg": "query success"
                }             
    return jsonify(data_dict)




@app.route('/api/ftp_upload',methods=['post'])
def ftp_upload():
    params = request.json
    localpath = params.get('localPath')
    #localpath = request.values.get('localpath')
    logger.info("interface params localPath:%s"%localpath)
    remotepath = params.get('remotePath')
    #remotepath = request.values.get('remotepath')
    logger.info("interface params remotePath:%s"%remotepath)
    operation = 'upload'
    code,message = ftpClient.ftpClient(remotepath,localpath,operation)
    return jsonify({"code": code, "msg":message})

@app.route('/api/ftp_download',methods=['post'])
def ftp_download():
    params = request.json
    localpath = params.get('localPath')
    #localpath = request.values.get('localpath')
    logger.info("interface params localPath:%s"%localpath)
    remotepath = params.get('remotePath')
    #remotepath = request.values.get('remotepath')
    logger.info("interface params remotePath:%s"%remotepath)
    operation = 'download'
    code,message = ftpClient.ftpClient(remotepath,localpath,operation)
    return jsonify({"code": code, "msg":message})

with app.test_request_context():
    print(url_for('ftp_upload'))
    print(url_for('nginx_upload'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=22220, debug=True)

