#!/usr/bin/env python
# -*- coding: utf-8 -*-

from viewmodel import UserCommand
from django.shortcuts import redirect, render


def has_perms(user, perms):
    user_perms = UserCommand.get_perms(user) if user else []
    return set(user_perms) & set(perms)

def perm_required(perms):
    def _perm_required(fn):
        def _wrapper(request, *args, **kwargs):
            if perms and not has_perms(request.user, perms):
                err_content = {
                    'title': u'出错了',
                    'errmsg': u'没有权限',
                }
                return render(request, 'error/403.html', err_content)
            return fn(request, *args, **kwargs)
        return _wrapper
    return _perm_required
