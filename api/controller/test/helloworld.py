#encoding: utf8
from tornado import gen
from tornado_api.requesthandlers import APIHandler
from tornado_api import schema
from tornado_api.gen import coroutine
from api.util.function import decrypt_access_token, intval
import json
import time
import logging
import sys
import os
sys.path.append("../../../../")

class RunHandler(APIHandler):

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "number", "desc": ""},
                "push_type": {
                    "type": "number", "desc":
                    "push_type 1表示需要发送push和cm_message, 2表示只发送cm_message, 3表示只发送push"
                },
                "title": {"type": "string", "desc":
                             "标题"},
                "content": {"type": "string", "desc": "内容"}
            },
            "required": ["user_id", "content", "title"]
        },
        input_example={
            "user_id": 131279,
            "title": "test",
            "content": "content",
            "push_to_mobile": 1,
            "push_type": 1
        },
        output_schema={},
        output_example="Hello world!")
    def run(self):
        user_id = intval(self.get_param('user_id', 0))
        title = self.get_param('title', '')
        content = self.get_param('content', '')
        push_type = int(self.get_param('push_type', 1))
        json_data = {}
        json_data['user_id'] = user_id
        json_data['title'] = title.encode('utf-8')
        json_data['content'] = content.encode('utf-8')
        json_data['push_type'] = push_type
        json_data['task_type'] = 'push'
        json_data['message_type'] = 1


        return json_data

    @coroutine
    def post(self):
        res = yield gen.Task(self.run)
        raise gen.Return(res)
