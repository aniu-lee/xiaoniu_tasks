from flask import jsonify
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({
        "errcode":1,
        "errmsg":'router is not found',
        "data":None
    })

@main.app_errorhandler(405)
def page_not_found(e):
    return jsonify({
        "errcode":1,
        "errmsg":'router method is not found',
        "data":None
    })

@main.app_errorhandler(500)
def internal_server_error(e):
    print(e)
    return jsonify({
        "errcode": 1,
        "errmsg": 'system err!',
        "data": None
    })
