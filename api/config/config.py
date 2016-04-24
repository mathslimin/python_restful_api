#coding:utf-8
from __future__ import absolute_import
import os
import logging
from tornado.options import define, options
from .config_local import *

'''
if 'PYTHON_ENVIRONMENT' not in os.environ['PYTHON_ENVIRONMENT']:
    from .config_local import *
else:
    env_msg = "environment = " + os.environ['PYTHON_ENVIRONMENT']
    print env_msg
    logging.info(env_msg)
    if os.environ['PYTHON_ENVIRONMENT'] == 'local':
        from .config_local import *
    elif os.environ['PYTHON_ENVIRONMENT'] == 'test':
        from .config_test import *    #local 表示本地，test表示测试环境，online表示线上环境
    elif os.environ['PYTHON_ENVIRONMENT'] == 'online':
        from .config_online import *    #local 表示本地，test表示测试环境，online表示线上环境
    else:
        from .config_online import *    #local 表示本地，test表示测试环境，online表示线上环境

'''