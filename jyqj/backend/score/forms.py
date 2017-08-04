#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import SCORE_TYPE, MUSIC_CATEGORY_TYPE, MUSIC_TYPE, WEAK_TYPE


class ScoreForm(forms.Form):
    """
    Score
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    name = forms.CharField(label=u'名称', max_length=20)
    music_category = forms.ChoiceField(label=u'音乐类型', choices=MUSIC_CATEGORY_TYPE.choices)
    ratio = forms.IntegerField(label=u'乐曲系数',)
    timbre = MultiChoiceNoValidateField(label=u'包含音色', initial='')
    keyboard = forms.CharField(label=u'包含声部', max_length=20, initial='000')
    score_type = forms.ChoiceField(label=u'曲谱类型', choices=SCORE_TYPE.choices, initial=0, required=False)
    weak_type = forms.ChoiceField(label=u'弱起类型', choices=WEAK_TYPE.choices, initial=0, required=False)
    music_type = forms.ChoiceField(label=u'演奏曲类型', choices=MUSIC_TYPE.choices, initial=0, required=False)
    xml_name = forms.CharField(label=u'曲谱XML', max_length=200, initial='', required=False)
    xml_path = forms.CharField(label=u'曲谱XML', max_length=200, initial='', )
    b00_name = forms.CharField(label=u'注册记忆B00', max_length=200, initial='', )
    b00_path = forms.CharField(label=u'注册记忆B00', max_length=200, initial='', )
    sample_midi_name = forms.CharField(label=u'示范MIDI', max_length=200, initial='', )
    sample_midi_path = forms.CharField(label=u'示范MIDI', max_length=200, initial='', )
    compare_midi_name = forms.CharField(label=u'纠错MIDI', max_length=200, initial='', )
    compare_midi_path = forms.CharField(label=u'纠错MIDI', max_length=200, initial='', )
    sample_audio_name = forms.CharField(label=u'示范音频', max_length=200, initial='', )
    sample_audio_path = forms.CharField(label=u'示范音频', max_length=200, initial='', )

    is_weak = forms.BooleanField(label=u'是否弱起', initial=False, required=False)
    is_repeat = forms.BooleanField(label=u'是否重复', initial=False, required=False)
    poster_name = forms.CharField(label=u'乐曲图片', max_length=200, initial='', required=False)
    poster_path = forms.CharField(label=u'乐曲图片', max_length=200, initial='', required=False)
    description = forms.CharField(label=u'乐曲描述', max_length=1000, initial='', required=False)
    status = forms.BooleanField(label=u'发布状态', initial=False, required=False)

class QnydScoreForm(forms.Form):
    name = forms.CharField(label=u'名称', max_length=20)
    staff1_name = forms.CharField(label=u'名称', max_length=20)
    staff1_score = ChoiceNoValidateField(label=u'选曲子')
    staff2_name = forms.CharField(label=u'名称', max_length=20, required=False)
    staff2_score = ChoiceNoValidateField(label=u'选曲子', required=False)
    staff3_name = forms.CharField(label=u'名称', max_length=20, required=False)
    staff3_score = ChoiceNoValidateField(label=u'选曲子', required=False)
    xml_name = forms.CharField(label=u'曲谱XML', max_length=200, initial='', )
    xml_path = forms.CharField(label=u'曲谱XML', max_length=200, initial='', )
    description = forms.CharField(label=u'乐曲描述', max_length=1000, initial='', required=False)
    status = forms.BooleanField(label=u'发布状态', initial=False, required=False)