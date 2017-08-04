#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Simple


class SimpleDB(DataBuilder):
    pass


class SimpleDQ(DataSQLQuery):
        model = Simple
        data_model = SimpleDB
        pass


class SimpleCommand:

    def __init__(self, data=None):
        self.data = data

    def simple_edit(self, simple_id=None):
        simple_info = self.data
        if simple_info is None:
            return None
        if simple_id is None:
            try:
                simple = Simple.objects.create(**simple_info)
            except IntegrityError:
                print 'error'
        else:
            try:
                simple = Simple.objects.get(id=simple_id)
            except:
                print 'error'

            for k, v in simple_info.iteritems():
                setattr(simple, k, v)
            simple.save()
        return simple.id

    def simple_get(self, simple_id):
        """
        GET LIST BY id
        """
        if simple_id is None:
            return None
        try:
            simple = Simple.objects.get(id=simple_id)
        except IntegrityError:
            print 'error'
        simple_data = to_dict(simple)
        return simple_data
