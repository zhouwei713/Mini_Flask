# coding = utf-8
"""
@author: zhou
@time:2019/12/12 18:43
@File: apschedulerjob.py
"""

from app import scheduler
from app import db
from .models import ZhihuDetails, ZhihuMetrics, ZhihuContent
from .get_zhihu import get_hot_zhihu, get_answer_zhihu
import datetime
from flask import current_app
import time
from .tools import redis_connection


rd = redis_connection.redis_conn_pool()


def opera_db():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('cron job start at: ', current_time)

    with scheduler.app.app_context():
        update_time = time.strftime('%Y-%m-%d %H:%M:00', time.localtime())
        current_app.logger.info('system log cron job start at: %s' % current_time)
        rd.set('new_update_time', update_time)
        try:
            current_app.logger.info(
                'get zhihu hot data: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            hot_list = get_hot_zhihu()
        except Exception as e:
            current_app.logger.error(
                'get zhihu hot data error: %s' % e)
        hot_cardid_list = db.session.query(ZhihuDetails.hot_cardid).all()
        hot_cardid_list = set(hot_cardid_list)
        hotcardid_id = [i[0] for i in hot_cardid_list]

        # cardid_list = [i['cardId'] for i in hot_list]

        for i in hot_list:
            cut_list = i['cardId'].split('_')
            if cut_list[0] == 'Q':
                answer_id = int(cut_list[1])
            else:
                continue
            try:
                answer_zhihu = get_answer_zhihu(answer_id)
            except Exception as e:
                current_app.logger.error(
                    'get zhihu answer data error (answer id: %s): %s' % (answer_id, e))
            if i['cardId'] in hotcardid_id:
                try:
                    update_metrics = ZhihuMetrics(hot_metrics=i['target']['metricsArea']['text'],
                                                  hot_cardid=i['cardId'],
                                                  update_time=datetime.datetime.now())
                    db.session.add(update_metrics)
                    db.session.commit()
                except Exception as e:
                    current_app.logger.error(
                        'update zhihu hot data error: %s' % e)
                    db.session.rollback()

                try:
                    for answer in answer_zhihu:
                        answer_info = ZhihuContent.query.filter_by(answer_id=answer_id, author=answer['author']).first()
                        if answer_info:
                            answer_info.voteup_count = answer['voteup_count']
                            answer_info.comment_count = answer['comment_count']
                            answer_info.reward_info = answer['reward_info']
                            db.session.commit()
                        else:
                            new_content = ZhihuContent(answer_id=answer_id, author=answer['author'], voteup_count=answer['voteup_count'],
                                                       comment_count=answer['comment_count'],
                                                       reward_info=answer['reward_info'],
                                                       content=answer['content'])
                            db.session.add(new_content)
                            db.session.commit()
                except Exception as e:
                    current_app.logger.error(
                        'update zhihu answer data error: %s' % e)
                    db.session.rollback()
            else:
                try:
                    new_details = ZhihuDetails(hot_id=i['id'], hot_name=i['target']['titleArea']['text'],
                                               hot_link=i['target']['link']['url'], hot_cardid=i['cardId'])
                    new_metrics = ZhihuMetrics(hot_metrics=i['target']['metricsArea']['text'],
                                               hot_cardid=i['cardId'],
                                               update_time=datetime.datetime.now())
                    db.session.add(new_details)
                    db.session.add(new_metrics)
                    db.session.commit()
                except Exception as e:
                    current_app.logger.error(
                        'insert zhihu hot data error: %s' % e)
                    db.session.rollback()

                try:
                    for answer in answer_zhihu:
                        new_content = ZhihuContent(answer_id=answer_id, author=answer['author'], voteup_count=answer['voteup_count'],
                                                   comment_count=answer['comment_count'], reward_info=answer['reward_info'],
                                                   content=answer['content'])
                        db.session.add(new_content)
                        db.session.commit()
                except Exception as e:
                    current_app.logger.error(
                        'insert zhihu answer data error: %s' % e)
                    db.session.rollback()
        current_app.logger.info(
            'system log cron job end at: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('cron job end at: ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
