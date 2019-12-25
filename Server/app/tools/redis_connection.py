# coding = utf-8
"""
@author: zhou
@time:2019/8/21 10:35
@File: redis_connection.py
"""

import redis
from config import Config


def redis_conn_pool():
    pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                                decode_responses=True, password=Config.REDIS_PWD)
    r = redis.Redis(connection_pool=pool)
    return r


if __name__ == '__main__':
    pass
