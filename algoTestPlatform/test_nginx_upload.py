#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests,json

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

def test_upload():
    url = "http://10.182.42.117:22220/api/nginx_upload"
    fd = open('sun1.jpg','rb')
    print type(fd)
    file_data = fd.read()
    print type(file_data)
    data = {'fileName':'sun1.jpg','fileBytes':file_data}
    r = requests.post(url,data=data)
    print r.status_code
    print r.text
    fd.close()

def test_wanjia():
    url = "http://172.20.141.77:22222/check/detectResult"
    register_openers()
    params = {'labelFile': open("/export/sun/WANJIA/label-20180906.txt", "rb"), 'testFile': open("/export/sun/WANJIA/t_person.txt","rb")}
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request).read()
    print result.decode("utf-8")
    print json.loads(result)

if __name__ == '__main__':
    #test_upload()
    test_wanjia()
