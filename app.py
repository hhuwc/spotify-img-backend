from flask import Flask
from flask import request, jsonify
import requests
import os
import colorsys
from PIL import Image

app = Flask(__name__)

# 文件绝对路径
folder = "{}/img/".format(os.getcwd())
if not os.path.exists(folder):
    os.mkdir(folder)

# 计算过的图片信息缓存
img_color_cache = {}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/calc_color", methods=['POST'])
def calc_color():
    request_data = request.json
    picUrl = request_data["picUrl"]

    # 默认色彩
    color = (210, 171, 164)

    if picUrl:
        filename = picUrl.split("/")[-1]
        exists = write_img(picUrl, filename)
        if exists:
            color = calc_img_color(filename)

        return jsonify({'success': True, 'color': color})
    else:
        return jsonify({'success': False})


def calc_img_color(name):
    if img_color_cache.get(name, None):
        return img_color_cache[name]

    image = Image.open(folder + name)
    image = image.convert('RGBA')
    image.thumbnail((128, 128))  # 生成一个缩略图

    max_score = None
    dominant_color = None

    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 透明度为0忽略
        if a == 0:
            continue

        # y 信号
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

        light_color = (y - 16.0) / (235 - 16)

        dark_color = (y - 16.0) / (90 - 16)

        # 忽略高亮色
        if light_color > 0.9:
            continue

        # 忽略暗黑色
        if dark_color < 1:
            continue

        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        score = (saturation + 0.1) * count
        if (max_score == None) or score > max_score:
            max_score = score
            dominant_color = (r, g, b)

    img_color_cache[name] = dominant_color
    return dominant_color


def write_img(url, name):
    if not os.path.exists(folder + name):
        try:
            r = requests.get(url)
            if not os.path.exists(folder):
                os.mkdir(folder)
            with open(folder + name, "wb") as code:
                code.write(r.content)
                code.flush()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return True
