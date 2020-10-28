#!/usr/bin/python3 
# -*- coding:utf-8 -*-
from configparser import ConfigParser


def configs(key = None):
    cp = ConfigParser()
    cp.read('conf.ini',encoding='utf-8')
    if key:
        return cp.get('default',key)
    celery_job_log_db_url = cp.get('default','celery_job_log_db_url')
    celery_broker_url = cp.get('default','celery_broker_url')
    login_pwd = cp.get('default','login_pwd')
    error_notice_api_key = cp.get('default','error_notice_api_key')
    job_log_counts = cp.get('default','job_log_counts')
    api_access_token = cp.get('default','api_access_token')
    error_keyword = cp.get('default',"error_keyword")
    retry_times = cp.get('default','retry_times')

    pz = {
        'celery_job_log_db_url':celery_job_log_db_url,
        'celery_broker_url':celery_broker_url,
        'login_pwd':login_pwd,
        'error_notice_api_key':error_notice_api_key,
        'job_log_counts':job_log_counts,
        'api_access_token':api_access_token,
        'error_keyword':error_keyword,
        'retry_times':retry_times
    }

    return pz