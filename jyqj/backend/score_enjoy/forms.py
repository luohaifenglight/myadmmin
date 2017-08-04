#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class ScoreEnjoyForm(forms.Form):
    """
    bkp pic form
    """

    name = forms.CharField(label=u'曲名', max_length=20, required=True)
    audio_name = forms.CharField(label=u'音频名称', max_length=100)
    audio_path = forms.CharField(label=u'音频路径', max_length=255)
    poster_name = forms.CharField(label=u'封面名称', max_length=100)
    poster_path = forms.CharField(label=u'封面路径', max_length=255)
    status = forms.BooleanField(label=u'是否发布', initial=False, required=False)

