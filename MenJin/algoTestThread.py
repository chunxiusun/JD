#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,time
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import threading

class algoTest(threading.Thread):
    def __init__(self,imgList,threadNum):
        threading.Thread.__init__(self)
        self.imgList = imgList
        self.threadNum = threadNum

    def search(self,img):
        url = "http://172.28.115.38:80/api/v1/menjin_multi_base_g2/search"
        #img = "/export/sun/MenJin/face_val/jfs_t30529_242_1028961700_40014_d156596_5c05f3f7N1bf348b6.jpg"
        #register_openers()
        #datagen, headers = multipart_encode({'img': open(img,'rb')})
        #request = urllib2.Request(url, datagen, headers)
        #resp = urllib2.urlopen(request).read()
        #print resp
        #data = eval(resp)
        data = {"code":0,"data":[{"key":"123","score":45}]}
        return data

    def batchSearch(self):
        imgDir = "/export/sun/MenJin/face_val/"
        result_lst = []
        error_lst = []
        for line in self.imgList:
            im = line.strip().split('\t')[1]
            print im
            img = os.path.join(imgDir,im)
            data_dict = self.search(img)
            if data_dict["code"] == 0:
                erp = data_dict["data"][0]["key"]
                score = data_dict["data"][0]["score"]
                info = "%s\t%s\t%s\n"%(line.strip(),erp,score)
                #print info
                result_lst.append(info)
            else:
                info = "%s\n"%data_dict
                error_lst.append(info)
            #break
        ResultThreadDict[self.threadNum] = result_lst
        ErrorThreadDict[self.threadNum] = error_lst
        

    def run(self):
        self.batchSearch()

def main():
    global ResultThreadDict,ErrorThreadDict

    threadNum = 1

    ResultThreadDict = dict()
    ErrorThreadDict = dict()

    with open("../face_val.list","r") as fd:
        lst = fd.readlines()
    
    n = len(lst)/threadNum
    query_list = []
    for i in range(threadNum):
        if i == threadNum-1:
            print i*n
            t = algoTest(lst[i*n:len(lst)],i)
        else:
            print i*n
            t = algoTest(lst[i*n:i*n+n],i)
        query_list.append(t)

    for i in range(threadNum):
        query_list[i].start()

    FLAG = True
    while FLAG:
        time.sleep(5)
        f = 0
        for thread in ResultThreadDict:
            if len(ResultThreadDict[thread]) == 0:
                f = 1
                break
        if f == 0:
            FLAG = False
    
    f_result = open("result.txt",'w')
    f_error = open("error.txt",'w')
    for i in range(threadNum):
        for line in ResultThreadDict[i]:
            if len(line) != 0:
                f_result.write(line)
        for line in ErrorThreadDict[i]:
            if len(line) != 0:
                f_error.write(line)
    f_result.close()
    f_error.close()

if __name__ == '__main__':
    main()
