# coding = utf-8
"""
@author: zhou
@time:2019/12/19 19:14
@File: views.py
"""

from . import auth
from flask import request, jsonify, current_app
from ..models import User
from ..tools import token
import time
from ..tools import redis_connection
import json
from config import Config
import logging


rd = redis_connection.redis_conn_pool()
expires = Config.ACCESS_TOKEN_EXPIRES_IN


# 产生token
@auth.route('/api/auth/token/', methods=['GET', 'POST'])
def get_token():
    current_app.logger.info('Get token by client')
    try:
        if request.method == 'POST':
            post_data = json.loads(request.data)
            if 'username' in post_data and 'pwd' in post_data:
                user = User.query.filter_by(username=post_data['username']).first()
                pwd = post_data['pwd']
                if user and user.verify_password(pwd):
                    data = token.genTokenSeq(user=post_data['username'])
                    # h_dict = {"token": data['access_token'], "operate_time": time.time()}
                    # rd.hmset(user.id, h_dict)
                    return jsonify({'code': 200, 'expires_in': expires, 'data': data}), 200
                return jsonify({'code': 422, 'message': 'Wrong username or password!'}), 422
            return jsonify({'code': 422, 'message': 'Wrong parameter!'}), 422
        elif request.method == 'GET':
            get_args = request.args
            if get_args.get('username') and get_args.get('pwd'):
                user = User.query.filter_by(username=get_args.get('username')).first()
                pwd = get_args.get('pwd')
                if user and user.verify_password(pwd):
                    data = token.genTokenSeq(user=get_args.get('username'))
                    # h_dict = {"token": data['access_token'], "operate_time": time.time()}
                    # rd.hmset(user.id, h_dict)
                    return jsonify({'code': 200, 'expires_in': expires, 'data': data}), 200
                return jsonify({'code': 422, 'message': 'Wrong username or password!'}), 422
            return jsonify({'code': 422, 'message': 'Wrong parameter!'}), 422
        else:
            return jsonify({'code': 422, 'message': 'Wrong method!'})
    except Exception as e:
        current_app.logger.error('Get token by client error: %s' % e)