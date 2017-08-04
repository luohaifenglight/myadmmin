#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField


class QnydScoreForm(forms.Form):
    name = forms.CharField(label=u'名称', max_length=20)
    staff1_name = forms.CharField(label=u'名称', max_length=20)
    whole_score = ChoiceNoValidateField(label=u'选择总谱')
    staff1_score = ChoiceNoValidateField(label=u'选曲子')
    staff2_name = forms.CharField(label=u'名称', max_length=20, required=False)
    staff2_score = ChoiceNoValidateField(label=u'选曲子', required=False)
    staff3_name = forms.CharField(label=u'名称', max_length=20, required=False)
    staff3_score = ChoiceNoValidateField(label=u'选曲子', required=False)
    description = forms.CharField(label=u'乐曲描述', max_length=1000, initial='', required=False)