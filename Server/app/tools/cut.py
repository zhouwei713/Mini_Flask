# coding = utf-8
"""
@author: zhou
@time:2019/12/20 15:58
@File: cut.py
"""

import jieba
import jieba.analyse
import os
import re


basedir = os.path.abspath(os.path.dirname(__file__))
stopwords_path = os.path.join(basedir, 'stopwords')


excludes = {'<', '>', '/', 'p', '，', '！', '？', '我', '你', '他', '的', '。', '了', '-', '—', '"',
            '在', '是', ' ', '=', 'br', '～', '.'}


def cut_word(word):
    word = re.sub('[a-zA-Z0-9]', '', word)
    empty_str = ' '
    with open(stopwords_path, encoding='utf-8') as f:
        stop_words = f.read()
    stop_words = stop_words + empty_str
    counts = {}
    txt = jieba.lcut(word)
    for w in txt:
        if w not in stop_words:
            counts[w] = counts.get(w, 0) + 1
    sort_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    return sort_counts[:20]


def key_word(word):
    word = re.sub('[a-zA-Z0-9]', '', word)
    print(str)
    jieba.analyse.set_stop_words(stopwords_path)
    tags = jieba.analyse.extract_tags(word, topK=100, withWeight=True)
    return tags[:10]


if __name__ == '__main__':
    word = '<p>我是一名护士</p><p>刚上班的时候发基本工资3600</p><p>后来有一天，我突然发奖金了，奖金8800</p><p>虽然和知乎小伙伴比不了，</p>'
    cut_word(word)
