# coding = utf-8
"""
@author: zhou
@time:2019/12/19 19:13
@File: __init__.py.py
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views