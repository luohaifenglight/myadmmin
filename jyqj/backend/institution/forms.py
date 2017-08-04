#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import INSTITUTION_TYPE
from backend.accounts.enumtype import ADMIN_DEPARTMENT

class InstitutionForm(forms.Form):
    """
    example
    """
    name = forms.CharField(label=u'机构名称', max_length=20,  initial='')
    code = forms.CharField(label=u'简码', max_length=20,  initial='')
    type = forms.ChoiceField(label=u'机构类型', choices=INSTITUTION_TYPE.choices)
    concurrent_num = forms.IntegerField(label=u'并发数')
    city = ChoiceNoValidateField(label=u'城市')
    experience_student_num = forms.IntegerField(label=u'体验学生数', min_value=0)
    course_system = MultiChoiceNoValidateField(label=u'可调用课程体系', initial='')


class AdminForm(forms.Form):
    department = forms.ChoiceField(label=u'部门', choices=ADMIN_DEPARTMENT.choices, initial=ADMIN_DEPARTMENT.JIGOU)
    username = forms.CharField(label=u'用户名', max_length=20, help_text='最多可输入20个字', initial='')
    mobile = forms.CharField(label=u'手机号码', max_length=20, initial='')
    password = forms.CharField(label=u'初始密码', max_length=200, initial='')
