# coding = utf-8
"""
@author: zhou
@time:2019/12/12 14:41
@File: config.py
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hardtohard'
    SALT = os.getenv('SALT') or 'hardtoguess'
    ACCESS_TOKEN_EXPIRES_IN = 1800
    REFRESH_TOKEN_EXPIRES_IN = 86400
    SESSION_EXPIRED_TIME = 300
    EXPARE_TIME = 604800  # 7 天
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_HOST = os.getenv('REDIS_HOST') or '127.0.0.1'
    REDIS_PORT = os.getenv('REDIS_PORT') or '6379'
    REDIS_PWD = os.getenv('REDIS_PORT') or ''
    REQUEST_NUM = 20
    JOBS = [
        {
            'id': 'autosubimit',
            'func': 'app.apschedulerjob:opera_db',  # 路径：job函数名
            'args': None,
            'trigger': {
                'type': 'interval',
                'seconds': 3600
            }
        }
    ]
    RETURN_NUM = 50
    ZHIHU_QUERY = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mini_flask.sqlite3')


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:root@localhost/mini'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
