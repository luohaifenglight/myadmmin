#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.messages.api import get_messages
from backend.accounts.perms import has_perms

from jinja2 import Environment, Markup, escape, evalcontextfilter


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){1}')


# @evalcontextfilter
# def nl2br(eval_ctx, value):
#     result = u'\n\n'.join(u'%s<br/>' % p for p in _paragraph_re.split(escape(value)))
#     if eval_ctx.autoescape:
#         result = Markup(result)
#     return result


def add_img_suffix(data, suf):
    if data:
        if '-' not in data:
            return data + suf
        return data
    return ''


def imgraw(data):
    return add_img_suffix(data, '-w')


def imgthumb(data):
    return add_img_suffix(data, '-thumb')


def environment(**options):
    options['line_comment_prefix'] = '##'
    env = Environment(**options)
    env.globals.update({
    #     # #### function #####
        'static': staticfiles_storage.url,
        'url': reverse,
    #     'int': int,
    #     'get_datetime': get_datetime,
    #     'selected_options': selected_options,
    #     'selected_tag_options': selected_tag_options,
          'get_messages': get_messages,  # for message framework
          'has_perms': has_perms,
    #     'str': str,
          'isinstance': isinstance,

          'list': list,
    #
    #     # #### variable #####
         'STATIC_URL': settings.STATIC_URL,
    #     'MEDIA_URL': settings.MEDIA_URL,
    #     'BACKEND_URL': settings.BACKEND,
    #     'DOCTOR_URL': settings.DOCTOR_URL,
    #     'SETTINGS': settings,
    #     'IMG_TYPE': IMG_TYPE,
     })
    env.filters.update({
         'jsonify': lambda data: json.dumps(data),
         'imgraw': imgraw,
         'imgthumb': imgthumb,
     })
    # env.filters.update({
    #     'nl2br': nl2br
    # })
    return env
