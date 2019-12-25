# coding = utf-8
"""
@author: zhou
@time:2019/12/12 14:45
@File: views.py
"""

from . import main
from .. import db
from flask import request, jsonify, render_template
from ..tools import redis_connection
from config import Config


rd = redis_connection.redis_conn_pool()


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/adddb/', methods=['GET', 'POST'])
def addbd():
    db.create_all()
    return "OK"


@main.before_app_request
def before_request():
    remote_add = request.remote_addr
    rd_add = rd.get('access_num_%s' % remote_add)
    if rd_add:
        if int(rd_add) <= Config.REQUEST_NUM:
            rd.incr('access_num_%s' % remote_add)
        else:
            return jsonify({'code': 422, 'message': '访问太频繁啦！'}), 422
    else:
        rd.set('access_num_%s' % remote_add, 1, ex=60)



