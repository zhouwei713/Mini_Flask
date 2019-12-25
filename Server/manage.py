# coding = utf-8
"""
@author: zhou
@time:2019/12/12 14:40
@File: manage.py
"""

import os
from app import create_app, scheduler
import logging


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.logger.debug('this is debug log')
app.logger.info('this is info log')


if __name__ != '__main__':
    # 如果不是直接运行，则将日志输出到 gunicorn 中
    scheduler.start()
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
