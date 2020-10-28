#!/usr/bin/python3 
# -*- coding:utf-8 -*-
from urllib.parse import unquote,unquote_plus

from app import db

'''
请求记录
'''
class ReqLog(db.Model):
    __tablename__='req_log'
    id = db.Column(db.Integer,primary_key=True)
    remark = db.Column(db.String(65),nullable=False,server_default='',default='',doc='备注')
    req_id = db.Column(db.String(65), nullable=False, default='')
    req_url = db.Column(db.String(128),nullable=False,default='')
    post_json = db.Column(db.TEXT,nullable=False,default='')
    respond = db.Column(db.TEXT,nullable=False,server_default='',default='',doc='请求结果')
    result = db.Column(db.TEXT,nullable=False,default='',doc='用户回调结果内容')
    create_time = db.Column(db.String(25),nullable=False,default='')
    update_time = db.Column(db.String(25),nullable=False,default='')
    is_err = db.Column(db.SMALLINT,default=0)
    take_time = db.Column(db.String(25),default='')

    def to_json(self):
        return {
            'id':self.id,
            'req_url':self.req_url,
            'post_json':self.post_json,
            'result': self.result,
            'create_time':self.create_time,
            'update_time':self.update_time,
            'req_id':self.req_id,
            'take_time':self.take_time
        }