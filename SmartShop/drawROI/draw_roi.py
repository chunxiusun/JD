#-*- coding:gbk -*-

import sys,time,datetime
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

fileName = sys.argv[1] #"imagesInfo.txt"
drawDir = sys.argv[2] #"drawImages\"

def drawROI():
    with open(fileName,'r') as fd:
        for line in fd.readlines():
            imageInfo = line.strip().split(",")
            localImage = imageInfo[0]
            print "原始图片：%s"%localImage
            imageName = localImage[localImage.rfind("\\")+1:]
            print "画框后图片：%s\%s"%(drawDir,imageName)
            im = cv2.imread(localImage)
            im_copy = im.copy()
            for sku in imageInfo[1:]:
                if "&" in sku:
                    index = sku.find("&")
                    skuName = sku[:index]
                    skuBox = sku[index+1:]
                else:
                    skuName = ""
                    skuBox = sku
                print skuName,skuBox
                #continue
                roi = skuBox.split("|")
                x = eval(roi[0])
                y = eval(roi[1])
                x1 = eval(roi[2])
                y1 = eval(roi[3])
                cv2.rectangle(im_copy,(int(x),int(y)),(int(x1),int(y1)),(0,0,255),3)
                img_PIL = Image.fromarray(cv2.cvtColor(im_copy, cv2.COLOR_BGR2RGB))
                font = ImageFont.truetype('simhei.ttf', 20) 
                if not isinstance(skuName, unicode):  
                    str = skuName.decode('gbk')
                draw = ImageDraw.Draw(img_PIL)  
                draw.text((int(x),int(y)-20), str, font=font, fill=(255,0,255))
                im_copy = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)
            cv2.imwrite("%s\%s"%(drawDir,imageName), im_copy)

if __name__ == '__main__':
    drawROI()
    
