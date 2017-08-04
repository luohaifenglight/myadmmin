#! /usr/bin/env python
# -*- coding: utf-8 -*-
from midi_measure import MidiMeasure
from musicxmlhelper import MusicXmlHelper
from utils.myredis import MyRedisConnector


def check_rule(compare_midi_path, sample_midi_path, xml_path, mear_sure_list=[]):
    sample_midi_count = MidiMeasure(path=sample_midi_path).get_measure_count()
    compare_midi_count = MidiMeasure(path=compare_midi_path).get_measure_count()
    if sample_midi_count != compare_midi_count:
        return -101
    for measure_num in mear_sure_list:
        if int(measure_num.get('end')) > compare_midi_count or int(measure_num.get('start')) > compare_midi_count:
            return -102
    xml = MusicXmlHelper(xml_path=xml_path)
    part_num = xml.get_all_parts_count()
    staff_num = xml.get_all_staff_num()
    print 'part, staff', part_num, staff_num
    if part_num > 2 or part_num > staff_num:
        return -103
    return 100


def clear_cache(score_id):
    key = 'tb_score_%s' % str(score_id)
    MyRedisConnector.delete(key)
    return True

