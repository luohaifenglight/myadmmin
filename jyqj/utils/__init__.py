import base64
import json


import hashlib
from datetime import datetime as date_time
import datetime
import time


def getformattime(timedel, fomat='%Y-%m-%d %H:%M:%S'):
    result_timedel = date_time.utcfromtimestamp(timedel + 28800)
    return result_timedel.strftime(fomat)


def upload_name(ext=None):
    prefix = str(int(time.time()))
    md5 = hashlib.md5(str(time.time()).encode("utf8")).hexdigest()[:10]
    md5 = prefix + '-' + md5
    if ext is not None:
        md5 = md5 + '.' + ext
    return md5


def dict_get(data, *args):
    for arg in args:
        data = data.get(arg, None)
        if data is None:
            return ""
    return data


def dict_get_int(data, *args):
    for arg in args:
        data = data.get(arg, None)
        if data is None:
            return 0
    return data


def pack(data):
    state = base64.urlsafe_b64encode(json.dumps(data).encode('utf8')).decode('utf8')
    return state


def unpack(state):
    data = base64.urlsafe_b64decode(state).decode("utf8")
    data = json.loads(data)
    return data


def string_bool(s):
    s = s.lower()
    if not s or s == 'false':
        return False
    return True


def split_one_char(s, delimiters):
    """equivalent re.split(delimiters, s)
    """
    split_delimiter = ','
    import string
    T = string.maketrans(delimiters, split_delimiter * len(delimiters))
    if type(s) == unicode:
        s = s.encode()
    split_list = s.translate(T).split(split_delimiter)
    return split_list

