#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import INSTITUTION_TYPE, LEVEL_CATEGORY_TYPE


class BKPPicForm(forms.Form):
    """
    bkp pic form
    """
    name = forms.CharField(label=u'图片名称', max_length=20, required=True)
    element_num = forms.IntegerField(label=u'元素数', required=False)
    path = forms.CharField(label=u'图片路径', max_length=100, required=False)
    description = forms.CharField(label=u'描述', max_length=200, required=False)
    # status = forms.IntegerField(label=u'是否发布', required=True)
    status = forms.BooleanField(label=u'是否发布', initial=False, required=False)

    target_name = forms.CharField(label=u'目标名称', max_length=20, required=False)
    top_left_x = forms.IntegerField(label=u'左上x', required=False)
    top_left_y = forms.IntegerField(label=u'左上y', required=False)
    bottom_right_x = forms.IntegerField(label=u'右下x', required=False)
    bottom_right_y = forms.IntegerField(label=u'右下y', required=False)
    # target_audio_name = forms.CharField(label=u'关卡名称', max_length=100)
    # target_audio_path = forms.CharField(label=u'关卡名称', max_length=255)
    # desc_audio_name = forms.CharField(label=u'关卡名称', max_length=100)
    # desc_audio_path = forms.CharField(label=u'关卡名称', max_length=100)


class BKPTargetForm(forms.Form):
    """
    bkp pic form
    """

    target_name = forms.CharField(label=u'目标名称', max_length=20, required=False)
    target_audio_name = forms.CharField(label=u'目标音频名称', max_length=100)
    target_audio_path = forms.CharField(label=u'目标音频路径', max_length=255)
    desc_audio_name = forms.CharField(label=u'解析音频名称', max_length=100)
    desc_audio_path = forms.CharField(label=u'解析音频路径', max_length=255)
    description = forms.CharField(label=u'解析描述', max_length=200, required=False)


class BKPLevelForm(forms.Form):
    """
    bkp pic form
    """

    name = forms.CharField(label=u'关卡名称', max_length=20, required=True)
    type = forms.ChoiceField(label=u'关卡分类', choices=LEVEL_CATEGORY_TYPE.choices, required=True)
    seq = forms.IntegerField(label=u'关卡顺序', required=True)
    description = forms.CharField(label=u'关卡描述', max_length=200, required=False)
    bgm_name = forms.CharField(label=u'背景音乐名称', max_length=200, required=False)
    bgm_path = forms.CharField(label=u'背景音乐路径', max_length=200, required=False)
    status = forms.IntegerField(label=u'发布状态', required=False)
