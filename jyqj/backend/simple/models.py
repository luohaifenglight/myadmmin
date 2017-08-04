#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Simple(models.Model):
    f1 = models.CharField(u'f1', max_length=20, default='')
    f2 = models.CharField(max_length=20, default='')
    f3 = models.CharField(max_length=20, default='')
    f4 = models.CharField(max_length=20, default='')
    f5 = models.CharField(max_length=20, default='')

    class Meta:
        db_table = 'tb_simple'