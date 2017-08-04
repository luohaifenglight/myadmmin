#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from rest_framework import routers, serializers, viewsets
from utils.forms import ChoiceNoValidateField


_all__ = (
    'Field', 'CharField', 'IntegerField',
    'DateField', 'TimeField', 'DateTimeField', 'DurationField',
    'RegexField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'ComboField', 'MultiValueField', 'FloatField', 'DecimalField',
    'SplitDateTimeField', 'GenericIPAddressField', 'FilePathField',
    'SlugField', 'TypedChoiceField', 'TypedMultipleChoiceField', 'UUIDField',
)

class InstitutionForm(forms.Form):
    """
    example
    """
    f1 = forms.CharField(label=u'字段一', max_length=20, help_text='最多可输入120个字', initial='')
    f2 = forms.CharField(label=u'字段二', max_length=20, help_text='最多可输入120个字', initial='')
    # f2 = ChoiceNoValidateField(label=u'医院', initial=None, required=False)
    f3 = forms.CharField(label=u'字段三', max_length=20, help_text='最多可输入120个字', initial='')
    f4 = forms.CharField(label=u'字段四', max_length=200, help_text='最多可输入120个字', initial='')
    f5 = forms.CharField(label=u'字段五', max_length=200, help_text='最多可输入120个字', initial='')

class SublevelInfo(serializers.Serializer):
    """
    小关配置信息
    """
    id = serializers.CharField(label=u'小关id',required=False)
    level_id = serializers.CharField(label=u'所属大关id',required=False)

    sublevel_name = serializers.CharField(label=u'大关名字', max_length=20,required=True)
    sublevel_seq = serializers.CharField(label=u'关卡顺序', required=False)
    sublevel_description = serializers.CharField(label=u'关卡描述', max_length=200,required=False)

    sublevel_pitch_rate = serializers.CharField(label=u'音名占比', required=False)
    sublevel_sing_rate = serializers.CharField(label=u'唱名占比', required=False)
    sublevel_score_rate = serializers.CharField(label=u'五线谱占比', required=False)
    sublevel_hint_rate = serializers.CharField(label=u'有提示占比', required=False)

    sublevel_pitch = serializers.CharField(label=u'音名占比勾选', required=False,allow_blank=True)
    sublevel_sing = serializers.CharField(label=u'唱名占比勾选', required=False,allow_blank=True)
    sublevel_score = serializers.CharField(label=u'五线谱占比勾选', required=False,allow_blank=True)


    sublevel_pop_interval = serializers.CharField(label=u'气球出现速度',required=False )
    sublevel_fly_time = serializers.CharField(label=u'气球停留时间', required=False)
    sublevel_level_time = serializers.CharField(label=u'关卡时长', required=False)
    sublevel_bgm_name = serializers.CharField(label=u'背景音乐名称', max_length=20,required=False)
    sublevel_bgm_path = serializers.CharField(label=u'背景音乐路径', max_length=100,required=False)
    sublevel_bgp_name = serializers.CharField(label=u'背景图片名称', max_length=20,required=False)
    sublevel_bgp_path = serializers.CharField(label=u'背景图片路径', max_length=100,required=False)

    sublevel_status = serializers.CharField(label=u'关卡发布状态', required=False)

    # octave_type = serializers.CharField(label=u'音域类型', max_length=5,required=False)
    # keyboard_type = serializers.IntegerField(label=u'键盘类型', required=False)
    # c = serializers.IntegerField(label=u'c占比', required=False)
    # d = serializers.IntegerField(label=u'd占比', required=False)
    # e = serializers.IntegerField(label=u'e占比', required=False)
    # f = serializers.IntegerField(label=u'f占比', required=False)
    # g = serializers.IntegerField(label=u'g占比', required=False)
    # a = serializers.IntegerField(label=u'a占比', required=False)
    # b = serializers.IntegerField(label=u'b占比', required=False)