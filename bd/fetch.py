# encoding: utf-8
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import json
import time


@gen.coroutine
def async_fetch(url, data_type):

    try:
        start = time.time()
        res = yield AsyncHTTPClient().fetch(url)
        res_time = round((time.time() - start) * 1000, 4)  # 单位ms
        print ("{0}, {1}ms".format(url, res_time))
    except Exception, e:
        print e, url
        raise gen.Return('')
    if data_type in ('json', 'JSON'):
        raise gen.Return(json.loads(res.body))
    else:
        raise gen.Return(res.body)