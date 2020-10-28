#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import time

'''
获取当前时间
'''
def get_now_time(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format,time.localtime(time.time()))