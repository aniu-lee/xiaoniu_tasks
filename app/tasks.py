#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import json
import time
import traceback

import requests
from flask import current_app

from app import celery, db
from app.common.functions import  wechat_info_err
from datas.models.req_log import ReqLog
from datas.utils.times import get_now_time


@celery.task
def celery_task_demo(a,b):
    time.sleep(10)
    return a + b

'''
后台任务访问(调用)接口
'''
@celery.task()
def celery_run(url,req_id,queue,priority,delay_time=0,post_json=None,is_fail_try=0,is_first=True,fail_counts=0,remark=''):
    time1 = time.time()
    try:

        is_err = False

        config = current_app.config.get('CONFIGS')

        timeouts = 60*2

        tt_list = config.get('retry_times')

        if tt_list:
            tt_list = tt_list.replace('，',',').split(',')

        else:
            tt_list = [30,60,180,900,1800,3600,43200]

        headers = {
            'User-Agent':'xiaoniu_tasks'
        }

        reqs = requests.Session()

        if post_json:
            rep = reqs.post(url,data=post_json,timeout=timeouts,headers=headers)
        else:
            rep = reqs.get(url, timeout=timeouts,headers=headers)

        ret = rep.text

        try:
            ret = rep.json()
        except:
            pass

        if type(ret) == dict:
            ret = json.dumps(ret, ensure_ascii=False)

        error_keyword = config.get('error_keyword')

        if error_keyword and is_fail_try == 1:
            error_keyword = error_keyword.replace('，', ',').split(',')
            for item in error_keyword:
                if item.strip().lower() in ret.lower():
                    is_err = True
                    wechat_info_err('定时任务【%s】发生错误' % req_id, '返回信息:%s' % ret)
                    break

        if is_err is True:
            #看是否得重试
            if is_first is True:
                is_first = False
                if is_fail_try == 1:delay_time = int(tt_list[0])
            else:
                if is_fail_try== 1:
                    is_first = False
                    if int(delay_time) == int(tt_list[-1]):
                        is_fail_try = 0
                        delay_time = -1
                    else:
                        delay_time = int(tt_list[tt_list.index(str(delay_time)) + 1])

            if delay_time !=-1:
                celery_run.apply_async(queue=queue,priority=priority,countdown = int(delay_time),args=[url,req_id,queue,priority,delay_time,post_json,is_fail_try,is_first,fail_counts,remark])
        time2 = time.time() - time1
        rl = ReqLog.query.filter(ReqLog.req_id == req_id).first()
        if not rl:
            rl = ReqLog(req_url=url,req_id=req_id,post_json=post_json,respond=ret,create_time=get_now_time(),is_err=int(is_err),take_time=time2)
        else:
            rl.respond = "%s<br/><br/>%s" % (rl.respond,ret)
            rl.update_time = get_now_time()
            rl.is_err = int(is_err)
            rl.take_time = time2

        db.session.add(rl)
        db.session.commit()

    except Exception as e:
        if fail_counts <=5:
            fail_counts = fail_counts + 1
            celery_run.apply_async(queue=queue,priority=priority,countdown=30*fail_counts,args=[url, req_id, queue,priority,delay_time, post_json, is_fail_try, is_first,fail_counts,remark])
            # trace_info = traceback.format_exc()
            # print(trace_info)