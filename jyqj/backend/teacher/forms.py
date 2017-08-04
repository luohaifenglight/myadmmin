#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import GENDER_TYPE


class TeacherForm(forms.Form):
    """
    teacher
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    city = ChoiceNoValidateField(label=u'城市')
    name = forms.CharField(label=u'名称', max_length=20)
    mobile = forms.CharField(label=u'电话', max_length=20)
    school_area = forms.CharField(label=u'学校区域', max_length=20)
    course_system = MultiChoiceNoValidateField(label=u'可调用课程体系', initial='')
