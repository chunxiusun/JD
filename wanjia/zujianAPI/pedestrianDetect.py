#coding:utf-8

import requests,json,time,os
import hashlib
import cv2
import copy

THRESHOLD = 0.5

def recallRate(g_list_tmp,t_list_tmp):
    g_list = copy.deepcopy(g_list_tmp)
    t_list = copy.deepcopy(t_list_tmp)
    
    recall_list = []
    g_num = 0
    no_person = 0
    for g_info in g_list:
        g_dict = eval(g_info)
        g_num = g_num + len(g_dict["data"])
        #image_name = g_dict["imgName"]
        for t_info in t_list:
            t_dict = eval(t_info)
            if t_dict["imgName"] == g_dict["imgName"]:
                if len(g_dict["data"]) == 0:
                    no_person = no_person + 1
                    continue
                for groi in g_dict["data"]:
                    flag = False
                    dct = {}
                    if len(t_dict["data"]) == 0:
                        continue
                    for troi in t_dict["data"]:
                        ratio = CalRatio(groi,troi)
                        if ratio >= THRESHOLD:
                            flag = True
                            dct[str(ratio)] = troi #有多个符合条件的
                    if flag == True:
                        recall_list.append(groi)
                    if len(dct) == 0:
                        continue
                    else:
                        c_list = sorted(dct.keys(),reverse=True)#相邻人的情况，取ratio最大的，从t_dict["data"]中去除
                        key = c_list[0]
                        t_dict["data"].remove(dct[key])
    if g_num == 0:
        recall_rate = 0
    else:
        recall_rate = len(recall_list)*1.0/g_num
    print "no person image number:%d"%no_person
    print "groundTruth person number:%d"%g_num
    print "recall rate:%0.2f%s"%(recall_rate*100,"%")
    return recall_rate

def precisionRate(g_list_tmp,t_list_tmp):
    g_list = copy.deepcopy(g_list_tmp)
    t_list = copy.deepcopy(t_list_tmp)
    
    precision_list = []
    t_num = 0
    for t_info in t_list:
        t_dict = eval(t_info)
        t_num = t_num + len(t_dict["data"])
        for g_info in g_list:
            g_dict = eval(g_info)
            if g_dict["imgName"] == t_dict["imgName"]:
                if len(t_dict["data"]) == 0:
                    continue
                for troi in t_dict["data"]:
                    flag = False
                    dct = {}
                    if len(g_dict["data"]) == 0:
                        continue
                    for groi in g_dict["data"]:
                        ratio = CalRatio(groi,troi)
                        if ratio >= THRESHOLD:
                            flag = True
                            dct[str(ratio)] = groi #有多个符合条件的
                    if flag == True:
                        precision_list.append(troi)
                    if len(dct) == 0:
                        continue
                    else:
                        c_list = sorted(dct.keys(),reverse=True)#相邻人的情况，取ratio最大的，从g_dict["data"]中去除
                        key = c_list[0]
                        g_dict["data"].remove(dct[key])
    if t_num == 0:
        precision_rate = 0
    else:
        precision_rate = len(precision_list)*1.0/t_num
    print "testResult person number:%d"%t_num
    print "precision rate:%0.2f%s"%(precision_rate*100,"%")
    return precision_rate

def CalRatio(pos1, pos2):
    ratio = 0.0
    x1 = float(pos1[0])
    x2 = float(pos2[0])
    y1 = float(pos1[1])
    y2 = float(pos2[1])
    width1 = float(pos1[2])
    width2 = float(pos2[2])
    height1 = float(pos1[3])
    height2 = float(pos2[3])

    startx = min(x1, x2)
    endx = max(x1+width1, x2+width2)
    width = width1 + width2 - (endx - startx)

    starty = min(y1, y2)
    endy = max(y1+height1, y2+height2)
    height = height1 + height2 - (endy - starty)

    if (width <= 0) or (height <= 0):
        ratio = 0.0
    else:
        area = width * height
        area1 = width1 * height1
        area2 = width2 * height2
        ratio = area*1.0 / (area1 + area2 - area)
    return ratio

def pedestrianDetect(testImage):
    url = "https://face-server.jd.com/api/face/url_area_detect.ajax"
    testImage = "http://10.182.8.16:22888/img/wanjia/testSet20180906/210235T85E3185000003-20180906172024.jpeg"
    userName = "1227796546_m"
    userToken = "3skevlvrslanc"
    appToken = "4u8o1n4nb5ih"
    args={"time":time.time(),"username":userName,"appSecret":"6k50im2cueqd5","token":appToken,"img":testImage} 
    m1 = hashlib.md5()
    m1.update((userName+userToken).encode("utf-8"))
    newToken = m1.hexdigest()
    m2 = hashlib.md5()
    m2.update((json.dumps(args)+newToken).encode("utf-8"))
    sign = m2.hexdigest()
    params = {}
    params["args"] = json.dumps(args)
    params["sign"] = sign
    params["username"] = userName
    r = requests.get(url,params=params)
    httpCode = r.status_code
    print httpCode
    data = json.loads(r.text)
    print r.text
    person_list = []
    if not data.has_key("data"):
        return person_list
    image_name = testImage.split("/")[-1]
    if data["data"].has_key("faceList"):
        personList = data["data"]["faceList"]
        for person in personList:
            cutboard_list = []
            t_roi = person["rect"]#y1,x1,y2,x2
            x = t_roi[1]
            y = t_roi[0]
            w = t_roi[3] - t_roi[1]
            h = t_roi[2] - t_roi[0]
            cutboard_list.append(x)
            cutboard_list.append(y)
            cutboard_list.append(w)
            cutboard_list.append(h)
            person_list.append(cutboard_list)
    return person_list

def formatTestResult():
    ft_person = open("t_person.txt",'w+')
    imagePath = u"E:/sun/项目/万家项目/testSet/testSet20180906v2"
    imageList = os.listdir(imagePath)
    for image in imageList:
        pedestrian_dict = {}
        pedestrian_dict["imgName"] = image
        pedestrian_dict["type"] = "pedestrian"
        httpImage = "http://10.182.8.16:22888/img/testSet20180906/"+image
        person_list = pedestrianDetect(httpImage)
        if len(person_list) == 0:
            print "no person"
        pedestrian_dict["data"] = person_list
        ft_person.write("%s\n"%json.dumps(pedestrian_dict))
    ft_person.close()


def formatGroundTruth():
    fg_person = open("g_person.txt",'w+')
    labelFile = "E:/sun/pythonCode/wanJia/label-20180906.txt"
    f_label = open(labelFile,'r')
    for line in f_label.readlines():
        info_dict = eval(line.strip())
        pedestrian_dict = {}
        pedestrian_dict["imgName"] = info_dict["imgName"]
        pedestrian_dict["type"] = "pedestrian"
        print pedestrian_dict["imgName"]
        pedestrian_list = []
        person_list = info_dict["data"]
        if len(person_list) != 0:
            for person in person_list:
                cutboard_list = []
                cutboard_list.append(person["x"])
                cutboard_list.append(person["y"])
                cutboard_list.append(person["width"])
                cutboard_list.append(person["height"])
                pedestrian_list.append(cutboard_list)
        pedestrian_dict["data"] = pedestrian_list
        fg_person.write("%s\n"%json.dumps(pedestrian_dict))
    f_label.close()
    fg_person.close()

def drawRoi(g_list,t_list):
    image_path = "E:/sun/pythonCode/wanJia/testSet20180906v2/"
    result_path = "E:/sun/pythonCode/wanJia/testResult20180906v2/"

    for g_info in g_list:
        g_dict = eval(g_info)
        image_name = g_dict["imgName"]
        #print image_name
        image = image_path + image_name
        print image
        im = cv2.imread(image)
        im_copy = im.copy()
        flag = False
        if len(g_dict["data"]) != 0:
            flag = True
            for g_roi in g_dict["data"]:
                x = g_roi[0]
                y = g_roi[1]
                x1 = g_roi[0] + g_roi[2]
                y1 = g_roi[1] + g_roi[3]
                cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)#red
        for t_info in t_list:
            t_dict = eval(t_info)
            if t_dict["imgName"] == g_dict["imgName"]:
                if len(t_dict["data"]) != 0:
                    flag = True
                    for t_roi in t_dict["data"]:
                        x = t_roi[0]
                        y = t_roi[1]
                        x1 = t_roi[0] + t_roi[2]
                        y1 = t_roi[1] + t_roi[3]
                        cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,255,0),3)#green
            
        if flag == True:
            cv2.imwrite("%s/%s"%(result_path,image_name), im_copy)
        #break

if __name__ == '__main__':
    pedestrianDetect("hehe")
    #formatGroundTruth()
    #formatTestResult()
    #with open("g_person.txt",'r') as fg:
       # g_list = fg.readlines()
    #with open("t_person_non.txt",'r') as ft:
     #   t_list = ft.readlines()
    #recall_rate = recallRate(g_list,t_list)
    #precision_rate = precisionRate(g_list,t_list)
    ###F=2* P* R/(P + R)
    #F_score = 2*precision_rate*recall_rate/(precision_rate+recall_rate)
    #print "F_score:%0.4f"%(F_score)
    #drawRoi(g_list,t_list)
     
    
