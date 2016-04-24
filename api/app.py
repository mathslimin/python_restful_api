#encoding: utf8
#!/usr/bin/env python2.7

# ---- import the tornado api system library direction ----#
import sys
reload(sys)
sys.setdefaultencoding('utf8')# pylint: disable=no-member
sys.path.append("../")
import json
import logging
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.netutil
import tornado.process

from tornado.options import define, options

from tornado_api.routes import get_routes
from tornado_api.application import Application
import time
import os
import signal
from config import config

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 10    #在接收到kill信号的时候停留多少秒


def sig_handler(sig, frame):
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    logging.info('%sCaught signal: %s', now_time, sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    tornado.ioloop.IOLoop.instance().stop()    # 不接收新的 HTTP 请求
    logging.info('Will shutdown in %s seconds ...',
                 MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        #if now < deadline and (io_loop._callbacks or io_loop._timeouts):
        if now < deadline:
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
            io_loop.add_timeout(now + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN, stop_loop)
        else:
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
            logging.info('Already Shutdown'+now_time)
            io_loop.stop()    # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环

    stop_loop()


def main():
    import controller
    routes = get_routes(controller)
    '''print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2))
    '''
    settings = {'debug': options.debug}
    # Create the application by passing routes and any settings
    tornado.options.options.logging = "debug"    #纪录日志的级别
    date_file = time.strftime('%Y-%m-%d') + '.log'
    log_save_dir = options.log_dir + "/"
    if os.path.isdir(log_save_dir) == False:
        os.mkdir(log_save_dir, 0777)
    log_file = os.path.join(log_save_dir, date_file)
    args = sys.argv
    args.append("--log_file_prefix=" + log_file)
    tornado.options.parse_command_line(args)
    application = Application(routes=routes, settings=settings, options=options)
    env_msg = "environment = " + os.environ['PYTHON_ENVIRONMENT']
    msg = "* "+env_msg+" Running on http://localhost:" + str(
        options.port) + "/ (Press CTRL+C to quit)"
    print msg
    logging.info(msg)
    application.listen(options.port)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    logging.info(now_time+'Exit')


if __name__ == '__main__':
    main()
