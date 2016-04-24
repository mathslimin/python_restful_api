# coding:utf8
import logging

from tornado.options import define, options
define("port", default=8700, type=int)
define("mysql_host", default="localhost:3306")
define("mysql_database", default="test")

define("mysql_user", default="root")
define("mysql_password", default="9800998ecf8427e")

define("process_num", default=100)
define("debug", default=True)
define("xsrf_cookies", default=False)
define("cookie_secret", default="test")

define('redis_port', default=6379, help="run on the give port", type=int)
define('redis_host', default='localhost', help="server host")
define('redis_pwd', default='', help="server password")
define('redis_db', default=0, help="")

#mongodb_write_host
define(
    "mongo_client",
    default=
    "localhost:27017",
    help="mongodb server")
define("mongo_repset",default="",help="repset if is use cluster")
define("mongo_user", default="admin", help="database user")
define("mongo_pwd", default="xxxx", help="database password")
define("mongo_dbname", default="test", help="database name")

define("log_dir", "/var/log/python/")
define("open_monitor", default=True, help="")
define("redis_monitor_key",default='MONITOR')
define("redis_error_key", default='ERROR')
define("redis_warning_key", default='WARNING')