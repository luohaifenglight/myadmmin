#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from django.http import HttpResponse, JsonResponse
import json
from django.core.cache import cache


def render_json(f):

    def decorated(request,*args,**kwargs):
        obj = f(request,*args,**kwargs)
        if isinstance(obj,dict):
            data = json.dumps(obj)
            response = HttpResponse(data)
            response["Content-Length"]=len(data)
            return response
        else:
            return obj

    return decorated


def cache_value(key, timeout=600):
    def _cache_value(fn):
        def _wrapper(*args, **kwargs):
            md5 = hashlib.md5()
            md5.update(args)
            md5.update(kwargs)
            k = '%s:%s' % (key, md5.hexdigest())
            value = cache.get(k)
            if value is not None:
                value = fn(*args, **kwargs)
                cache.set(k, value, timeout=timeout)
            return value
        return _wrapper
    return _cache_value


def json_http_response(result, status=200):
    return HttpResponse(json.dumps(result),
                        content_type="application/json; charset=UTF-8", status=status)
