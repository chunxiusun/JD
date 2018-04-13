# -*- coding:utf8 -*-

'''调用理货算法接口，将返回的商品信息（sku编号和坐标）保存文件，且将商品的坐标和名称画到图片上 '''

import os, requests, json, time, datetime
import traceback
import cv2
import urllib.request
from math import *
from drawROI import drawROI

imageURL = "http://img20.360buyimg.com/cv/jfs/t18844/276/1483557371/110165/65d975a2/5acb3819N40def98b.jpg"
fileName = "skuInfo.txt"
drawDir = ".\originImages\\"

if not os.path.exists(drawDir):
    os.mkdir(drawDir)

DRAW = 1  # 1表示画框，0表示不画框


def smartShopInventory():
    fw = open(fileName, 'a+')
    img = imageURL[imageURL.find("jfs"):]
    httpUrl = "http://vse.jd.care/smartshop/inventory?url=%s" % img
    try:
        re = requests.post(httpUrl)
        print (re.status_code)
        data = json.loads(re.text)
    except:
        fw.write("error\r\n")
        f = open("log.txt", 'a+')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        fw.close()
        return
    errorCode = data["summary"]["errorCode"]
    errorMsg = data["summary"]["errorMsg"]
    skuCount = data["summary"]["count"]
    queryCost = data["summary"]["cost"]
    skuThreshold = data["summary"]["threshold"]
    skuList = data["wareCollection"]
    fw.write("%s " % datetime.datetime.now())
    for item in ["errorCode", "errorMsg", "skuCount", "queryCost", "skuThreshold"]:
        fw.write(eval(item) + " ")

    for item in ["skuNumber", "skuIdx", "skuBox", "skuDist"]:
        item = ""
    if len(skuList) > 0:
        for sku in skuList:
            skuNumber = sku["sku"]
            skuIdx = sku["sku_idx"]
            skuBox = sku["box"]
            roi = skuBox.split("|")
            skuDist = sku["dist"]
            for item in ["skuNumber", "skuIdx", "skuBox", "skuDist"]:
                fw.write(eval(item) + " ")
        if DRAW == 1:
            dealImage(skuList)
    fw.write("\r\n")
    fw.close()


def dealImage(skuList):
    imageBinData = urllib.request.urlopen(imageURL).read()
    localImage = drawDir + imageURL[imageURL.rfind("/") + 1:]
    with open(localImage, 'wb') as f_img:
        f_img.write(imageBinData)
    im = cv2.imread(localImage)
    # 旋转图片，保持图像不被裁剪
    height, width, channel = im.shape
    degree = 90
    font = cv2.FONT_HERSHEY_SIMPLEX
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) / 2
    matRotation[1, 2] += (heightNew - height) / 2
    dst = cv2.warpAffine(im, matRotation, (widthNew, heightNew))
    cv2.imwrite("%s" % (localImage), dst)

    objList = []
    mappingDict = {"630838": "ABC", "5037855": "牛栏山", "5042359": "可口可乐"}
    for sku in skuList:
        skuNumber = sku["sku"]
        skuBox = sku["box"]
        skuName = mappingDict[skuNumber]
        obj = "%s:%s" % (skuName, skuBox)
        objList.append(obj)
    # objList = ["可口可乐:726.23|472.88|792.78|625.91","牛栏山:396.44|368.78|482.33|650.44"] 格式：商品名称:坐标  坐标格式：x|y|x1|y1
    # objList = ["726.23|472.88|792.78|625.91","396.44|368.78|482.33|650.44"]  格式：坐标
    # drawROI(localImage,objList,drawDir)#drawDir可传可不传，不传默认画框后图片存在当前目录下drawImages文件夹
    drawROI(localImage, objList)


if __name__ == '__main__':
    # while True:
    smartShopInventory()
    # time.sleep(60)