#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from utils.forms import ChoiceNoValidateField, MultiChoiceNoValidateField
from enumtype import UNIT_TYPE, PLAY_WAY, GAME_TYPE, STAR_TYPE, KEYBOARD_TYPE


class UnitForm(forms.Form):
    """
    UNit
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    name = forms.CharField(label=u'单元名称', max_length=20)
    show_name = forms.CharField(label=u'显示名称', max_length=20)
    type = forms.ChoiceField(label=u'单元类型', choices=UNIT_TYPE.choices)
    description = forms.CharField(label=u'描述', initial='', max_length=200, required=False)


class SectionAudioForm(forms.Form):
    """
    audio
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    section_name = forms.CharField(label=u'名称', max_length=20)
    pic_name = forms.CharField(label=u'图片', initial='', max_length=200,)
    pic_path = forms.CharField(label=u'图片', initial='', max_length=100,)
    audio_name = forms.CharField(label=u'音频', initial='', max_length=200,)
    audio_path = forms.CharField(label=u'音频', initial='', max_length=255,)
    play_type = forms.ChoiceField(label=u'播放形式', choices=PLAY_WAY.choices)
    is_auto_play = forms.BooleanField(label=u'是否自动播放', initial=False, required=False)


class SectionVideoForm(forms.Form):
    """
    video
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    video = ChoiceNoValidateField(label=u'视频',)
    video_segment = ChoiceNoValidateField(label=u'视频分段', required=False)
    section_name = forms.CharField(label=u'名称', max_length=50)
    poster_name = forms.CharField(label=u'前poster', initial='', max_length=200, required=False)
    poster_path = forms.CharField(label=u'前poster', initial='', max_length=100, required=False)
    back_poster_name = forms.CharField(label=u'后poster', initial='', max_length=200, required=False)
    back_poster_path = forms.CharField(label=u'后poster', initial='', max_length=100, required=False)
    play_type = forms.ChoiceField(label=u'播放形式', choices=PLAY_WAY.choices)
    is_auto_play = forms.BooleanField(label=u'是否自动播放', initial=False, required=False)
    b00_name = forms.CharField(label=u'注册记忆B00', max_length=200, initial='', required=False)
    b00_path = forms.CharField(label=u'注册记忆B00', max_length=200, initial='', required=False)
    program_change_midi_name = forms.CharField(label=u'音色变换midi', max_length=200, initial='', required=False)
    program_change_midi_path = forms.CharField(label=u'音色变换midi', max_length=200, initial='', required=False)


class SectionSegmentForm(forms.Form):
    """
    segment
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    video = ChoiceNoValidateField(label=u'视频', )
    video_segment = ChoiceNoValidateField(label=u'视频分段', required=False)
    score = ChoiceNoValidateField(label=u'曲子', )
    score_segment = ChoiceNoValidateField(label=u'曲子分段', )
    section_name = forms.CharField(label=u'名称', max_length=20)
    keyboard = forms.ChoiceField(label=u'琴键', choices=KEYBOARD_TYPE.choices)
    tempo = forms.IntegerField(label=u'tempo')


class SectionFullForm(forms.Form):
    """
    full
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    score = ChoiceNoValidateField(label=u'曲子', )
    section_name = forms.CharField(label=u'名称', max_length=20)


class SectionHomeworkForm(forms.Form):
    """
    homework
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    section_name = forms.CharField(label=u'名称', max_length=20)


class SectionGameForm(forms.Form):
    """
    game
    """
    # institution = ChoiceNoValidateField(label=u'机构')
    level_id = ChoiceNoValidateField(label=u'关卡', )
    section_name = forms.CharField(label=u'名称', max_length=20)
    type = forms.ChoiceField(label=u'游戏类型', choices=GAME_TYPE.choices)


SECTION_TYPE_FORM = [

    SectionAudioForm, SectionVideoForm, SectionSegmentForm, SectionFullForm, \
    SectionHomeworkForm, SectionGameForm
]

