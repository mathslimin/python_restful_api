#!/usr/bin/env python2.7
#encoding: utf8
"""
@desc 这是一个命令行脚本的例子
"""

import sys
import logging
import logging.handlers
import time
import traceback
sys.path.append("../../")
LOG_FILE = "/tmp/example.log"
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="d", interval=1, backupCount=30) # 实例化handler
fmt = '[%(asctime)s %(levelname)s %(filename)s:%(lineno)s] - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('')    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)
from tornado.options import define, options

from tornado_api.command_line import CommandlineHandler


def get_all_index(application):
    index_list = application.mongodb.chengmi.cm_index.find()
    index_array = []
    for index in index_list:
        index_array.append(index)
    return index_array

def get_all_order(application):
    order_sql = "select user_id, buy_number, goods_id, create_time from xxx where 1"
    order_list = application.readdb.query(order_sql)
    return order_list

def main():
    try:
        """
        命令行既可以调用model，也可以在此文件中写函数，调用mongodb的方法
        application.mongodb.test.one_table.find()
        """
        application = CommandlineHandler()
        user_id = 131279
        title = ''
        content = 'xxxx'
        send_android_push = application.model('push').send_push_to_android(
            user_id, title, content)
        print send_android_push
        index_list = get_all_index(application)
        logging.error('记录一条错误日志')
        logging.info('info')
        logging.warn('warn')
        logging.debug('debug')
        print index_list
    except KeyboardInterrupt:
        logging.info('exit now')
        sys.exit(0)
    except Exception as err:
        traceback_string = traceback.format_exc()
        logging.error(str(err)+str(traceback_string))
        print str(err)+str(traceback_string)


if __name__ == '__main__':
    main()
