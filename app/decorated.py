#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import json
import traceback
from functools import wraps

from flask import request, current_app, session, redirect

from app.common.functions import  wechat_info_err
from datas.utils.json import api_return

'''
#明显错误返回
'''
def api_err_return(msg,code=1,data=None):
    return code, msg, data

'''
接口 api返回
'''
def api_deal_return(func):
    @wraps(func)
    def gen_status(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if type(result)==str:
                return api_return(errcode=0,errmsg=result)
            if type(result)==list or type(result)==dict:
                return api_return(errcode=0,errmsg='success',data=result)
            if type(result)==tuple:
                if len(result)==2:
                    errmsg=result[0]
                    if errmsg is None or errmsg=="":
                        errmsg='success'
                    return api_return(errcode=0, errmsg=errmsg, data=result[1])
                else:
                    return api_return(errcode=result[0],errmsg=result[1],data=result[2])
        except Exception as e:
            error = str(e)
            trace_info = traceback.format_exc()
            wechat_info_err("小牛异步队列-BUG",trace_info)
            return api_return(errcode=1, errmsg=error)
    return gen_status

# request 参数验证
def request_params(required=None, optional=None,is_sign=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            param = {}
            request_param = {}

            config = current_app.config.get('CONFIGS')

            if request.method == 'GET':
                request_param = request.values.to_dict()

            if request.method == 'POST':
                request_param = request.form.to_dict()

            api_access_token = config.get('api_access_token')
            if is_sign is True and api_access_token:
                if api_access_token != request_param.get('access_token'):
                    return api_return(errmsg='access_token 有误!!',errcode=1)

            if required:
                for req in required:
                    validate_param = request_param.get(req)
                    if validate_param is None or validate_param is False:
                        message = '缺少参数: ' + req
                        return api_return(errcode=1, errmsg=message)
                    else:
                        param[req] = validate_param

            if optional:
                for opt in optional:
                    validate_param = request_param.get(opt)
                    if validate_param:
                        param[opt] = validate_param
                    else:
                        param[opt] = ''

            request.datas = param

            return func(*args, **kwargs)
        return wrapper
    return decorator

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'is_login' not in session:
            return redirect('/check_pass?msg=需要验证密码')

        return func(*args, **kwargs)

    return wrapper