#!/usr/bin/env python
#coding:utf-8
import os
import time

import requests
from flask import json
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from flask_script import Manager, Shell

from app.common.functions import wechat_info_err
from app.tasks import celery_task_demo, celery_run
from datas.models.req_log import ReqLog
from datas.utils.times import get_now_time

'''
production
os.getenv('FLASK_CONFIG') or 'default'
'''
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(
        app=app,
        ReqLog=ReqLog
    )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

def set_is_err():
    db.session.execute("update req_log set is_err=0 where id >0")

@manager.command
def test():

    # requests.post("http://celery.58pxw.com/api/v1/run", data={'url': 'http://celery.58pxw.com/api/v1/demo', 'data': '', 'exe_time': ''})
    # wechat_info_err('bug来了,看得到吗','详细信息可以看到在哪个文件出错。88888')
    # set_is_err()
    # reqs = requests.post('http://127.0.0.1:5000/api/v1/demo', data={'data': ''}, headers={'User-Agent': 'xmb_celery'},timeout=60)
    # print(reqs.text)
    # t = time.time()
    # time.sleep(2.5)
    # tt = time.time()  -t
    # rl = ReqLog(url='', datas='', result='', create_time=get_now_time(), req_id='fasdf', is_err=0,take_time=tt)
    # db.session.add(rl)
    # db.session.commit()
    # celery_task_demo.apply_async(args=[1,1])
    # celery_task_demo.apply_async(args=[1, 2])
    # celery_task_demo.apply_async(args=[1, 3])
    # celery_task_demo.apply_async(args=[1, 4])
    # sign = celery_task_demo.s(1,1)
    # sign.apply_async(queue='prioritys',priority=2)
    # sign = celery_task_demo.s(2,2)
    # sign.apply_async(queue='prioritys',property=9)
    # sign = celery_task_demo.s(3,3)
    # sign.apply_async(queue='prioritys',priority=7)
    # celery_task_demo.apply_async(queue='prioritys',args=[1, 4],priority=2)
    post_json = json.dumps({
        'username':'aniulee'
    })
    url = "http://cron_demo.aniulee.com/api/cron/test?id=fail"
    url = "http://127.0.0.1:6656/api/demo"
    req = requests.post("http://127.0.0.1:6656/api/task",data={'req_url':url,'is_fail_try':1})
    print(req.json())
    # sign = celery_run.s("http://127.0.0.1:5000/api/demo","11111",is_fail_try=1)
    # sign.apply_async()

if __name__ == '__main__':
    manager.run()
