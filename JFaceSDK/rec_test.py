#!/usr/bin/python
#-*-coding:utf-8-*-

import numpy

threshold = 0.684

def algoRec():
    #初始化统计数据
    totalCount = 0
    correctCount = 0

    featureTest = "featureTest.txt"
    featureLibrary = "featureLibrary.txt"
    with open(featureTest,'r') as f_test:
        test_list = f_test.readlines()
    with open(featureLibrary,'r') as f_library:
        library_list = f_library.readlines()
    for test_f in test_list:
        totalCount += 1
        test_feature_dict = eval(test_f.strip())
        test_key = test_feature_dict.keys()[0]
        print "#"*10 + test_key + "#"*10
        test_feature = test_feature_dict[test_key]
        cos_dict = dict()
        for library_f in library_list:
            library_feature_dict = eval(library_f.strip())
            library_key = library_feature_dict.keys()[0]
            library_feature = library_feature_dict[library_key]
            cos = cosineSimilarity(test_feature,library_feature)
            cos_dict[cos] = library_key
            #test_name = dealString(test_key)
            #top1_name = dealString(library_key)
            #if test_name == top1_name:
             #   print test_key,library_key,cos
            #break
        c_list = sorted(cos_dict.keys(),reverse=True)#根据key降序排序
        #print c_list
        top1_key = c_list[0]
        top1 = cos_dict[top1_key]
        print "计算结果:",test_key,top1,top1_key
        if top1_key >= threshold:
            print "大于阈值:",test_key,top1,top1_key
            test_name = dealString(test_key)
            top1_name = dealString(top1)
            if test_name == top1_name:
                correctCount += 1
        #break
    print totalCount,correctCount 
            

def cosineSimilarity(test_feature,library_feature):
    t_sum = 0.0
    l_sum = 0.0
    tl_sum = 0.0
    for i in range(len(test_feature)):
        t_sum += numpy.square(test_feature[i])#求平方和
        l_sum += numpy.square(library_feature[i])
        tl_sum += test_feature[i]*library_feature[i]
    t_sqrt = numpy.sqrt(t_sum)#求平方根
    l_sqrt = numpy.sqrt(l_sum)
    #print tl_sum,t_sqrt,l_sqrt
    cos = tl_sum*1.0/(t_sqrt*l_sqrt)
    cos = 0.5 + (0.5*cos)
    #print cos
    return cos

def dealString(img_name):
    lst = img_name.split("_")
    new_name = "_".join(lst[:len(lst)-1])
    #print new_name
    return new_name

def processData():
    originFeature = "feature.txt"
    testFeature = "featureTest.txt"
    f_library = open("featureLibrary.txt","w")
    with open(testFeature,"r") as f_test:
        test_list = f_test.readlines()
    with open(originFeature,"r") as f_f:
        feature_list = f_f.readlines()
    print len(feature_list)
    for feature in test_list:
        feature_list.remove(feature)
    print len(feature_list)
    for feature in feature_list:
        f_library.write(feature) 
    f_library.close()
    f_test.close()

def tmp():
    totalCount = 0
    correctCount = 0
    with open("tmp.txt",'r') as fd:
        cos_list = fd.readlines()
    for item in cos_list:
        totalCount += 1
        test_img = item.strip().split()[1]
        top1_img = item.strip().split()[2]
        cos = eval(item.strip().split()[3])
        cos = 0.5 + (0.5*cos)
        #print test_img,top1_img,cos
        if cos >= threshold:
            test_name = dealString(test_img)
            top1_name = dealString(top1_img)
            if test_name == top1_name:
                correctCount += 1
            else:
                print test_img,top1_img,cos
    print totalCount,correctCount


if __name__ == '__main__':
    #processData()
    algoRec()
    #tmp()    
