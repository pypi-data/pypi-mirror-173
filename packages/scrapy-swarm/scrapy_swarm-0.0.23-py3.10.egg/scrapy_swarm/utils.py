import datetime
import hashlib
import json
from json import JSONDecodeError

import six


class TextColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


def is_dict(string_content):
    """Try load string_content as json, if failed, return False, else return True."""
    try:
        json.loads(string_content)
    except JSONDecodeError:
        return False
    return True


def convert_bytes_to_str(data, encoding='utf-8'):
    """Convert a dict's keys & values from `bytes` to `str`
        or convert bytes to str"""
    if isinstance(data, bytes):
        return data.decode(encoding)
    if isinstance(data, dict):
        return dict(map(convert_bytes_to_str, data.items()))
    elif isinstance(data, tuple):
        return map(convert_bytes_to_str, data)
    return data


def fp(data):
    m = hashlib.md5()
    result = []
    if data is None:
        return None
    elif type(data) is not dict:
        result.append(str(data))
    else:
        for i in sorted(data):
            result.append(str(data[i]))
    s = "".join(result)
    m.update(s.encode("utf-8"))
    return m.hexdigest()


class CodeHelper:
    format = '%Y%m%d'

    @classmethod
    def now_code(cls):
        dt = datetime.datetime.now()
        return dt.strftime(cls.format)

    @classmethod
    def pre_code(cls, code):
        dt = datetime.datetime.strptime(code, cls.format) + datetime.timedelta(days=-1)
        return dt.strftime(cls.format)

    @classmethod
    def next_code(cls, code):
        dt = datetime.datetime.strptime(code, cls.format) + datetime.timedelta(days=1)
        return dt.strftime(cls.format)


def get_swarm_subclasses(cls):
    # mod_names = importlib.import_module('mgr.process.scrapy.hh')
    # 这个加不加载都无所谓了  scrapy 加载过了  直接遍历
    # importlib.import_module(path)
    result = []
    for sub in cls.__subclasses__():
        for i in sub.__subclasses__():
            result.append(i)
    return result


def get_spider_map(cls):
    result = {}
    spiders = get_swarm_subclasses(cls)
    for spider in spiders:
        if not hasattr(spider, 'name'):
            continue
        result[spider.name] = spider
    return result

