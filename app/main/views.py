import json

import requests
from flask import request, session, redirect, render_template, jsonify, current_app
from sqlalchemy import or_

from app import db
from datas.models.req_log import ReqLog
from datas.utils.times import get_now_time
from . import main
from ..decorated import login_required


@main.route('/',methods=['GET','POST'])
@login_required
def req_log_list():
    keywords = request.values.to_dict()
    page = int(request.args.get('page') or 1)
    keyword = keywords.get('keyword')
    filter_arr = []
    if keyword:
        filter_arr.append(or_(ReqLog.req_id.like('%{}%'.format(keyword)),ReqLog.post_json.like('%{}%'.format(keyword)),ReqLog.result.like('%{}%'.format(keyword))))

    page_data = ReqLog.query.filter(*filter_arr).order_by(db.desc(ReqLog.id)).paginate(page=page,per_page=20)
    if 'page' in keywords: del keywords['page']
    return render_template("index.html", page_data=page_data, keyword=keywords)

@main.route('/api_doc', methods=['GET'])
@login_required
def api_doc():
    return render_template("api_doc.html")

@main.route('/req')
@login_required
def do_requests():
    req_id = request.args.get('id')
    req = ReqLog.query.get(req_id)
    try:
        post_json = req.post_json
        if post_json:
            reqs = requests.post(req.req_url,data=req.post_json,headers={'User-Agent':'xiaoniu_tasks'},timeout=60)
        else:
            reqs = requests.get(req.req_url,headers={'User-Agent':'xiaoniu_tasks'})

        return jsonify({
            'errcode': 0,
            'errmsg': reqs.text,
            'url': ''
        })
    except Exception as e:
        return jsonify({
            'errcode':1,
            'errmsg':str(e),
            'url':''
        })

@main.route('/del')
@login_required
def delete_log():
    id = request.args.get('id')
    rl = ReqLog.query.get(id)
    db.session.delete(rl)
    db.session.commit()

    return jsonify({
        'errcode': 0,
        'errmsg': '删除成功',
        'url': '/'
    })

@main.route('/result')
@login_required
def req_result():
    id = request.args.get('id')
    type = request.args.get('type')
    rl = ReqLog.query.get(id)
    content = rl.respond
    if int(type) == 2:
        content = rl.result
    return render_template("result.html",content=content)

@main.route('/req_log_batch_del',methods=['GET','POST'])
@login_required
def req_log_batch_del():
    ids = request.form.getlist('id')
    ReqLog.query.filter(ReqLog.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({
        'errcode': 0,
        'errmsg': '删除成功',
        'url': '/'
    })

@main.route('/check_pass', methods=['GET', 'POST'])
def check_pass():
    today = get_now_time()
    msg = request.values.get('msg', '')

    if request.method == 'POST':
        try:
            password = request.values.get('password')
            if not password:
                return redirect("/check_pass?msg=密码不能为空")
            login_pwd = current_app.config.get('CONFIGS').get('login_pwd')
            if not login_pwd:
                return redirect("/check_pass?msg=请联系管理员")
            if login_pwd!=password:
                return redirect("/check_pass?msg=密码有误")
            session['is_login'] = True
            return redirect('/')
        except:
            return redirect("/check_pass?msg=系统有误,请重新试试")
    return render_template("check_pass.html", msg=msg, today=today)

@main.route('/logout')
def logout():
    session.clear()
    return redirect("/")