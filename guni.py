import gevent.monkey
import multiprocessing

"""
gunicorn的配置文件
"""
# gevent的猴子魔法 变成非阻塞
gevent.monkey.patch_all()

debug = True
loglevel = 'info'
bind = '0.0.0.0:5432'

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2  # 指定每个进程开启的线程数
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
preload_app = True
x_forwarded_for_header = 'X-FORWARDED-FOR'