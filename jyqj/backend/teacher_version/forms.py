#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import PUBLIC_TYPE, VERSION_TYPE


class TeacherVersionForm(forms.Form):
    """
    teacherverion
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    zip_path = forms.CharField(label=u'选择文件', max_length=200)
    zip_name = forms.CharField(max_length=200, initial='', required=False)
    version = forms.CharField(label=u'Res版本号', max_length=20)
    package_code = forms.CharField(label=u'App版本号', max_length=20)
    public_type = forms.ChoiceField(label=u'发布类型', choices=PUBLIC_TYPE.choices,  )
    version_type = forms.ChoiceField(label=u'版本类型', choices=VERSION_TYPE.choices, initial=VERSION_TYPE.SMALL)
    status = forms.BooleanField(label=u'发布状态', initial=False, required=False)
    size = forms.FloatField(required=False)
