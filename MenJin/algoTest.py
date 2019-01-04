#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,time
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import threading

class algoTest:
    def __init__(self,imgList,f_result,f_error):
        self.imgList = imgList
        self.f_result = f_result
        self.f_error = f_error

    def search(self,img):
        url = "http://172.28.115.38:80/api/v1/menjin_multi_base_g2/search"
        #img = "/export/sun/MenJin/face_val/jfs_t1_26940_30_25_15555_5c066c53Ee386d144_1d82b695420a37fb.jpg"
        register_openers()
        datagen, headers = multipart_encode({'img': open(img,'rb')})
        request = urllib2.Request(url, datagen, headers)
        resp = urllib2.urlopen(request).read()
        #print resp
        data = eval(resp)
        if data["code"] == 0:
            return data
        else:
            print resp
            self.f_error.write("%s\n"%resp)
            return 1

    def batchSearch(self,imgDir):
        #imgDir = "/export/sun/MenJin/face_val/"
        lst = []
        for line in self.imgList:
            im = line.strip().split('\t')[1]
            img = os.path.join(imgDir,im)
            data_dict = self.search(img)
            if not isinstance(data_dict,dict):
                continue
            erp = data_dict["data"][0]["key"]
            score = data_dict["data"][0]["score"]
            info = "%s\t%s\t%s\n"%(line.strip(),erp,score)
            #print info
            self.f_result.write(info)
            #break

    def dirty_batchSearch(self,imgDir):
        totalNum = 0
        correctNum = 0
        recallNum = 0
        for line in self.imgList:
            totalNum += 1
            #im = line.strip()
            im = line.strip().split('\t')[0]
            img = os.path.join(imgDir,im)
            #print img
            data_dict = self.search(img)
            if not isinstance(data_dict,dict):
                continue
            correctNum += 1
            erp = data_dict["data"][0]["key"]
            score = data_dict["data"][0]["score"]
            if score > 44:
                recallNum += 1
            info = "%s\t%s\t%s\n"%(line.strip(),erp,score)
            self.f_result.write(info)
        print totalNum,correctNum,recallNum


def runSearch():
    imgDir = "/export/sun/MenJin/face_val/"
    fd = open("face_val.list","r")
    lst = fd.readlines()
    f_error = open("error.txt",'w')
    f_result = open("result.txt",'w')
    algo_test = algoTest(lst,f_result,f_error)
    algo_test.batchSearch(imgDir)
    f_error.close()
    f_result.close()
    fd.close()

def normalImage(flag):
    if flag == 0: #0表示正常数据，1表示脏数据
        fileName = "result.txt"
    else:
        fileName = "dirty_result_all.txt"
    fd = open(fileName,'r')
    totalNum = 0
    correctNum = 0
    errorNum = 0
    oldCorrectNum = 0
    newCorrectNum = 0
    for line in fd.readlines():
        totalNum += 1
        #print line
        data_list = line.strip().split('\t')
        if len(data_list) < 5:
            errorNum += 1
            continue
        correctNum += 1
        if flag == 0:
            old_erp = data_list[0]
            old_score = eval(data_list[2])
            new_erp = data_list[3]
            new_score = eval(data_list[4])
        else:
            old_erp = data_list[3]
            old_score = eval(data_list[4])
            new_erp = data_list[1]
            new_score = eval(data_list[2])
        if old_score > 44:
            oldCorrectNum += 1
        if flag == 0:
            if new_erp == old_erp and new_score > 41.5:
                newCorrectNum += 1
        else:
            if new_score > 41.5:
                newCorrectNum += 1
    fd.close()
    old = oldCorrectNum*1.0/totalNum
    new = newCorrectNum*1.0/totalNum
    print "totalNum:%d"%totalNum
    print "correctNum:%d"%correctNum
    print "errorNum:%d"%errorNum
    print "oldCorrectNum:%d"%oldCorrectNum
    print "newCorrectNum:%d"%newCorrectNum
    if flag == 0:
        print "正常数据-旧模型准确率:%0.2f%s"%(old*100,"%")
        print "正常数据-新模型准确率:%0.2f%s"%(new*100,"%")
    else:
        print "脏数据-旧模型召回率:%0.2f%s"%(old*100,"%")
        print "脏数据-新模型召回率:%0.2f%s"%(new*100,"%")

def dirty_runSearch():
    imgDir = "/export/sun/MenJin/dirty_face_val/"
    #fd = open("dirty_face_val.list","r")
    fd = open("dirty_result.txt","r")
    lst = fd.readlines()
    f_error = open("dirty_error_old.txt",'w')
    f_result = open("dirty_result_all.txt",'w')
    algo_test = algoTest(lst,f_result,f_error)
    algo_test.dirty_batchSearch(imgDir)
    f_error.close()
    f_result.close()
    fd.close()


if __name__ == '__main__':
    #runSearch()
    #normalImage(0)
    dirty_runSearch()
    #normalImage(1)
