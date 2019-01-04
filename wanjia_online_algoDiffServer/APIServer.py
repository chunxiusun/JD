#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, abort, request, jsonify, url_for
from detectCheck import AlgorithmCheck

app = Flask(__name__)

@app.route('/HelloWorld')
def hello_world():
    return "Hello World!"

@app.route('/check/detectResult',methods=['post'])
def check_recResult():
    label_file = request.files["labelFile"]
    test_file = request.files["testFile"]
    print "ssssssssssssssssssssssss"
    algorithmCheck = AlgorithmCheck(label_file,test_file)
    data = algorithmCheck.Check()
    if isinstance(data,str):
        return jsonify({"code": 1, "msg":data})
    else:
        return jsonify({"code": 0, "msg":"调用成功！", "data":data})


if __name__ == "__main__":
    app.run(host="172.20.141.77", port=22222, debug=True)
