#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import MultiChoiceNoValidateField, ChoiceNoValidateField


class ClassForm(forms.Form):
    teacher = ChoiceNoValidateField(label=u'授课教师', initial='')
    name = forms.CharField(label=u'班级名称', max_length=20, help_text='最多可输入12个字', initial='')
    course_system = ChoiceNoValidateField(label=u'可调用课程体系', initial='')