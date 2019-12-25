# coding = utf-8
"""
@author: zhou
@time:2019/12/12 20:47
@File: db_opera.py
"""

from config import Config


def db_to_list(data):
    data_list = []
    for i in data:
        if i.hot_metrics == '盐选会员':
            continue
        data_list.append([int(i.hot_metrics.split()[0]), i.hot_cardid, i.update_time])
    data_list.sort(key=order_key, reverse=True)
    if len(data_list) <= Config.RETURN_NUM:
        return data_list
    return data_list[:Config.RETURN_NUM+1]


def order_key(elem):
    return elem[0]
