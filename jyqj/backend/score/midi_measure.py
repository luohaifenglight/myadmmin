#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import mido
from mido import MidiFile


class MidiMeasure(object):
    def __init__(self, path=None):
        self.file_name, header = urllib.urlretrieve(path)

    def get_measure_count(self):
        midi_measure_data = "F0 43 70 70 78 00 00 F7"
        count = 0
        messages = MidiFile(self.file_name)
        for message in messages:
            if message.hex() == midi_measure_data:
                count = count + 1
        print count
        return count

    @classmethod
    def is_same(cls, smaple_midi_path, compare_midi_path):
        sample_mid_measure = cls(path=smaple_midi_path)
        sample_mid_count = sample_mid_measure.get_measure_count()
        compare_mid_measure = cls(path=compare_midi_path)
        compare_mid_count = compare_mid_measure.get_measure_count()
        if sample_mid_count == compare_mid_count:
            return True
        return False

# test

