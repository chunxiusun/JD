#-*- coding:utf8 -*-

'''图片画框后保存，需传入图片位置、图片中目标坐标及名称、画框后图片保存路径（可选参数）'''

import os
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont


def drawROI(originImage,objectList,drawDir=".\drawImages"):
    if not os.path.exists(drawDir):
        os.mkdir(drawDir)
    print ("原始图片：%s"%originImage)
    imageName = originImage[originImage.rfind("\\")+1:]
    print ("画框后图片：%s\%s"%(drawDir,imageName))
    im = cv2.imread(originImage)
    im_copy = im.copy()
    #objectList = ["可口可乐:726.23|472.88|792.78|625.91","牛栏山:396.44|368.78|482.33|650.44"] 格式：目标名称:坐标  坐标格式：x|y|x1|y1
    #objectList = ["726.23|472.88|792.78|625.91","396.44|368.78|482.33|650.44"]  格式：坐标
    for obj in objectList:
        if ":" in obj:
            index = obj.find(":")
            objName = obj[:index]
            objBox = obj[index+1:]
        else:
            objName = ""
            objBox = obj
        print (objName,objBox)
        roi = objBox.split("|")
        x = eval(roi[0])
        y = eval(roi[1])
        x1 = eval(roi[2])
        y1 = eval(roi[3])
        cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
        #图片上写中文,OpenCV不支持中文，对图像进行OpenCV格式和PIL格式的相互转换
        img_PIL = Image.fromarray(cv2.cvtColor(im_copy, cv2.COLOR_BGR2RGB))
        font = ImageFont.truetype('simhei.ttf', 20) #字体
        draw = ImageDraw.Draw(img_PIL)
        draw.text((int(x),int(y)-20), objName, font=font, fill=(255,0,255))
        im_copy = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)
    cv2.imwrite("%s\%s"%(drawDir,imageName), im_copy)