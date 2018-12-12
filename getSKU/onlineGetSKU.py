#-*- coding:utf-8 -*-

#接口cf：https://cf.jd.com/pages/viewpage.action?pageId=132106994

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import time,json,os
import hashlib
import requests

def onlineGetSKU():
    url = "http://mobile-server.jd.com/api/platform/material/find_recommend_info.ajax"
    args = dict()
    args["time"] = time.time()
    args["deviceUuid"] = "bfdf104bd7b8056ebcbd839760e0e1cd"#"c801b5f57f3361b7bd80647e6b9e1de4"
    args["age"] = 40
    args["gender"] = 1
    args["pin"] = "1227796546_m"
    #print args
    userName = "1227796546_m"
    userToken = "3skevlvrslanc"
    m1 = hashlib.md5()
    m1.update((userName+userToken).encode("utf-8"))
    newToken = m1.hexdigest()
    m2 = hashlib.md5()
    m2.update((json.dumps(args)+newToken).encode("utf-8"))
    sign = m2.hexdigest()
    #print sign

    register_openers()
    params = dict()
    params["args"] = json.dumps(args)
    params["username"] = userName
    params["sign"] = sign
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request).read()
    print result.decode("utf-8")
    return json.loads(result)

def analyzeSKU():
    data = onlineGetSKU()
    code = data["code"]
    if code != 0:
        print code
        print data["msg"]
        return
    sku_list = data["data"]["skuList"]
    for sku in sku_list:
        sku_id = sku["sku"]
        print sku_id

if __name__ == '__main__':
    #onlineGetSKU()
    analyzeSKU()
