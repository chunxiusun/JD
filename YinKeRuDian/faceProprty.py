#-*- coding:utf-8 -*-

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import time,json,os
import hashlib

imageDir = "e:/sun/pythonCode/YinKeRuDian/biaozhu_data_2668/board_biaozhu_data/"
testOldFile = "e:/sun/pythonCode/YinKeRuDian/biaozhu_data_2668/test_result_old.txt"
testNewFile = "e:/sun/pythonCode/YinKeRuDian/biaozhu_data_2668/test_result_new.txt"
labelFile = "e:/sun/pythonCode/YinKeRuDian/biaozhu_data_2668/label.txt"

#单张图片调用接口，返回算法识别结果
def Query(img):
    #img = "sun1.jpg"
    url = "http://mobile-server.jd.com/api/platform/face/get_face_property.ajax"
    args = {"time":time.time()}
    userName = "1227796546_m"
    userToken = "3skevlvrslanc"
    m1 = hashlib.md5()
    m1.update((userName+userToken).encode("utf-8"))
    newToken = m1.hexdigest()
    m2 = hashlib.md5()
    m2.update((json.dumps(args)+newToken).encode("utf-8"))
    sign = m2.hexdigest()
    register_openers()
    params = dict()
    params["img"] = open(img, "rb")
    params["args"] = json.dumps(args)
    params["username"] = userName
    params["sign"] = sign
    datagen, headers = multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request).read()
    print result.decode("utf-8")
    return json.loads(result)

#读取图片测试集，调用接口，将算法识别结果写入文件
def testResult():
    fw = open(testOldFile,"w")
    for child in os.listdir(imageDir):
        face_property = dict()
        face_property["imgName"] = child
        img = os.path.join(imageDir,child)  
        data = Query(img)
        #print data
        code = data["code"]
        if code == 0:
            if "age" in data["data"]:
                face_property["age"] = data["data"]["age"]
            if "gender" in data["data"]:
                face_property["gender"] = data["data"]["gender"]
        fw.write("%s\n"%json.dumps(face_property))
    fw.close()

#测试结果与标注结果进行比对
def faceProperty():
    #初始化统计数据
    stat = dict()
    stat["totalNum"] = 0
    stat["unidentificationGenderNum"] = 0
    stat["genderCorrectNum"] = 0
    stat["genderErrorNum"] = 0
    stat["unidentificationAgeNum"] = 0
    stat["ageCorrectNum"] = 0
    stat["ageErrorNum"] = 0
    #读取文件生成列表
    with open(labelFile,'r') as f_label:
        label_list = [eval(line.strip()) for line in f_label.readlines()]
    with open(testOldFile,'r') as f_test:
        test_list = [eval(line.strip()) for line in f_test.readlines()]
    #循环遍历标注列表与算法识别结果列表，根据图片名称进行一一比对
    for label_dict in label_list:
        stat["totalNum"] += 1
        label_img_name = label_dict["imgName"]
        for item in label_dict["data"]:
            if item["key"] == "gender":
                label_gender = item["value"]
            if item["key"] == "age":
                label_age = item["value"]
        for test_dict in test_list:
            test_img_name = test_dict["imgName"]
            if test_img_name == label_img_name:
                #比对性别
                if "gender" in test_dict:
                    test_gender = test_dict["gender"]
                    if test_gender == label_gender:
                        stat["genderCorrectNum"] += 1
                    else:
                        stat["genderErrorNum"] +=1
                        #print test_gender,label_gender
                else:
                    stat["unidentificationGenderNum"] += 1
                    stat["genderErrorNum"] += 1
                #比对年龄
                if "age" in test_dict:
                    test_age = test_dict["age"]
                    flag = dealAge(label_age,test_age)#调用年龄比对方法
                    if flag == 0:
                        stat["ageCorrectNum"] += 1
                    else:
                        stat["ageErrorNum"] += 1
                        #print test_age,label_age
                else:
                    stat["unidentificationAgeNum"] += 1
                    stat["ageErrorNum"] += 1
        #break
    print stat
    return stat

#测试结果与标注结果进行比对
def facePropertyNew():
    #初始化统计数据
    stat = dict()
    stat["totalNum"] = 0
    stat["unidentificationNum"] = 0
    stat["genderCorrectNum"] = 0
    stat["genderErrorNum"] = 0
    stat["ageCorrectNum"] = 0
    stat["ageErrorNum"] = 0
    #读取文件生成列表
    with open(labelFile,'r') as f_label:
        label_list = [eval(line.strip()) for line in f_label.readlines()]
    with open(testNewFile,'r') as f_test:
        test_list = [line.strip() for line in f_test.readlines()]
    #循环遍历标注列表与算法识别结果列表，根据图片名称进行一一比对
    for label_dict in label_list:
        stat["totalNum"] += 1
        label_img_name = label_dict["imgName"]
        for item in label_dict["data"]:
            if item["key"] == "gender":
                label_gender = item["value"]
            if item["key"] == "age":
                label_age = item["value"]
        flag = False
        for test_data in test_list:
            test_img_name = test_data.split()[0].split("/")[-1]
            test_age = test_data.split()[1]
            test_gender = test_data.split()[2] #0是女，1是男
            if test_img_name == label_img_name:
                flag = True
                #比对性别
                if (test_gender=="0" and label_gender=="female") or (test_gender=="1" and label_gender=="male"):
                    stat["genderCorrectNum"] += 1
                else:
                    stat["genderErrorNum"] +=1
                    #print test_gender,label_gender
                #比对年龄
                r = dealAge(label_age,test_age)#调用年龄比对方法
                if r == 0:
                    stat["ageCorrectNum"] += 1
                else:
                    stat["ageErrorNum"] += 1
                    #print test_age,label_age
                
        if flag == False:
            stat["unidentificationNum"] += 1
            stat["genderErrorNum"] +=1
            stat["ageErrorNum"] += 1
        #break
    print stat
    return stat

#年龄比对方法
def dealAge(label_age,test_age):
    #label_age:"10-18"or"70-"or"4-7,8-12"
    #test_age:20
    age_list = []
    if "," in label_age:
        age_list = []
        for age_group in label_age.split(","):
            begin = int(age_group.split("-")[0])
            end = int(age_group.split("-")[1])
            age_list.extend(range(begin,end+1))
        if int(test_age) in age_list:
            return 0
        else:
            return 1
    else:
        begin = label_age.split("-")[0]
        end = label_age.split("-")[1]
        if end != "":
            if int(test_age) in range(int(begin),int(end)+1):
                return 0
            else:
                return 1
        else:
            if int(test_age) >= int(begin):
                return 0
            else:
                return 1

if __name__ == '__main__':
    #testResult()
    #result = faceProperty()
    result = facePropertyNew()
    genderAccuracy = result["genderCorrectNum"]*1.0/result["totalNum"]
    ageAccuracy = result["ageCorrectNum"]*1.0/result["totalNum"]
    print "性别正确率:%0.2f%s"%(genderAccuracy*100,"%")
    print "年龄正确率:%0.2f%s"%(ageAccuracy*100,"%")
    
