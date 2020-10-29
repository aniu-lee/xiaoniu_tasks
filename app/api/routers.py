#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import datetime
import uuid

from flask import request, json

from app import db
from app.decorated import request_params, api_deal_return,api_err_return
from app.tasks import celery_run
from datas.models.req_log import ReqLog
from . import api


@api.route('/demo', methods=['POST','GET'])
@request_params(required=[],optional=[],is_sign=False)
@api_deal_return
def demo():
    datas = request.values.to_dict()
    if request.data:
        datas = json.loads(request.data)
    return 'ok',datas

'''
req_url 请求的链接
delay_time 延迟时间 默认0 不延迟
post_data 字符串 post数据
is_fail_try 失败是否重试 0 
priority 0 默认不优先
remark 备注
'''
@api.route('/task', methods=['POST'])
@request_params(required=['req_url'],optional=['delay_time','post_json','is_fail_try','priority','remark'])
@api_deal_return
def task():

    datas = request.datas

    req_id = str(uuid.uuid1())

    delay_time = datas.get('delay_time') or 0

    remark = datas.get('remark')

    req_url = datas.get('req_url')

    if 'http://' not in req_url and 'https://' not in req_url:
        return api_err_return(msg='req_url好像不是个链接')

    try:
        if int(delay_time) < 0:
            return api_err_return(msg='delay_time必须大于等于0')
    except:
        return api_err_return(msg='delay_time必须是数字型')

    priority = int(datas.get('priority') or 0)
    try:
        if int(priority) < 0:
            return api_err_return(msg='priority必须大于等于0')
        if int(priority) not in range(10):
            return api_err_return(msg='priority范围[0-9]有误')
    except:
        return api_err_return(msg='priority必须是数字型')

    post_json = datas.get('post_json') or ''

    if post_json:
        try:
            j = json.loads(post_json)
            if type(j) != dict:
                api_err_return(msg='post_json格式有问题')
        except:
            return api_err_return(msg='post_json格式有问题')

    try:
        is_fail_try = int(datas.get('is_fail_try') or 0)
    except:
        return api_err_return(msg='is_fail_try必须是数字型')

    if priority == 0:
        queue = 'default'
    else:
        queue = 'prioritys'

    celery_run.apply_async(queue=queue,priority=priority,countdown = int(delay_time),args=[req_url,req_id,queue,priority,int(delay_time),post_json,is_fail_try,True,0,remark])

    return '已加入后台队列',{
        'req_id':req_id
    }


@api.route('/task_result_add', methods=['POST', 'GET'])
@request_params(required=['req_id','result'])
@api_deal_return
def task_result_add():
    datas = request.datas
    req_id = datas.get('req_id')
    result = datas.get('result')
    rl = ReqLog.query.filter(ReqLog.req_id == req_id).first()
    if not rl:
        return api_err_return(msg='该任务不存在')
    rl.result = result
    db.session.add(rl)
    db.session.commit()

    return 'ok'

'''
删除记录
'''
@api.route('/del_log', methods=['POST','GET'])
@request_params(is_sign=False,optional=['data'])
@api_deal_return
def del_log():
    tiimes = (datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:%S")
    ReqLog.query.filter(ReqLog.create_time < tiimes).delete(synchronize_session=False)
    db.session.commit()
    return 'ok'
