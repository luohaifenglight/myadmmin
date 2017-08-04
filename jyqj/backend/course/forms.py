#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField


class CourseForm(forms.Form):
    """
    course
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    course_system = ChoiceNoValidateField(label=u'所属课程体系')
    name = forms.CharField(label=u'课程名称', max_length=50)
    description = forms.CharField(label=u'描述', initial='', max_length=20, required=False)
    seq = forms.IntegerField(label=u'课程顺序', initial=0)
    status = forms.BooleanField(label=u'是否发布', initial=False, required=False)
    keypoint_name = forms.CharField(label=u'内容梗概', max_length=200, initial='', required=False)
    keypoint_path = forms.CharField(label=u'内容梗概', max_length=200, initial='', required=False)
