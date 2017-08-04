#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import MultiChoiceNoValidateField, ChoiceNoValidateField
from enumtype import ADMIN_DEPARTMENT


class RoleForm(forms.Form):
    """
    role
    """
    name = forms.CharField(label=u'名称', max_length=20, help_text='最多可输入120个字', initial='')
    permissions = MultiChoiceNoValidateField(label=u'权限')


class AdminForm(forms.Form):
    department = forms.ChoiceField(label=u'部门', choices=ADMIN_DEPARTMENT.choices, initial=ADMIN_DEPARTMENT.JIGOU)
    username = forms.CharField(label=u'用户名', max_length=20, help_text='最多可输入20个字', initial='')
    belong_groups = MultiChoiceNoValidateField(label=u'角色', initial='5', required=False)
    mobile = forms.CharField(label=u'手机号码', max_length=20, initial='')
    password = forms.CharField(label=u'初始密码', max_length=200, initial='')


class PasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原密码', max_length=50, initial='')
    new_password = forms.CharField(label=u'新密码', max_length=50, initial='')
    review_password = forms.CharField(label=u'重复新密码', max_length=50, initial='')

    def clean(self):
        data = self.cleaned_data
        if data.get('new_password', '') != data.get('review_password', ''):
            # self.add_error('new_password', u'两次输入密码不一致')
            self.add_error('review_password', u'两次输入密码不一致')