#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests,json,time,json,os
import csv


def userSearch():
    #url = "http://172.28.115.38/api/v1/itemFeature_333/search"
    url = "http://172.28.115.38:80/commidity/recommend"
    params = dict()
    params["appId"] = "100001"
    params["token"] = "0aebdee6-b74b-45aa-acd3-c4ddac8e26dd"
    storeInfo = dict()
    storeInfo["storeId"] = "itemFeature_123"#业务名
    storeInfo["limit"] = "400"
    storeInfo["type"] = "item"
    storeInfo["itemSkuId"] = "1887518"
    storeInfo["itemName"] = "闪迪（SanDisk）64GB CF（CompactFlash）存储卡 UDMA7 4K 至尊超极速版 读速160MB/s 写速150MB/s"
    storeInfo["itemThirdCate"] = "845"
    storeInfo["itemBrandName"] = "15341"
    storeInfo["itemPrice"] = "679.0"
    storeInfo["itemVlume"] = "253.792"
    storeInfo["itemWt"] = "0.034"
    storeInfo["dropoutKeepProb"] = "1"
    storeInfo["baseBusiness"] = "allFeature"
    storeInfo["baseTopN"] = "3"
    storeInfo["storeTopN"] = "3"
    params["storeInfo"] = json.dumps(storeInfo)
    start = (time.time())*1000
    r = requests.post(url,data=json.dumps(params))
    end = (time.time())*1000
    #print r.status_code
    #print r.content
    print "搜索耗时：%d ms"%int((end - start))
    data = json.loads(r.content)
    sku_list = data["data"]
    #for sku in sku_list:
     #   print sku["key"]
    #print len(sku_list)

def skuUpload(itemSkuId,itemName,itemThirdCate,itemBrandName,itemPrice,itemVlume,itemWt):
    #url = "http://172.28.115.38/api/v1/itemFeature_333/upload"
    url = "http://172.28.115.38:80/commidity/upload"
    params = dict()
    params["appId"] = "100001"
    params["token"] = "0aebdee6-b74b-45aa-acd3-c4ddac8e26dd"
    storeInfo = dict()
    storeInfo["storeId"] = "itemFeature_123"
    storeInfo["type"] = "item" #特征类型 eg:"item"
    storeInfo["itemSkuId"] = itemSkuId #"1887518"
    storeInfo["itemName"] = itemName #"闪迪（SanDisk）64GB CF（CompactFlash）存储卡 UDMA7 4K 至尊超极速版 读速160MB/s 写速150MB/s"
    storeInfo["itemThirdCate"] = itemThirdCate #"845"
    storeInfo["itemBrandName"] = itemBrandName #"15341"
    storeInfo["itemPrice"] = itemPrice #"679.0"
    storeInfo["itemVlume"] = itemVlume #"253.792"
    storeInfo["itemWt"] = itemWt #"0.034"
    storeInfo["dropoutKeepProb"] = "1"
    params["storeInfo"] = json.dumps(storeInfo)
    start = (time.time())*1000
    r = requests.post(url,data=json.dumps(params))
    end = (time.time())*1000
    print "上传耗时：%d ms"%int(end-start)
    #print r.status_code
    #print r.content

def skuUploadBatch():
    csvFile = "take_recommend_spu_2018_12_10.csv"
    count = 0
    with open(csvFile) as f:
        reader = csv.DictReader(f)
        #head_row = next(reader)
        for row in reader:
            itemSkuId = row["main_sku_id"]
            itemName = row["item_name"]
            itemThirdCate = row["item_third_cate_cd"]
            itemBrandName = row["brand_cd"]
            itemPrice = row["sku_jd_prc"]
            itemVlume = row["volume"]
            itemWt = row["wt"]
            #print itemName
            skuUpload(itemSkuId,itemName,itemThirdCate,itemBrandName,itemPrice,itemVlume,itemWt)
            count += 1
            if count == 1:
                break


if __name__ == '__main__':
    userSearch()
    skuUploadBatch()
