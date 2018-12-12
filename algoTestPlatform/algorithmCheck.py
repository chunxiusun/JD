#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,requests,json,logging
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2


#配置logger
algorithm_logger = logging.getLogger("SeverLogger.algorithm")
#os.system("mkdir -p ./logs")
#log_name = "./logs/nginxClient.log"
handler = logging.StreamHandler()
#handler = logging.handlers.RotatingFileHandler(log_name,
 #           maxBytes = 20971520, backupCount = 5)
logging_format = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(logging_format)
algorithm_logger.addHandler(handler)
algorithm_logger.setLevel(logging.DEBUG)

class AlgorithmCheck():
    def __init__(self):
        self.check_url = "http://10.182.42.117:22220/mock"
        self.process_detail_url = "http://q.j.jd.com/process/detail" #"http://10.182.8.72:22333/process/detail"
        self.filepath = "/export/sun/FlaskServer/tmp/"
        self.upload_url = "http://10.182.42.117:22220/nginx/upload"

    #调用获取验证信息接口/process/detail?pid=xxxx
    def Query(self,process_id):
        try:
            params = {"pid":process_id}
            r = requests.get(self.process_detail_url,params=params)
            #r = requests.get(self.check_url)
        except Exception,e:
            algorithm_logger.error(e.message)
            #return e.message
            return "获取验证信息失败！"
        http_code = r.status_code
        algorithm_logger.info("(API:/process/detail?pid=%s)The return code for the HTTP request is %d"%(process_id,http_code))
        if http_code != 200:
            #return "The return code for the HTTP request is %d"%(http_code)
            return "获取验证信息失败！"
        #print r.content
        algorithm_logger.info(r.content)
        diff_info = json.loads(r.content)
        code = diff_info["code"]
        algorithm_logger.info("(API:/process/detail?pid=%s)The interface return code is %d"%(process_id,code))
        if code != 0:
            return "获取验证信息失败！"
            #return "The interface return code is %d"%code
        analysis_info = {}
        analysis_info["resultTxt"] = diff_info["value"]["file"]
        analysis_info["type"] = int(diff_info["value"]["type"]) #type:1表示识别结果类，2表示识别阈值类
        analysis_info["positive"] = int(diff_info["value"]["positive"])
        if analysis_info["type"] == 1:
            analysis_info["negative"] = int(diff_info["value"]["negtive"])
        analysis_info["label"] = diff_info["value"]["field"]
        algorithm_logger.info("Authentication information:%s"%json.dumps(analysis_info))
        print analysis_info
        return analysis_info

    def recResultCheck(self,process_id):
        #初始化统计数据
        result = dict()
        stat = dict()
        stat["totalCase"] = 0
        stat["badDataCase"] = 0
        stat["passCase"] = 0
        stat["badCase"] = 0
        query_result = self.Query(process_id)
        if not isinstance(query_result,dict):
            return query_result
        resultTxt = query_result["resultTxt"]
        ty = query_result["type"]
        positive = query_result["positive"]
        if ty == 1:
            negative = query_result["negative"]
        label = query_result["label"]
        #deal file
        try:
            #pass
            os.system("wget -P %s %s"%(self.filepath,resultTxt))
        except Exception,e:
            algorithm_logger.error("Download failed,file:%s,message:%s"%(resultTxt,e.message))
            return "Download failed,file:%s,message:%s"%(resultTxt,e.message)
        filename = resultTxt.split("/")[-1]
        origin_file = os.path.join(self.filepath,filename)
        bad_data_file = os.path.join(self.filepath,"%s_bad_data.txt"%filename.split(".")[0])
        bad_file = os.path.join(self.filepath,"%s_bad.txt"%filename.split(".")[0])
        f_bad_data = open(bad_data_file,'w')
        f_bad = open(bad_file,'w')
        try:
            fd = open(origin_file,'r')
        except Exception,e:
            algorithm_logger.error("Read file failed:%s"%filename)
            return "Read file failed:%s"%filename
        for line in fd.readlines():
            stat["totalCase"] += 1
            try:
                algorithm_result = eval(line.strip().split("___HOLD___")[2])
            except Exception,e:
                stat["badDataCase"] += 1
                f_bad_data.write(line)
                #print e.message
                continue
            code = algorithm_result["code"]
            if code != 0:
                stat["badDataCase"] += 1
                f_bad_data.write(line)
                continue
            keys = label.split('.')
            tmp_data = algorithm_result
            try:
                for item in keys:
                    tmp_data = tmp_data[item]
            except Exception,e:
                stat["badDataCase"] += 1
                f_bad_data.write(line)
                continue
            except_result = line.strip().split("___HOLD___")[1]
            if ty == 1:
                if (eval(except_result)==1 and tmp_data==positive) or (eval(except_result)==0 and tmp_data==negative):
                    stat["passCase"] += 1
                else:
                    stat["badCase"] += 1
                    f_bad.write(line)
            elif ty == 2:
                if (eval(except_result)==1 and tmp_data>=positive) or (eval(except_result)==0 and tmp_data<positive):
                    stat["passCase"] += 1
                else:
                    stat["badCase"] += 1
                    f_bad.write(line)
        f_bad_data.close()
        f_bad.close()
        fd.close()
        #将文件上传到httpServer，只上传和返回有内容的
        if stat["badDataCase"] != 0:
            upload_bad_data_file = self.fileUpload(bad_data_file)
            result["badDataFile"] = upload_bad_data_file
        if stat["badCase"] != 0:
            upload_bad_file = self.fileUpload(bad_file)
            result["badFile"] = upload_bad_file
        #删掉临时目录
        os.system("rm -r %s"%self.filepath)
        result["summary"] = stat
        algorithm_logger.info("The final result:%s"%json.dumps(result))
        print result
        return result
        

    def recThresholdCheck(self):
        pass

    #调用上传文件接口
    def fileUpload(self,filepath):
        filename = filepath.split("/")[-1]
        opener = register_openers()
        params = {'file': open(filepath, "rb"), 'name': filename}
        datagen, headers = multipart_encode(params)
        request = urllib2.Request(self.upload_url, datagen, headers)
        result = urllib2.urlopen(request).read()
        data = json.loads(result)
        if data["code"] == 0:
            file_url = data["fileUrl"]
            algorithm_logger.info("Upload file:%s"%file_url)
            #print file_url
            return file_url
        else:
            self.fileUpload(filepath)


if __name__ == '__main__':
    algorithmCheck = AlgorithmCheck()
    algorithmCheck.recResultCheck(84)
