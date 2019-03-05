1. 环境管理[conda](https://docs.conda.io/en/latest/)
```
conda create -n spotify python=3.6
```
2. 包安装
```
pip install Flask   
pip install Pillow # 图片处理工具
pip install requests
pip install gunicorn
pip install gevent
```
3. 启动服务
```
set FLASK_APP=app.py & set FLASK_DEBUG=1 & flask run  # 开发模式
gunicorn -c guni.py app:app  # 生产模式

```