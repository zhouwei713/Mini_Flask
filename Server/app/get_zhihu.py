# coding = utf-8
"""
@author: zhou
@time:2019/12/12 19:11
@File: get_zhihu.py
"""

import requests
from bs4 import BeautifulSoup
import json
from config import Config


def get_hot_zhihu():
    url = 'https://www.zhihu.com/billboard'
    headers = {"User-Agent": "", "Cookie": ""}
    res = requests.get(url, headers=headers)
    content = BeautifulSoup(res.text, "html.parser")
    hot_data = content.find('script', id='js-initialData').string
    hot_json = json.loads(hot_data)
    hot_list = hot_json['initialState']['topstory']['hotList']
    return hot_list


def get_answer_zhihu(id):
    url = 'https://www.zhihu.com/api/v4/questions/%s/answers?include=' % id
    headers = {"User-Agent": "", "Cookie": ""}
    res = requests.get(url + Config.ZHIHU_QUERY, headers=headers)
    data_json = res.json()
    answer_info = []
    for i in data_json['data']:
        if 'paid_info' in i:
            continue
        answer_info.append({'author': i['author']['name'], 'voteup_count': i['voteup_count'],
                            'comment_count': i['comment_count'], 'content': i['content'],
                            'reward_info': i['reward_info']['reward_member_count']})
    return answer_info


if __name__ == '__main__':
    hot_list = get_hot_zhihu()
    for i in hot_list:
        print(i)

