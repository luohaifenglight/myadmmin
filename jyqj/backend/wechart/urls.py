#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import bind, unbind, oncourse, offcourse
wechart_urls = [
    url(r'^bind/$', bind, name='bind'),
    url(r'^unbind/$', unbind, name='unbind'),
    url(r'^oncourse/$', oncourse, name='oncourse'),
    url(r'^offcourse/$', offcourse, name='offcourse'),
    ]
