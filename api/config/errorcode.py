#encoding: utf8

error_list = {
    10001: {'message': 'Service Connect timeout',
            'desc': '服务连接超时',},
    10002: {'message': 'Service does not exists',
            'desc': '不存在的服务',},
    10003: {'message': 'Remote service error',
            'desc': '远程服务器异常',},
    10004: {'message': 'Api does not exists',
            'desc': '不存在的接口',},
    10005: {'message': 'Script error',
            'desc': '脚本异常',},
    10006: {'message': 'Framework exception', 'desc': '框架内部代码异常'},
    10007: {
        'message': 'App requests out of rate limit', 'desc': '访问超过服务允许的上限'
    },
    10008: {'message': 'Auth error', 'desc': '通讯认证失败'},
    10009: {'message': 'Protocol error', 'desc': '传输协议错误'},
    10010: {'message': 'Client exception', 'desc': '客户端内部异常'},
    10011: {'message': 'Application authorization failure', 'desc': '应用授权失败'},
    10012: {'message': 'System is upgrading', 'desc': '系统正在升级中...'},
    10013: {'message': 'exception', 'desc': '程序内部异常'},
    10014: {'message': 'Api Data Debug', 'desc': '数据调试'},
    10016: {'message': 'components does not exists', 'desc': '组件 % 不存在'},
    10017: {'message': 'app_id is null', 'desc': 'app_id不能为空'},
    10018: {'message': 'app_id  exception', 'desc': 'Api接口服务异常'},
    10019: {'message': 'app_id is unregister', 'desc': 'client端尚未注册或已被停止使用'},
    10020: {'message': 'ip limited access', 'desc': '服务器IP % 访问API受限'},
    10021: {'message': 'command has error %', 'desc': 'command有错误%'},
    10022: {'message': 'sign is not right', 'desc': '签名不正确'},
    10023: {'message': 'require Parameter  Is Null', 'desc': '参数不能为空'},
    10025: {'message': 'paramter %s is not valid', 'desc': '参数%s验证失败'},
    10027: {'message': 'paramter is not valid', 'desc': '参数验证失败'},
    10028: {'message': 'phone number is not correct', 'desc': '手机号码格式不对'},
    10029: {'message': 'user_id can not be none', 'desc': '请先登录'},
    10030: {'message': 'email is not correct', 'desc': '邮箱格式不对'},
    10031: {
        'message': 'return json format %s is wrong', 'desc': '返回json格式%s错误'
    },
    #应用报错
    2000001: {'message': 'category %s is not exists', 'desc': '分类 %s 不存在!'}
}
