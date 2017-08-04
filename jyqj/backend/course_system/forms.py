#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .enumtype import COURSE_SYSTEM_TYPE
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField


class CourseSystemForm(forms.Form):
    """
    coursesystem
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    background_image_name = forms.CharField(label=u'背景图', max_length=200, initial='')
    background_image_path = forms.CharField(label=u'背景图', max_length=200, initial='')
    name = forms.CharField(label=u'名称', max_length=200)
    desc = forms.CharField(label=u'描述', max_length=1000, initial='', required=False)
    course_system_type = forms.ChoiceField(label=u'课程体系类型', choices=COURSE_SYSTEM_TYPE.choices)
