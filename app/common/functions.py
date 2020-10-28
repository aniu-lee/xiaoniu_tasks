#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import traceback

import requests
from flask import current_app

'''
推送
https://www.aniulee.com
'''
def wechat_info_err(titile,content=''):
    try:
        config = current_app.config.get('CONFIGS')
        api_key = config.get('error_notice_api_key')
        if api_key:
            post_url = 'https://api.aniulee.com/blog_api_go/api/v1/push'
            data = {
                'api_key': api_key,
                'content': content,
                'title': titile
            }
            requests.post(post_url, data=data,timeout=2,headers={'user-agent':'XNTask'})
    except Exception as e:
        print(str(e))