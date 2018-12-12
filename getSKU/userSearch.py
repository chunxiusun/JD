#-*- coding:utf-8 -*-

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import time,json,os

def userSearch():
    url = "http://172.28.115.38/api/v1/itemFeature_333/search"
    params = dict()
    params["type"] = "user"
    params["topN"] = "10"
    params["userGender"] = "1"
    params["userAge"] = "3"
    params["userPurchPower"] = "2"
    params["userCounty"] = "72"
    params["userMonth"] = "11"
    params["userQuarter"] = "4"
    params["userWeek"] = "4"
    params["dropoutKeepProb"] = "1"
    register_openers()
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request).read()
    print result.decode("utf-8")
    return json.loads(result)

def skuUpload():
    url = "http://172.28.115.38/api/v1/itemFeature_333/upload"
    params = dict()
    params["type"] = "item"
    params["itemSkuId"] = "28712073937"
    params["itemName"] = "健力宝 运动饮料橙蜜味330ml*24罐 整箱装"
    params["itemThirdCate"] = "1602"
    params["itemBrandName"] = "45697"
    params["itemPrice"] = "45"
    params["itemVlume"] = "1.296e+07"
    params["itemWt"] = "8e+06"
    params["dropoutKeepProb"] = "1"
    register_openers()
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request).read()
    print result.decode("utf-8")
    return json.loads(result)


if __name__ == '__main__':
    #userSearch()
    skuUpload()
