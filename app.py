from flask import Flask
from flask import request,jsonify
import requests 
import os

app = Flask(__name__)

# 文件绝对路径
folder="{}/img/".format(os.getcwd())

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/calc_color",methods=['POST'])
def calc_color():
    request_data = request.json
    picUrl = request_data["picUrl"]

    if picUrl:
      r = requests.get(picUrl) 
      filename = picUrl.split("/")[-1]
      if not os.path.exists(folder + filename):
        with open(folder + filename, "wb") as code:
          code.write(r.content)
          code.flush()

      return jsonify({'success':True})
    else:
      return jsonify({'success':False})


def calc_img_color():
