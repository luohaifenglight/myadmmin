#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
from decimal import Decimal

from django.db import models
from django.utils.html import escape


class DictMixin(object):
    """
    >> g1 = BackendGroup.objects.get(id=1)
    >> g1.to_dict(expands={'members': ['id', 'username', 'date_joined'], 'permssions': ['id', 'name', 'title']})
    """
    def to_dict(self, fields=None, excludes=None, expands=None):
        return to_dict(self, fields, excludes, expands)

SKIP_TYPES = (int, long, float, Decimal, type(None), bool, list, tuple, dict)


def _get_val(v):
    if isinstance(v, SKIP_TYPES):
        return v
    else:
        try:
            v = unicode(v)
        except:
            v = str(v)
        return escape(v)


def _fetch_related(obj, fields):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict(fields)
    else:
        if not fields:
            fields = ['id']
        return {f: _get_val(getattr(obj, f)) for f in fields}


def get_non_model_field_value(obj, field):
    fval = getattr(obj, field, None)
    if callable(fval):
        i = inspect.getargspec(fval)
        if len(i.args) == 1:
            fval = fval()
        else:
            fval = None
    return fval


def to_dict(obj, fields=None, excludes=None, expands=None):
    ret = {}
    model_fields = []
    for field in obj._meta.get_fields():
        field_name = field.name
        model_fields.append(field_name)
        if (excludes is not None and field_name in excludes) or \
                (fields is not None and field_name not in fields):
            # skip field that in the excludes or not in ther fields
            continue
        try:
            fval = getattr(obj, field_name, None)
        except:
            fval = None
        if not isinstance(field, models.fields.related.RelatedField) or not fval:
            # Basic Field, get value directly
            ret[field_name] = _get_val(fval)
        else:
            if expands is None or field_name not in expands.keys():
                if isinstance(field, models.ForeignKey):
                    ret[field_name] = fval.id if fval else None
                else:
                    # ManyToManyField
                    ret[field_name] = list(fval.values_list('id', flat=True))
            else:
                # need expand related object
                related_fields = expands[field_name]
                if isinstance(field, models.ForeignKey):
                    ret[field_name] = _fetch_related(fval, related_fields)
                else:
                    # ManyToManyField
                    ret[field_name] = [
                        _fetch_related(o, related_fields) for o in fval.all()
                    ]
    # access the field not a Model's Field
    if fields:
        for field_name in set(fields) - set(model_fields):
            field_list = field_name.split('__')
            if len(field_list) > 1:
                fval = obj
                for i in field_list:
                    if fval is None:
                        break
                    try:
                        fval = getattr(fval, i, None)
                    except:
                        break
            else:
                fval = get_non_model_field_value(obj, field_name)
            ret[field_name] = _get_val(fval)
    return ret
