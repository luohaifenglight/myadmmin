#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect


t_dir = 'wechart/'


def bind(request):
    http_content = {
        'title': u'首页',
    }
    print 'GET:', request.GET
    return render(request, t_dir + 'account_bind.html', http_content)


def unbind(request):
    http_content = {
        'title': u'首页',
    }
    print 'GET:', request.GET
    return render(request, t_dir + 'account_unbind.html', http_content)


def oncourse(request):
    http_content = {
        'title': u'首页',
    }
    print 'GET:', request.GET
    return render(request, t_dir + 'oncourse.html', http_content)


def offcourse(request):
    http_content = {
        'title': u'首页',
    }
    print 'GET:', request.GET
    return render(request, t_dir + 'offcourse.html', http_content)
