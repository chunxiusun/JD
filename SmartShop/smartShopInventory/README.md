1、smartShopInventory.py

功能：调用理货算法接口，将返回的商品信息（sku编号和坐标）保存文件，且将商品的坐标和名称画到图片上

2、drawROI.py（定义函数，其他画框需求也可调用）

功能：图片画框后保存

传参：需传入图片位置、图片中目标坐标及名称、画框后图片保存路径（可选参数）

调用方法：

from drawROI import drawROI

drawROI(localImage,objList,drawDir)#drawDir可传可不传，不传默认画框后图片存在当前目录下drawImages文件夹

或drawROI(localImage, objList)