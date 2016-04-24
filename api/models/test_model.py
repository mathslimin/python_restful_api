#-*- coding:utf-8 -*-
from base_model import BaseModel
from pymongo import ASCENDING, DESCENDING
import logging
import time
import simplejson
import json
import copy

from api.util.function import calcDistance, is_new

class Test_model(BaseModel):

    def get_article(self, article_id, is_delete=-1):
        '''
        通过article id获取article信息
        '''
        query = {"id": int(article_id)}
        if int(is_delete) != -1:
            query['is_delete'] = is_delete

        show_col = {
            "_id": 0,
            "id": 1,
            "city_id": 1,
            "user_id": 1,
            "cmsec_id": 1,
            "tag_ids": 1,
            "cmpoi_id": 1,
            "upoi_id": 1,
            "is_delete": 1,
            "newcontent": 1,
            "created_at": 1,
            "is_selected": 1,
            "like_count": 1,
            "comment_count": 1,
        }

        article = self.mongo_r.find_one('cm_article', query, show_col)
        return article