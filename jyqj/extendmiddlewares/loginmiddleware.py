#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import QueryDict, HttpResponseRedirect
import re


def build_login_url(request):
    path = request.get_full_path()
    querystring = QueryDict(mutable=True)
    querystring['next'] = path
    url = reverse('accounts:login') + '?' + querystring.urlencode()
    return url


class LoginAuthenticationMiddleware(object):
    def process_request(self, request):
        path = request.path_info
        no_need_path = ['/accounts/login/',
                        '/wechart/bind/',
                        '/wechart/unbind/',
                        '/wechart/oncourse/',
                        '/wechart/offcourse/']
        compile_path = [re.compile(r) for r in no_need_path]
        for com in compile_path:
            if com.match(path):
                return
        if not request.user.is_authenticated():
            return HttpResponseRedirect(build_login_url(request))
        request.session.set_expiry(3600)  # reset session time-limit

