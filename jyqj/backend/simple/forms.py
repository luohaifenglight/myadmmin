#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField


class SimpleForm(forms.Form):
    """
    example
    """
    f1 = forms.CharField(label=u'字段一', max_length=20, help_text='最多可输入120个字', initial='')
    # f2 = forms.CharField(label=u'字段二', max_length=20, help_text='最多可输入120个字', initial='')
    f2 = ChoiceNoValidateField(label=u'医院', initial=None, required=False)
    f3 = forms.CharField(label=u'字段三', max_length=20, help_text='最多可输入120个字', initial='')
    f4 = forms.CharField(label=u'字段四', max_length=200, help_text='最多可输入120个字', initial='')
    f5 = forms.CharField(label=u'字段五', max_length=200, help_text='最多可输入120个字', initial='')
