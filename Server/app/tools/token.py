# coding = utf-8
"""
@author: zhou
@time:2019/12/19 16:05
@File: token.py
"""

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData
import time
from ..models import User
from functools import wraps
from flask import request
from config import Config
from ..tools import redis_connection
import json
from flask import jsonify


secret_key = Config.SECRET_KEY
salt = Config.SALT
access_token_expires_in = Config.ACCESS_TOKEN_EXPIRES_IN
refresh_token_expires_in = Config.REFRESH_TOKEN_EXPIRES_IN

rd = redis_connection.redis_conn_pool()


def genTokenSeq(user=None, userid=None, onlyaccesstoken=False):
    if user is None and userid is None:
        return jsonify({'code': 422, 'message': 'Wrong parameter!'}), 422
    if user:
        u = User.query.filter_by(username=user).first()
        if u:
            userid = u.id
        else:
            return jsonify({'code': 422, 'message': 'Wrong username or password!'}), 422
    access_token_gen = Serializer(secret_key=secret_key, salt=salt, expires_in=access_token_expires_in)
    refresh_token_gen = Serializer(secret_key=secret_key, salt=salt, expires_in=refresh_token_expires_in)
    timtstamp = time.time()
    access_token = access_token_gen.dumps({
        "userid": userid,
        "iat": timtstamp
    })
    refresh_token = refresh_token_gen.dumps({
        "userid": userid,
        "iat": timtstamp
    })
    if onlyaccesstoken:
        data = {
            "access_token": str(access_token, 'utf-8'),
            "access_token_expire_in": access_token_expires_in,
        }
        return data
    else:
        data = {
                "access_token": str(access_token, 'utf-8'),
                "access_token_expire_in": access_token_expires_in,
                "refresh_token": str(refresh_token, 'utf-8'),
                "refresh_token_expire_in": refresh_token_expires_in,
        }
        return data


def check_token(token):
    token_list = []
    if rd.keys("token*"):
        for t in rd.keys("token*"):
            token_list.append(rd.get(t))
    if token in token_list:
        return {'code': 401, 'message': 'token is blocked'}, 401
    validator = validateToken(token)
    if validator['code'] != 200:
        if validator['message'] == 'toekn expired':
            return validator
        else:
            return validator
    elif validator['code'] == 200:
        return True


def tokenRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            post_data = json.loads(request.data)
            if 'token' in post_data and 'secret' in post_data and post_data['secret'] == '周萝卜真帅':
                token = post_data['token']
                check_result = check_token(token)
                if check_result is True:
                    return f(*args, **kwargs)
                else:
                    return jsonify(check_result), 401
            return jsonify({'code': 422, 'message': '按套路出牌啊'}), 422
        elif request.method == 'GET':
            get_args = request.args
            if get_args.get('token') and get_args.get('secret') and get_args.get('secret') == '周萝卜真帅':
                token = get_args.get('token')
                check_result = check_token(token)
                if check_result is True:
                    return f(*args, **kwargs)
                else:
                    return jsonify(check_result), 401
            return jsonify({'code': 422, 'message': '按套路出牌啊'}), 422

    return decorated_function


def validateToken(token):
    s = Serializer(secret_key=secret_key, salt=salt)
    try:
        data = s.loads(token)
    except SignatureExpired:
        msg = 'toekn expired'
        return {'code': 401, 'error_code': 'auth_01', 'message': msg}
    except BadSignature as e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                msg = 'token tampered'
                return {'code': 401, 'error_code': 'auth_01', 'message': msg}
        msg = 'badSignature of token'
        return {'code': 401, 'error_code': 'auth_01', 'message': msg}
    except:
        msg = 'wrong token with unknown reason'
        return {'code': 401, 'error_code': 'auth_01', 'message': msg}

    if 'userid' not in data:
        msg = 'illegal payload inside'
        return {'code': 401, 'error_code': 'auth_01', 'message': msg}
    msg = 'user(' + str(data['userid']) + ') logged in by token.'
    userId = data['userid']
    return {'code': 200, 'error_code': 'auth_00', 'message': msg, 'userid': userId}