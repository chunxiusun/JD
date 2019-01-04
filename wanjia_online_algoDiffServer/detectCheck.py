#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json,ast
import copy
import traceback

#init logger
#logger = logging.getLogger("ServerLogger")
#log_name = "server.log"
#handler = logging.StreamHandler()
#logging_format = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#handler.setFormatter(logging_format)
#logger.addHandler(handler)
#logger.setLevel(logging.DEBUG)


class AlgorithmCheck():
    def __init__(self,label_file,test_file):
        self.THRESHOLD = 0.5
        self.label_file = label_file
        self.test_file = test_file
        self.summry_dict = dict()

    def detectionAlgorithm(self,g_list,t_list):
        #logger.info("Begin to recall rate calculation.")
	#g_list = copy.deepcopy(g_list_tmp)
        #t_list = copy.deepcopy(t_list_tmp)
        correct_list = []
        g_num = 0
        no_person = 0
        for g_info in g_list:
	    g_dict = eval(g_info.strip())
	    g_num = g_num + len(g_dict["data"])
	    #image_name = g_dict["imgName"]
	    for t_info in t_list:
                if not len(t_info.strip()):
                    continue
                t_dict = ast.literal_eval(t_info.strip())
	        if t_dict["imgName"] == g_dict["imgName"]:
		    if len(g_dict["data"]) == 0:
		        no_person = no_person + 1
		        continue
		    for groi_tmp in g_dict["data"]:#groi_tmp:{"content":"1","height":704,"width":341,"code":"1","y":343,"x":979}
                        groi = []
                        groi.append(groi_tmp["x"])
                        groi.append(groi_tmp["y"])
                        groi.append(groi_tmp["width"])
                        groi.append(groi_tmp["height"])
		        flag = False
		        dct = {}
		        if len(t_dict["data"]) == 0:
			    continue
		        for troi_tmp in t_dict["data"]:#troi_tmp:[y1,x1,y2,x2]
                            troi = []
                            x = troi_tmp[1]
                            y = troi_tmp[0]
                            w = troi_tmp[3] - troi_tmp[1]
                            h = troi_tmp[2] - troi_tmp[0]
                            troi.append(x)
                            troi.append(y)
                            troi.append(w)
                            troi.append(h)
			    ratio = self.CalRatio(groi,troi)
			    if ratio >= self.THRESHOLD:
			        flag = True
			        dct[str(ratio)] = troi_tmp #有多个符合条件的
		        if flag == True:
			    correct_list.append(groi)
		        if len(dct) == 0:
			    continue
		        else:
			    c_list = sorted(dct.keys(),reverse=True)#相邻人的情况，取ratio最大的，从t_dict["data"]中去除
			    key = c_list[0]
			    t_dict["data"].remove(dct[key])
        #召回率
        if g_num == 0:
	    recall_rate = 0
        else:
	    recall_rate = len(correct_list)*1.0/g_num

        self.summry_dict["imageNum"] = len(g_list)
        self.summry_dict["groundTruthObjectNum"] = g_num
        self.summry_dict["recallRate"] = recall_rate
        self.summry_dict["correctNum"] = len(correct_list)
        print "no person image number:%d"%no_person
        print "groundTruth person number:%d"%g_num
        print "recall rate:%0.2f%s"%(recall_rate*100,"%")
        #准确率
        t_num = self.getTNum(g_list,t_list)
        if t_num == 0:
            precision_rate = 0
        else:
            precision_rate = len(correct_list)*1.0/t_num
        self.summry_dict["testResultObjectNum"] = t_num
        self.summry_dict["precisionRate"] = precision_rate
        print "testResult person number:%d"%t_num
        print "precision rate:%0.2f%s"%(precision_rate*100,"%")
        return recall_rate,precision_rate

    def getTNum(self,g_list,t_list):
        t_num = 0
        for t_info in t_list:
            if not len(t_info.strip()):
                continue
	    t_dict = eval(t_info.strip())
	    t_num = t_num + len(t_dict["data"])
        return t_num

    def CalRatio(self,pos1, pos2):
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

    def Check(self):
        try:
            g_list = self.label_file.readlines()
            self.label_file.close()
            t_list = self.test_file.readlines()
            self.test_file.close()
            recall_rate,precision_rate = self.detectionAlgorithm(g_list,t_list)
            ###F=2* P* R/(P + R)
            if (precision_rate+recall_rate) == 0:
                F_score = 0
            else:
                F_score = 2*precision_rate*recall_rate/(precision_rate+recall_rate)
            self.summry_dict["F_score"] = F_score
            print "F_score:%0.4f"%(F_score)
            return self.summry_dict
        except Exception as e:
            traceback.print_exc()
            return "请检查文件内容！"

if __name__ == '__main__':
    fg = open("labelResult.txt",'r')
    ft = open("algoResult.txt",'r')
    algorithmCheck = AlgorithmCheck(fg,ft)
    summry_dict = algorithmCheck.Check()
    print summry_dict
    
