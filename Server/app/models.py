# coding = utf-8
"""
@author: zhou
@time:2019/12/12 14:54
@File: models.py
"""

from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class ZhihuDetails(db.Model):
    __tablename__ = 'ZhihuDetails'
    id = db.Column(db.Integer, primary_key=True)
    hot_id = db.Column(db.String(32), unique=True, index=True)
    hot_name = db.Column(db.Text)
    hot_link = db.Column(db.String(64))
    hot_cardid = db.Column(db.String(32), unique=True)


class ZhihuMetrics(db.Model):
    __tablename__ = 'ZhihuMetrics'
    id = db.Column(db.Integer, primary_key=True)
    hot_metrics = db.Column(db.String(64))
    hot_cardid = db.Column(db.String(32), index=True)
    update_time = db.Column(db.DateTime)


class ZhihuContent(db.Model):
    __tablename__ = 'ZhihuContent'
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, index=True)
    author = db.Column(db.String(32), index=True)
    voteup_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    reward_info = db.Column(db.Integer)
    content = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    phone = db.Column(db.Integer)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(64))
    gender = db.Column(db.SmallInteger, default=0)  # 默认为0：男
    active = db.Column(db.SmallInteger, default=0)  # 默认为0：正常

    @staticmethod
    def insert_users():
        users = User.query.filter_by(username="admin").first()
        if users:
            pass
        else:
            user = User(username="admin", password="admin")
            db.session.add(user)
            db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


