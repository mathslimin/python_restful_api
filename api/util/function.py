#coding=utf-8
import bcrypt, os, string, random, hashlib, time, re, tornado.escape, datetime, base64, math, logging
import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from BeautifulSoup import BeautifulSoup
from collections import OrderedDict
import collections

def is_new(update_time):
    """
    @Desc: 计算section是不是新的
    """
    try:
        update_time = time.strftime('%Y%m%d', time.localtime(int(update_time)))
        now_time = time.strftime('%Y%m%d', time.localtime(time.time()))

        if (int(now_time) - int(update_time)) <= 3:
            return 1
        else:
            return 0
    except Exception as msg:
        logging.error(msg)
        return 0


def md5(str):
    '''
	计算简单的md5 hex格式字符串

	:param str: 原字符串
	:return: 返回的32尾hex字符串
	'''
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def humansize(file):
    '''
	计算文件大小并输出为可读的格式（如 1.3MB）

	:param file: 文件路径
	:return: 可读的文件大小
	'''
    if os.path.exists(file):
        nbytes = os.path.getsize(file)
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])
    else:
        return u"未知"


def humantime(t=None, format="%Y-%m-%d %H:%M:%S", span=False):
    '''

	%y 两位数的年份表示（00-99）
	%Y 四位数的年份表示（000-9999）
	%m 月份（01-12）
	%d 月内中的一天（0-31）
	%H 24小时制小时数（0-23）
	%I 12小时制小时数（01-12）
	%M 分钟数（00=59）
	%S 秒（00-59）

	%a 本地简化星期名称
	%A 本地完整星期名称
	%b 本地简化的月份名称
	%B 本地完整的月份名称
	%c 本地相应的日期表示和时间表示
	%j 年内的一天（001-366）
	%p 本地A.M.或P.M.的等价符
	%U 一年中的星期数（00-53）星期天为星期的开始
	%w 星期（0-6），星期天为星期的开始
	%W 一年中的星期数（00-53）星期一为星期的开始
	%x 本地相应的日期表示
	%X 本地相应的时间表示
	%Z 当前时区的名称
	%% %号本身

	:param t: 时间戳，默认为当前时间
	:param format: 格式化字符串
	:return: 当前时间字符串
	'''
    if not t:
        t = time.time()
    if span:
        return time_span(t)
    return time.strftime(format, time.localtime(t))


def time_span(ts):
    '''
	计算传入的时间戳与现在相隔的时间

	:param ts: 传入时间戳
	:return: 人性化时间差
	'''
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(ts)
    if delta.days >= 365:
        return '%d年前' % int(delta.days / 365)
    elif delta.days >= 30:
        return '%d个月前' % int(delta.days / 30)
    elif delta.days > 0:
        return '%d天前' % delta.days
    elif delta.seconds < 60:
        return "%d秒前" % delta.seconds
    elif delta.seconds < 60 * 60:
        return "%d分钟前" % int(delta.seconds / 60)
    else:
        return "%d小时前" % int(delta.seconds / 60 / 60)


def random_str(randomlength=12):
    '''
	获得随机字符串，包含所有大小写字母+数字

	:param randomlength: 字符串长度，默认12
	:return: 随机字符串
	'''
    a = list(string.ascii_letters + string.digits)
    random.shuffle(a)
    return ''.join(a[:randomlength])


def intval(str):
    '''
	如php中的intval，将字符串强制转换成数字

	:param str: 输入的字符串
	:return: 数字
	'''
    if type(str) is int: return str
    try:
        ret = re.match(r"^(\-?\d+)[^\d]?.*$", str).group(1)
        ret = int(ret)
    except:
        ret = 0
    return ret


def nl2br(str):
    str = tornado.escape.xhtml_escape(str)
    return str


def dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj = obj
    if '__dict__' in dir(obj):
        newobj = obj.__dict__
        if ' object at ' in str(obj) and not newobj.has_key('__type__'):
            newobj['__type__'] = str(obj)
        for attr in newobj:
            newobj[attr] = dump(newobj[attr])
    return newobj


def decrypt_access_token(access_token=''):
    """
    @把用户ID解密出来
    """
    if not access_token:
        return 0
    try:
        access_token = base64.b64decode(access_token)
        user_id = access_token.split('_')[-1]
        user_id = int(user_id)
    except Exception as msg:
        user_id = 0
    return user_id


def calcDistance(curlng, curlat, gaodelng, gaodelat):
    """
    计算两点之间的距离, 距离单位是米
    """
    R = 6370996.81
    if not curlng or not curlat:
        return 100000000
    try:
        curlng = float(curlng)
        curlat = float(curlat)
        gaodelng = float(gaodelng)
        gaodelat = float(gaodelat)

        dis = R * math.acos(math.cos(curlat * math.pi / 180) * math.cos(
            gaodelat * math.pi / 180) * math.cos(curlng * math.pi / 180 -
                                                 gaodelng * math.pi / 180) +
                            math.sin(curlat * math.pi /
                                     180) * math.sin(gaodelat * math.pi / 180))
        return int(dis)
    except Exception as msg:
        return 100000000


def get_city_name_by_id(city_id=0):
    """
    @Desc: 通过一个城市的id得到城市名称
    """
    city_code = {11: u'北京', 31: u'上海', 441: u'广州', 443: u'深圳'}

    if not city_code.has_key(int(city_id)):
        return 2000019

    return city_code[int(city_id)]


def get_city_short_by_id(city_id=0):
    """
    @Desc: 获取城市的缩写
    """
    city_code = {11: 'bj', 31: 'sh', 441: 'gz', 443: 'sz'}
    if not city_code.has_key(int(city_id)):
        return 2000019

    return city_code[int(city_id)]


def SortedDict(od):
    """
    @Desc: 对字典按照key进行排序
    """
    res = OrderedDict()
    for k, v in sorted(od.items()):
        if isinstance(v, dict):
            res[k] = SortedDict(v)
        elif isinstance(v, list):
            tmp = []
            for item in v:
                if isinstance(item, dict):
                    item = SortedDict(item)
                tmp.append(item)
            res[k] = tmp
        else:
            res[k] = v
    return res


def str_len(str):
    try:
        row_l = len(str)
        utf8_l = len(str.encode('utf-8'))
        return int((utf8_l - row_l) / 2 + row_l)
    except:
        return int(row_l)
    return int(row_l)

def rename(self,key,new_key):
    """
    字典对字段进行重命名
    dic = OrderedDict((("a",1),("b",2),("c",3)))
    print dic
    dic.rename("a","foo")
    """
    ind = self._keys.index(key)  #get the index of old key, O(N) operation
    self._keys[ind] = new_key    #replace old key with new key in self._keys
    self[new_key] = self[key]    #add the new key, this is added at the end of self._keys
    self._keys.pop(-1)           #pop the last item in self._keys

def filter_emoji(src_string=''):
    '''
    过滤表情
    '''
    if str(src_string).isdigit():
        return str(src_string)
    import re
    try:
        # UCS-4
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # UCS-2
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    # mytext = u'<some string containing 4-byte chars>'
    resovle_value = highpoints.sub(u'\u25FD', src_string)
    return resovle_value

def check_mobile_format(mobile):
    """
    检测手机号码正确性
    """
    mobile = str(mobile).replace('-', '')
    if len(str(mobile))<>11:
        return False
    if str(mobile).isdigit():
        if int(str(mobile)[0:1]) == 1:
            return True
    return False

def send_mail(to_mail, subject, mail_content):
    msg = MIMEMultipart()
    from_mail = "report@chengmi.com"
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject

    #添加邮件内容
    txt = MIMEText(mail_content)
    msg.attach(txt)

    #发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com:25')
    smtp.login('report@chengmi.com', 'Robot123')
    smtp.sendmail(from_mail, to_mail, msg.as_string())
    smtp.quit()

def strip_tags(some_string):
    text = text_with_newlines(some_string)
    return text

def text_with_newlines(some_string):
    elem = BeautifulSoup(some_string)
    text = ''
    for e in elem.recursiveChildGenerator():
        if isinstance(e, basestring):
            text += e.strip()
        elif e.name == 'br':
            text += '\n'
    return text


def convert_keys_to_string2(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v)) 
        for k, v in dictionary.items())

def convert_keys_to_string(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_keys_to_string, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_keys_to_string, data))
    else:
        return data
