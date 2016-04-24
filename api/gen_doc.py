#!/usr/bin/env python2.7

# ---- import the tornado api system library direction ----#
import sys
sys.path.append("../")

import json
import tornado.ioloop
from tornado_api.routes import get_routes
import tornado.web

from tornado_api.api_doc_gen import api_doc_gen
from tornado_api.constants import TORNADO_MAJOR
import redis
from pymongo import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference
import torndb
from tornado.options import define, options
from config import config


class Application(tornado.web.Application):
    """Entry-point for the app

    - Generate API documentation using provided routes
    - Initialize the application

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes for the app
    :type  settings: dict
    :param settings: Settings for the app
    :param  db_conn: Database connection
    """

    def __init__(self, routes, settings, options):
        # Generate API Documentation
        api_doc_gen(routes)


def main():
    import controller
    routes = get_routes(controller)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2))
    settings = {'debug': True,}
    # Create the application by passing routes and any settings
    application = Application(routes=routes, settings=settings, options=options)


if __name__ == '__main__':
    main()
