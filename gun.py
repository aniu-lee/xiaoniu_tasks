#-*-coding:utf-8-*-
import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()
errorlog='access_err_log.log'
loglevel = 'error'
# bind = '127.0.0.1:5850'
bind = 'xiaoniu_tasks.sock'
# 启动的进程数
#workers = 1
# workers = multiprocessing.cpu_count() * 2 + 1
workers=4

worker_class='gevent'

x_forwarded_for_header = 'X-FORWARDED-FOR'
