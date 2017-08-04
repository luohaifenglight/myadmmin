#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.accounts.models import Admin, BackendModule

import time


class OperationLog(models.Model):
    admin = models.ForeignKey(Admin, blank=True, null=True)
    visitor_ip = models.CharField(max_length=20, blank=True, null=True)
    visit_time = models.BigIntegerField(default=int(time.time()), blank=True, null=True)
    operation_path = models.CharField(max_length=20, blank=True, null=True)
    action = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'tb_operation_log'
