#encoding:utf8

from tornado_api.db_pymongo import db_pymongo
from tornado_api.db_mysql import db_mysql
from tornado_api.requesthandlers import GLOBALS
import json
import logging
import pickle
from json import dumps, loads, JSONEncoder, JSONDecoder
from bson.objectid import ObjectId


class Encoder(json.JSONEncoder):

    '''def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj
    '''
    def default(self, obj):
        if isinstance(obj,
                      (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

class BaseModel(object):

    def __init__(self, userdb, wmongo, rmongo, redisdb, storedb):

        self._redisdb = redisdb
        self._userdb = userdb
        self._storedb = storedb
        self._wmongo = wmongo
        self._rmongo = rmongo
        self.chengmi_w = db_pymongo(wmongo)
        self.chengmi_r = db_pymongo(rmongo)
        self.mongo_w = self.chengmi_w
        self.mongo_r = self.chengmi_r
        self.chengmi_user_w = db_mysql(userdb)
        self.chengmi_user_r = db_mysql(userdb)
        self.storedb = db_mysql(storedb)
        self._model_storage = {
            'model': {},
            'wmongo': {},
            'rmongo': {},
            'userdb': {},
            'storedb': {},
            'redisdb': {}
        }

    @property
    def redisdb(self):
        global GLOBALS
        if int(GLOBALS['api_debug']) == 1:
            if 'count' not in GLOBALS:
                GLOBALS['count'] = {}
            else:
                if 'redis' not in GLOBALS['count']:
                    GLOBALS['count']['redis'] = {}
                    GLOBALS['count']['redis']['commands'] = 1
                else:
                    GLOBALS['count']['redis']['commands'] += 1

        return self._redisdb

    '''
    调用model
    '''

    def model(self, name):
        model_name = name.title() + 'Model'
        file_name = name + '_model'
        if model_name not in self._model_storage['model']:
            import_string = 'from %s import %s' % (file_name, model_name) + ''
            exec (import_string)
            self._model_storage['model'][model_name] = eval(model_name)(
                self._userdb, self._wmongo, self._rmongo, self._redisdb, self._storedb)
        return self._model_storage['model'][model_name]

    '''
    model 中的api_dump抛出一个用户自定义警告
    '''

    '''def api_dump(self, data):
        if isinstance(data, object):
            data = json.dumps(data,
                              cls=Encoder,
                              sort_keys=True,
                              indent=4,
                              ensure_ascii=False)

        raise GeneratorExit(data)
    '''
    def api_dump(self, data):
        if isinstance(data, object):
            data = json.dumps(data,
                              cls=Encoder,
                              sort_keys=True,
                              indent=4,
                              ensure_ascii=False).encode('utf-8')
        raise GeneratorExit(data)


    def api_trace(self, one_log):
        global GLOBALS
        if not GLOBALS or 'api_debug' not in GLOBALS or not GLOBALS['api_debug']:
            return
        if 'api_trace_log' not in GLOBALS:
            GLOBALS['api_trace_log'] = []
        GLOBALS['api_trace_log'].append(one_log)

    def log_merge_info(self, tablename='',keys={},values={}):
        """    
        @Desc: 纪录一个合并表的信息
        """
        try:
            rets = self.chengmi_r.find(tablename, keys, params=values)
            log_msg = []
            for ret in rets:
                log_msg.extend(ret.values())
            logging.info('tablename( %s) (userID: %s) has values(%s), ids(%s)'%(tablename, str(keys), len(log_msg), str(log_msg)))
        except Exception as msg:
            logging.error('query %s user(ID: %s) error(%s)'%(tablename, str(keys), msg))

