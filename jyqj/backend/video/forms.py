#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import VIDEO_TYPE


class VideoForm(forms.Form):
    """
    Video
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    video_path = forms.CharField(label=u'选择视频', max_length=200)
    video_name = forms.CharField(max_length=200, initial='', required=False)
    thumb_path = forms.CharField(label=u'缩略图路径', max_length=200, initial='', required=False)
    name = forms.CharField(label=u'名称', max_length=50)
    type = forms.ChoiceField(label=u'类型', choices=VIDEO_TYPE.choices, )
    status = forms.BooleanField(label=u'发布状态', initial=False, required=False)
    size = forms.FloatField(required=False)
    time = forms.FloatField(required=False)
