# -*- coding: utf-8 -*-
import urllib 
import logging
import copy
import socket
import time
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class MusicXmlHelper(object):
    """
    parse the musicxml file
    """

    def __init__(self, xml_path):
        socket.setdefaulttimeout(10.0)
        self.file_name, header = urllib.urlretrieve(xml_path)
        self.tree = ET.ElementTree(file=self.file_name)

        self.pic_width = 3508.0
        self.pic_height = 2480.0
        self.settings = self.get_settings()
        self.x_ratio = self.settings['x_ratio']
        self.y_ratio = self.settings['y_ratio']


    def get_default_info(self):
        """get default page and system info"""

        page_info = dict()
        system_info = dict()
        appearance = dict()
        default_info = dict(page_info=dict(), system_info=dict(), staff_distance=0, appearance=dict())

        # set page info
        page_info['page_height'] = int(self.tree.find("defaults/page-layout/page-height").text)
        page_info['page_width'] = int(self.tree.find("defaults/page-layout/page-width").text)
        page_info['left_margin'] = int(self.tree.find("defaults/page-layout/page-margins/left-margin").text)
        page_info['right_margin'] = int(self.tree.find("defaults/page-layout/page-margins/right-margin").text)
        page_info['top_margin'] = int(self.tree.find("defaults/page-layout/page-margins/top-margin").text)
        page_info['bottom_margin'] = int(self.tree.find("defaults/page-layout/page-margins/bottom-margin").text)

        # set system info
        system_info['left_margin'] = int(self.tree.find("defaults/system-layout/system-margins/left-margin").text)
        system_info['right_margin'] = int(self.tree.find("defaults/system-layout/system-margins/right-margin").text)
        system_info['system_distance'] = int(self.tree.find("defaults/system-layout/system-distance").text)
        system_info['top_system_distance'] = int(self.tree.find("defaults/system-layout/top-system-distance").text)

        # set staff distance info
        item = self.tree.find("defaults/staff-layout/staff-distance")
        if item is not None:
            staff_distance = int(item.text)
        else:
            staff_distance = 0
        # set appearance info
        appearance['light_barline'] = float(self.tree.find('defaults/appearance/line-width[@type="light barline"]').text)

        default_info = dict(page_info=page_info, system_info=system_info, staff_distance=staff_distance, appearance=appearance)

        return default_info

    def get_settings(self):

        page_width = int(self.tree.find("defaults/page-layout/page-width").text)
        page_height = int(self.tree.find("defaults/page-layout/page-height").text)
        x_ratio = self.pic_width / page_width 
        y_ratio = self.pic_height / page_height 

        line_width = float(self.tree.find('defaults/appearance/line-width[@type="light barline"]').text)

        parts = self.get_all_parts()
        clef_list = []
        for part in parts:
             clefs = self.tree.findall('part[@id="%s"]/measure/attributes/clef' % part['id']) 
             for clef in clefs:
                 sign = clef.find('sign').text
                 line = clef.find('line').text
                 clef_list.append(sign+line)

        pid = "P1"
        attributes = self.tree.find('part[@id="%s"]/measure/attributes' % pid)
        divisions = int(attributes.find("divisions").text)
        beat_num =int(attributes.find("time/beats").text)
        beat_type =int(attributes.find("time/beat-type").text)
        tempo = int(self.tree.find('part[@id="%s"]/measure/sound' % pid).attrib['tempo'])
        beat_time = 60.0/tempo 

        settings = dict(x_ratio=x_ratio, y_ratio=y_ratio, space_width=4.5, line_width=line_width, clef_list=clef_list,\
                        beat_num=beat_num, beat_type=beat_type, beat_time=beat_time)

        return settings

    def get_attributes(self, pid):
        """ get attributes info by part id"""

        attributes = self.tree.find('part[@id="%s"]/measure/attributes' % pid)

        divisions = int(attributes.find("divisions").text)

        beats =int(attributes.find("time/beats").text)
        beat_type =int(attributes.find("time/beat-type").text)
        time = dict(beats=beats, beat_type=beat_type)

        clef_list = []
        clefs =attributes.findall("clef")
        for item in clefs:
            sign = item.find("sign").text
            line = item.find("line").text
            clef = sign+line
            clef_list.append(clef)

        tempo = int(self.tree.find('part[@id="%s"]/measure/sound' % pid).attrib['tempo'])

        attributes = dict(divisions=divisions, time=time, clefs=clef_list, tempo=tempo)

        return attributes


    def get_staff_num(self, pid, mid):
        """get staff numbers by part number and measure number"""

        staff_num = 1
        s = []

        staffs = self.tree.findall('part[@id="%s"]/measure[@number="%s"]/note/staff'% (pid, mid))
        for item in staffs:
            s.append(item.text)
        if len(list(set(s))) > 0:
            staff_num = len(list(set(s)))

        return staff_num

    def get_all_staff_num(self):
        """get staff numbers by part number and measure number"""

        staff_num = 1
        s = []

        staffs = self.tree.findall('part/measure/note/staff')
        for item in staffs:
            s.append(item.text)
        if len(list(set(s))) > 0:
            staff_num = len(list(set(s)))

        return staff_num

    def get_page_info_by_mid(self, pid, mid, page_info, default):
        """get current page type by pid, mid"""

        # ptype: 0-in page, 1-first page, 2-new page
        # mtype: 0-in measure, 1-first measure, 2-new system measure


        pinfo = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print'% (pid, mid))

        if pinfo is None:
            page_info['ptype'] = 0  # in page
            page_info['mtype'] = 0  # in measure

            start_st = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, 1))
            if start_st is None:
                page_info['staff_distance'] = default['staff_distance'] 
            else:
                page_info['staff_distance'] = int(start_st.text)
        else:
            if pinfo.attrib.has_key('new-page') and pinfo.attrib['new-page'] == "yes":
                page_info['ptype'] = 2  # new page
                page_info['mtype'] = 1  # first measure
                page_info['left_margin'] = default['page_info']['left_margin']
                page_info['top_margin'] = default['page_info']['top_margin']

                tp = self.tree.find('part/measure[@number="%s"]/print/system-layout/top-system-distance'% mid)
                if tp is not None:
                    page_info['top_system_distance'] = int(tp.text)
                else:
                    page_info['top_system_distance'] = default['system_info']['top_system_distance']

                st = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid))
                if st is not None:
                    page_info['staff_distance'] = int(st.text)
                else:
                    page_info['staff_distance'] = default['staff_distance']
            else:
                if pinfo.attrib.has_key('new-system') and pinfo.attrib['new-system'] == "yes":
                    page_info['ptype'] = 0  # in page
                    page_info['mtype'] = 2 # new system measure
                    system = self.tree.find('part/measure[@number="%s"]/print/system-layout/system-distance'% mid)
                    if system is not None:
                        page_info['system_distance'] = int(self.tree.find('part/measure[@number="%s"]/print/system-layout/system-distance'% mid).text)
                    else:
                        page_info['system_distance'] = default['system_info']['system_distance'] 

                    staff = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid))
                    if staff is not None:
                        page_info['staff_distance'] = int(self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid)).text)
                    else:
                        page_info['staff_distance'] = default['staff_distance'] 

                else:
                    page_info['ptype'] = 1  # first page
                    page_info['mtype'] = 1 # first measure
                    page_info['top_system_distance'] = int(self.tree.find('part/measure[@number="%s"]/print/system-layout/top-system-distance'% mid).text)
                    sd = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid))
                    if sd is not None:
                        page_info['staff_distance'] = int(self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid)).text)
                    else:
                        page_info['staff_distance'] = default['staff_distance'] 

                    pl = self.tree.find('part/measure[@number="%s"]/print/page-layout'% mid)
                    if pl is not None:
                        page_info['page_height'] = int(pl.find('page-height').text)
                        page_info['page_width'] = int(pl.find('page-width').text)
                        page_info['left_margin'] = int(pl.find('page-margins/left-margin').text)
                        page_info['top_margin'] = int(pl.find('page-margins/top-margin').text)
                    else:
                        page_info['page_height'] = default['page_info']['page_height']
                        page_info['page_width'] = default['page_info']['page_width']
                        page_info['left_margin'] = default['page_info']['left_margin']
                        page_info['top_margin'] = default['page_info']['top_margin']

        return page_info

    def get_staff_distance(self, mid=None, pid=None):
        """get staff distance"""

        staff_distance = 0

        default = self.tree.find("defaults/staff-layout/staff-distance")
        if default is not None:
            staff_distance = int(default.text)

        if pid is not None:
            d = self.tree.find('part[@id="%s"]/measure[@number="%s"]/print/staff-layout/staff-distance'% (pid, mid))
            if d is not None:
                staff_distance = int(d.text)

        return staff_distance

    def get_measure_repeat_flag(self, mid, pid):
        """get staff distance"""


        is_repeat_forward = 0
        is_repeat_backward = 0

        repeat = self.tree.find('part[@id="%s"]/measure[@number="%s"]/barline/repeat'% (pid, mid))
        if repeat is not None:
            if repeat.get('direction') == "forward":
                is_repeat_forward = 1
            if repeat.get('direction') == "backward":
                is_repeat_backward = 1

        return is_repeat_forward, is_repeat_backward
    
    def get_all_parts(self):
        """get all parts from music xml file."""

        plist = []

        parts = self.tree.iterfind('part-list/score-part')
        for item in parts:
            plist.append(item.attrib)

        return plist

    def get_all_parts_count(self):
        return len(self.get_all_parts())

    def get_tempo_by_part(self, pid):
        """get divisions value in measure 1 by part."""

        slist = []
        sounds = self.tree.iterfind('part[@id="%s"]/measure/direction/sound'% pid)
        for item in sounds:
            if item.attrib.has_key('tempo'):
                slist.append(int(item.attrib['tempo']))

        if len(slist) == 0:
            sounds = self.tree.iterfind('part[@id="%s"]/measure/sound'% pid)
            for item in sounds:
                if item.attrib.has_key('tempo'):
                    slist.append(int(item.attrib['tempo']))

        return slist[0]

    def get_divisions_by_part(self, pid):
        """get divisions value in measure 1 by part."""

        dlist = []
        divisions = self.tree.iter(tag='divisions')
        for item in divisions:
            dlist.append(item.text)

        if pid == 'P1':
            return int(dlist[0])
        if pid == 'P2':
            return int(dlist[1])

    def get_measures_by_part(self, pid):
        """get all measures by part id."""

        mlist = []

        measures = self.tree.findall('part[@id="%s"]/measure'% pid)
        return measures

    def get_measure_left_margin(self, is_start, pages):

        start_measure_margin = 1000
        default_measure_margin = 1000
        for page in pages:
            for m in page:
                notes = m['staff1'] + m['staff2'] + (m['staff3'])
                notes.sort(key=lambda k: (k.get('x', 0)))
                if m['is_start'] == 1:  # first measure in line
                    if notes[0]['defaultx'] < start_measure_margin:
                        start_measure_margin = notes[0]['defaultx']
                else:
                    if notes[0]['defaultx'] < default_measure_margin:
                        default_measure_margin = notes[0]['defaultx']
        if is_start == 1:
            return start_measure_margin
        else:
            return default_measure_margin

    def get_measure_right_margin(self, pages):

        start_measure_margin = 1000
        default_measure_margin = 1000
        for page in pages:
            for m in page:
                notes = m['staff1'] + m['staff2'] + (m['staff3'])
                notes.sort(key=lambda k: (k.get('x', 0)))
                if m['is_start'] == 1:  # first measure in line
                    if notes[0]['defaultx'] < start_measure_margin:
                        start_measure_margin = notes[0]['defaultx']
                else:
                    if notes[0]['defaultx'] < default_measure_margin:
                        default_measure_margin = notes[0]['defaultx']
        if is_start == 1:
            return start_measure_margin
        else:
            return default_measure_margin


    def get_notes_by_mpid(self, mid, pid):
        """get all notes by measure id part id."""

        nlist = []

        notes = self.tree.iterfind('part[@id="%s"]/measure[@number="%s"]/note'% (pid, mid))

        return notes

    def formate_note_info(self, note):
        """ formate note object to note dict."""

        p = dict(step="", octave=0, alter=0)
        n = dict(ntype=0, start=0, end=0, duration=0, pitch=p, staff=0, defaultx=0, defaulty=0, accidental="")

        staff = note.find("staff")

        if staff is None:
            n['staff'] = 1
        else:
            n['staff'] = int(staff.text)
        rest = note.find('rest')
        if note.attrib.has_key("default-x") and rest is None:
            n['ntype'] = 0  # 0-normal note, 1-rest note, 2-rest meassure, 3-not,print
            n['defaultx'] = int(note.attrib['default-x'])
            n['duration'] = int(note.find('duration').text)
            n['dtype'] = note.find('type').text
            pitch = note.find('pitch')
            n['pitch']['step'] = pitch.find('step').text
            n['pitch']['octave'] = pitch.find('octave').text
            if pitch.find('alter') is not None: # 升降处理
                n['pitch']['alter'] = int(pitch.find('alter').text)
                accidental = note.find('accidental')
                if accidental is not None:    # C大调，临时升降
                    if accidental.text == "sharp":
                        n['accidental'] = "#"
                    elif accidental.text == "flat":
                        n['accidental'] = "b"
                    elif accidental.text == "natural":
                        n['accidental'] = ""
                else:  # G/F大调，整体升降
                    if  n['pitch']['alter'] == 1:  # G大调
                        n['accidental'] = "#"
                    if  n['pitch']['alter'] == -1:  # F大调
                        n['accidental'] = "b"
        else:
            if rest is not None:
                if rest.attrib.has_key("measure"):
                    n['ntype'] = 2  # 0-normal note, 1-rest note, 2-rest meassure, 3-not print
                    n['duration'] = int(note.find('duration').text)
                else:
                    n['ntype'] = 1  # 0-normal note, 1-rest note, 2-rest meassure, 3-not print
                    n['dtype'] = note.find('type').text
                    n['duration'] = int(note.find('duration').text)
                    n['defaultx'] = int(note.attrib['default-x'])
            else:
                n['ntype'] = 3 # 0-normal note, 1-rest note, 2-rest meassure, 3-not print
                n['duration'] = int(note.find('duration').text)
                n['dtype'] = note.find('type').text
                pitch = note.find('pitch')
                n['pitch']['step'] = pitch.find('step').text
                n['pitch']['octave'] = pitch.find('octave').text
                if pitch.find('alter'):
                    accidental = note.find('accidental').text
                    if accidental == "sharp":
                        accidental = "#"

        return n

    def get_step_y_in_score(self, note, line_width, clef, score_type=0):
        """ get the note step' y value in score."""
        n = 4.5
        #m = 0.5
        #m = 0.7487
        m = line_width
        step = note['pitch']['step']
        octave = int(note['pitch']['octave'])

        if note['ntype'] == 1: # rest note 
            return 1 * n + 1 * m
        if note['ntype'] == 2: # rest measure
            return 2 * n + 2 * m

        if score_type == 1:  # 一线谱
            if step == "C":
                return -1 * n
            elif step == "A":
                return 1 * n
            else:
                print "------------step OOPS."
        elif score_type == 0:  # 五线谱
            if clef == "G2":
                if octave == 2:
                    if step == "C":
                        return 24 * n + 12 * m
                    if step == "D":
                        return 23 * n + 12 * m
                    if step == "E":
                        return 22 * n + 11 * m
                    if step == "F":
                        return 21 * n + 11 * m
                    if step == "G":
                        return 20 * n + 10 * m
                    if step == "A":
                        return 19 * n + 10 * m
                    if step == "B":
                        return 18 * n + 9 * m
                if octave == 3:
                    if step == "C":
                        return 17 * n + 9 * m
                    if step == "D":
                        return 16 * n + 8 * m
                    if step == "E":
                        return 15 * n + 8 * m
                    if step == "F":
                        return 14 * n + 7 * m
                    if step == "G":
                        return 13 * n + 7 * m
                    if step == "A":
                        return 12 * n + 6 * m
                    if step == "B":
                        return 11 * n + 6 * m
                if octave == 4:
                    if step == "C":
                        return 10 * n + 5 * m
                    if step == "D":
                        return 9 * n + 5 * m
                    if step == "E":
                        return 8 * n + 4 * m
                    if step == "F":
                        return 7 * n + 4 * m
                    if step == "G":
                        return 6 * n + 3 * m
                    if step == "A":
                        return 5 * n + 3 * m
                    if step == "B":
                        return 4 * n + 2 * m
                if octave == 5:
                    if step == "C":
                        return 3 * n + 2 * m
                    if step == "D":
                        return 2 * n + 1 * m
                    if step == "E":
                        return 1 * n + 1 * m
                    if step == "F":
                        return 0 * n + 0 * m
                    if step == "G":
                        return -1*(1 * n + 1 * m)
                    if step == "A":
                        return -1*(2 * n + 1 * m)
                    if step == "B":
                        return -1*(3 * n + 2 * m)
                if octave == 6:
                    if step == "C":
                        return -1*(4 * n + 2 * m)
                    if step == "D":
                        return -1*(5 * n + 3 * m)
            elif clef == "F4":
                if octave == 2:
                    if step == "C":
                        return 12 * n + 6 * m
                    if step == "D":
                        return 11 * n + 6 * m
                    if step == "E":
                        return 10 * n + 5 * m
                    if step == "F":
                        return 9 * n + 5 * m
                    if step == "G":
                        return 8 * n + 4 * m
                    if step == "A":
                        return 7 * n + 4 * m
                    if step == "B":
                        return 6 * n + 3 * m
                if octave == 3:
                    if step == "C":
                        return 5 * n + 3 * m
                    if step == "D":
                        return 4 * n + 2 * m
                    if step == "E":
                        return 3 * n + 2 * m
                    if step == "F":
                        return 2 * n + 1 * m
                    if step == "G":
                        return 1 * n + 1 * m
                    if step == "A":
                        return 0 * n + 0 * m
                    if step == "B":
                        return -1 * (1 * n + 1 * m)
                if octave == 4:
                    if step == "C":
                        return -1 * (2 * n + 1 * m)
                    if step == "D":
                        return -1 * (3 * n + 2 * m)
                    if step == "E":
                        return -1 * (4 * n + 2 * m)
                    if step == "F":
                        return -1 * (5 * n + 3 * m)
                    if step == "G":
                        return -1 * (6 * n + 3 * m)
                    if step == "A":
                        return -1 * (7 * n + 4 * m)
                    if step == "B":
                        return -1 * (8 * n + 4 * m)
                if octave == 5:
                    if step == "C":
                        return -1 * (9 * n + 5 * m)
                    if step == "D":
                        return -1 * (10 * n + 5 * m)
                    if step == "E":
                        return -1 * (11 * n + 6 * m)
                    if step == "F":
                        return -1 * (12 * n + 6 * m)
                    if step == "G":
                        return -1 * (13 * n + 7 * m)
                    if step == "A":
                        return -1 * (14 * n + 7 * m)
                    if step == "B":
                        return -1 * (15 * n + 8 * m)

            else:
                print "-----------Clef OOPS----------------"

    def handle_note_accidental(self, pages):

        for i in range(len(pages)):
            for j in range(len(pages[i])):
                measure = pages[i][j]
                #handle staff1
                accidentals = []
                for k in range(len(measure['staff1'])):
                    note = measure['staff1'][k]
                    if note['pitch']['alter'] == 1:
                        if note['accidental'] != "":
                            accidentals.append(note) # start of accidental, then append to the accidentals list
                        else: # 处理整体升降，没有accidental的情况
                            # searce in accidentals and get the same accidental value
                            for acc in accidentals:
                                if note['pitch']['step'] == acc['pitch']['step']:
                                   note['accidental'] = acc['accidental']
                                   pages[i][j]['staff1'][k] = note
                                   logging.info( "Fill the continue accidental note:%s in measure:%s", note, measure['number'])
                                   break
                            if note['accidental'] == "":
                                print "accidental OOPS -------"
                    else:
                        continue

                #handle staff2
                accidentals = []
                for k in range(len(measure['staff2'])):
                    note = measure['staff2'][k]
                    if note['pitch']['alter'] == 1:
                        if note['accidental'] != "":
                            accidentals.append(note) # start of accidental, then append to the accidentals list
                        else:
                            # searce in accidentals and get the same accidental value
                            for acc in accidentals:
                                if note['pitch']['step'] == acc['pitch']['step']:
                                   note['accidental'] = acc['accidental']
                                   pages[i][j]['staff2'][k] = note
                                   print "Fill the continue accidental in measure:", measure['number'],note
                                   break
                            if note['accidental'] == "":
                                print "accidental OOPS -------"
                    else:
                        continue

                #handle staff3
                accidentals = []
                for k in range(len(measure['staff3'])):
                    note = measure['staff3'][k]
                    if note['pitch']['alter'] == 1:
                        if note['accidental'] != "":
                            accidentals.append(note) # start of accidental, then append to the accidentals list
                        else:
                            # searce in accidentals and get the same accidental value
                            for acc in accidentals:
                                if note['pitch']['step'] == acc['pitch']['step']:
                                   note['accidental'] = acc['accidental']
                                   pages[i][j]['staff3'][k] = note
                                   print "Fill the continue accidental in measure:", measure['number'],note
                                   break
                            if note['accidental'] == "":
                                print "accidental OOPS -------"
                    else:
                        continue

        return pages


    def handle_measure_repeat_in_score(self, pages):

        measures = []
        for i in range(len(pages)):
            for j in range(len(pages[i])):
                measures.append(pages[i][j])

        start = 0
        end = 0
        measure_list = []
        for i in range(len(measures)):
            m = measures[i]
            measure_list.append(m)
            if m['is_repeat_forward'] == 1:
                start = i
            if m['is_repeat_backward'] == 1:
                end = i
                measure_list.extend(measures[start:end+1])

        return measure_list

    def get_score_info(self, score_type):
        
        default_info = self.get_default_info()
        settings = self.get_settings()
        x_ratio = settings['x_ratio']
        y_ratio = settings['y_ratio']
        
        pages = []
        staff_height = 0
        
        parts = self.get_all_parts()
        
        xoffset = default_info['page_info']['left_margin']
        yoffset = default_info['page_info']['top_margin']
        xmoffset = 0
        
        pid = parts[0]['id']
        measures = self.get_measures_by_part(pid)
        mid = measures[0].get('number')
        staff_num = self.get_staff_num(pid, mid)
        if score_type == 0:  # 五线谱
            staff_height = 9*4 + default_info['appearance']['light_barline']*5
        else:                # 一线谱
            staff_height = 0

        if len(parts) == 1:
            page_info = dict()
        
            if staff_num in (1, 2):
                for m in measures:
                    #print '-------------Measure:', m.get('number')
                    staff1 = []
                    staff2 = []
                    staff3 = []
                    measure = dict()
                    pid = "P1" 
                    page_info = self.get_page_info_by_mid(pid, m.get('number'), page_info, default_info)
                    staff_height_list = []
                    if staff_num == 1:
                        staff_height_list.append(0)
                    else:
                        staff_height_list.append(0)
                        staff_height_list.append(staff_height+page_info['staff_distance'])
                    measure['staff_height_list'] = staff_height_list
                    ptype = page_info['ptype']
                    mtype = page_info['mtype']
                    if ptype == 1 and mtype == 1:  # first page, first measure
                        page = []
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m.get('number'))
                        measure['width'] = int(m.get('width')) * x_ratio
                        xoffset = page_info['left_margin']
                        yoffset = page_info['top_margin'] + page_info['top_system_distance'] # first measure
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (staff_num * staff_height + page_info['staff_distance']) * y_ratio
                    elif ptype == 0 and mtype == 0: # in page, in measure
                        measure['is_start'] = 0  # 0-not start measure, 1-start measure
                        measure['number'] = int(m.get('number'))
                        measure['width'] = int(m.get('width')) * x_ratio
                        measure['x'] = xmoffset
                        measure['y'] = yoffset * y_ratio * -1
                        xmoffset += measure['width'] 
                    elif ptype == 2 and mtype == 1: # new page, first measure
                        pages.append(page)
                        page = []
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m.get('number'))
                        measure['width'] = int(m.get('width')) * x_ratio
                        xoffset = page_info['left_margin'] # first measure
                        yoffset = page_info['top_margin'] + page_info['top_system_distance'] # first measure
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (staff_num * staff_height + page_info['staff_distance']) * y_ratio
                    elif ptype == 0 and mtype == 2: # in page, new system measure
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m.get('number'))
                        measure['width'] = int(m.get('width')) * x_ratio
                        xoffset = page_info['left_margin'] # new system measure
                        yoffset = yoffset + staff_num * staff_height + page_info['staff_distance'] + page_info['system_distance'] # new system measure
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (staff_num * staff_height + page_info['staff_distance']) * y_ratio
                    else:
                        print "...........Measure  OOPS........."
        
                    # handle repeat measure
                    is_repeat_forward, is_repeat_backward = self.get_measure_repeat_flag(m.get('number'), pid)
                    measure['is_repeat_forward'] = is_repeat_forward
                    measure['is_repeat_backward'] = is_repeat_backward

                    notes = self.get_notes_by_mpid(m.get('number'), pid)
                    for note in notes:
                        n = self.formate_note_info(note)
                        if n['ntype'] == 2: # rest measure
                            n['defaultx'] = int(m.get("width"))/2.0
                        n['x'] = (xoffset + n['defaultx']) * x_ratio
                        n['defaultx'] = n['defaultx'] * x_ratio
                        if n['staff'] == 1: # staff1
                            stepy = self.get_step_y_in_score(n, default_info['appearance']['light_barline'], settings['clef_list'][0], score_type)
                            #print "staff1:", yoffset, stepy, y_ratio, n
                            n['y'] = (yoffset + stepy) * y_ratio *-1
                            staff1.append(n)
                        else: # staff2
                            #print n
                            stepy = self.get_step_y_in_score(n, default_info['appearance']['light_barline'], settings['clef_list'][1], score_type)
                            #print "staff2:", yoffset, stepy, page_info['staff_distance'], y_ratio
                            n['y'] = (yoffset + stepy + page_info['staff_distance'] + staff_height) * y_ratio * -1
                            staff2.append(n)
        
                        #print n
        
                    xoffset = xoffset + int(m.get('width'))
                    measure['staff1'] = staff1
                    measure['staff2'] = staff2
                    measure['staff3'] = staff3
                    page.append(measure)
                pages.append(page)

                return pages
            else:
                logging.info("...........Staff OOPS.........")
        elif len(parts) == 2:
            pid1 = parts[0]['id']
            pid2 = parts[1]['id']
            staff_distance1 = 0
            staff_distance2 = 0
            measures1 = self.get_measures_by_part(pid1)
            measures2 = self.get_measures_by_part(pid2)
            mid = measures[0].get('number')
            staff_num = self.get_staff_num(pid1, mid)
            page_info1 = dict()
            page_info2 = dict()
        
            if staff_num == 1:
                logging.info("OOPS Not support Part=2, Staff=1")
            elif staff_num == 2:
                for (m1, m2) in zip(measures1, measures2):
                    #print '----------------------------------------------Measure:', m1.get('number')
                    staff1 = []
                    staff2 = []
                    staff3 = []
                    measure = dict()
        
                    page_info1 = self.get_page_info_by_mid("P1", m1.get('number'), page_info1, default_info)
                    page_info2 = self.get_page_info_by_mid("P2", m2.get('number'), page_info2, default_info)
                    staff_height_list = []
                    staff_height_list.append(0)
                    staff_height_list.append(staff_height+page_info1['staff_distance'])
                    staff_height_list.append(staff_height*2+page_info1['staff_distance']+page_info2['staff_distance'])
                    measure['staff_height_list'] = staff_height_list
                    ptype = page_info1['ptype']
                    mtype = page_info1['mtype']
                    if ptype == 1 and mtype == 1:  # first page, first measure
                        page = []
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m1.get('number'))
                        measure['width'] = int(m1.get('width')) * x_ratio
                        xoffset = page_info1['left_margin']
                        yoffset = page_info1['top_margin'] + page_info1['top_system_distance'] # first measure
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (3*staff_height + page_info1['staff_distance'] + page_info2['staff_distance']) * y_ratio
                    elif ptype == 0 and mtype == 0: # in page, in measure
                        measure['is_start'] = 0  # 0-not start measure, 1-start measure
                        measure['number'] = int(m1.get('number'))
                        measure['width'] = int(m1.get('width')) * x_ratio
                        measure['x'] = xmoffset
                        measure['y'] = yoffset * y_ratio * -1
                        xmoffset += measure['width'] 
                    elif ptype == 2 and mtype == 1: # new page, first measure
                        pages.append(page)
                        page = []
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m1.get('number'))
                        measure['width'] = int(m1.get('width')) * x_ratio
                        xoffset = page_info1['left_margin'] # first measure
                        yoffset = page_info1['top_margin'] + page_info1['top_system_distance'] # first measure
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (3*staff_height + page_info1['staff_distance'] + page_info2['staff_distance']) * y_ratio
                    elif ptype == 0 and mtype == 2: # in page, new system measure
                        measure['is_start'] = 1  # 0-not start measure, 1-start measure
                        measure['number'] = int(m1.get('number'))
                        measure['width'] = int(m1.get('width')) * x_ratio
                        xoffset = page_info1['left_margin'] # new system measure
                        #print "**** new measure system ***"
                        #print yoffset, 3*staff_height, page_info1['staff_distance'], page_info2['staff_distance'], page_info1['system_distance']
                        yoffset = yoffset + 3*staff_height + page_info1['staff_distance'] + page_info2['staff_distance'] + page_info1['system_distance']
                        xmoffset = xoffset * x_ratio + measure['width']
                        measure['x'] = xoffset * x_ratio
                        measure['y'] = yoffset * y_ratio * -1
                        measure['height'] = (3*staff_height + page_info1['staff_distance'] + page_info2['staff_distance']) * y_ratio
                    else:
                        print "...........Measure  OOPS........."
        
                    # handle repeat measure
                    is_repeat_forward, is_repeat_backward = self.get_measure_repeat_flag(m1.get('number'), pid)
                    measure['is_repeat_forward'] = is_repeat_forward
                    measure['is_repeat_backward'] = is_repeat_backward

                    # handle part1 notes
                    #logging.info("########## Part 1##############")
                    notes = self.get_notes_by_mpid(m1.get('number'), pid1)
                    for note in notes:
                        n = self.formate_note_info(note)
                        if n['ntype'] == 2: # rest measure
                            n['defaultx'] = int(m1.get("width"))/2.0
                        n['x'] = (xoffset + n['defaultx']) * x_ratio
                        n['defaultx'] = n['defaultx'] * x_ratio
                        if n['staff'] == 1: # staff1
                            stepy = self.get_step_y_in_score(n, default_info['appearance']['light_barline'], settings['clef_list'][0], score_type)
                            n['y'] = (yoffset + stepy) * y_ratio *-1
                            staff1.append(n)
                        else: # staff2
                            stepy = self.get_step_y_in_score(n, default_info['appearance']['light_barline'], settings['clef_list'][1], score_type)
                            #print yoffset, stepy
                            n['y'] = (yoffset + stepy + page_info1['staff_distance'] + staff_height) * y_ratio * -1
                            staff2.append(n)
        
                        #print n
        
                    # handle part2 notes
                    #logging.info("########## Part 2##############")
                    notes = self.get_notes_by_mpid(m2.get('number'), pid2)
                    for note in notes:
                        n = self.formate_note_info(note)
                        if n['ntype'] == 2: # rest measure
                            n['defaultx'] = int(m2.get("width"))/2.0
                        n['x'] = (xoffset + n['defaultx']) * x_ratio
                        n['defaultx'] = n['defaultx'] * x_ratio

                        stepy = self.get_step_y_in_score(n, default_info['appearance']['light_barline'], settings['clef_list'][2], score_type)
                        #print  yoffset, stepy
                        n['y'] = (yoffset + stepy + 2*staff_height + page_info1['staff_distance'] + page_info2['staff_distance']) * y_ratio * -1
                        staff3.append(n)
        
                        #print n
        
                    xoffset = xoffset + int(m1.get('width'))
                    measure['staff1'] = staff1
                    measure['staff2'] = staff2
                    measure['staff3'] = staff3
                    page.append(measure)
                pages.append(page)

                return pages
            else:
                logging.info("...........Staff OOPS.........")
        else:
            logging.info("...........Part OOPS.........")


    def get_first_note_in_measure(self, m, pages):
        "“” get first normal note in measure """

        notes = m['staff1'] + m['staff2'] + (m['staff3'])
        notes.sort(key=lambda k: (k.get('x', 0)))
        for note in notes:
            if note['ntype'] in (0, 1):  # 0-normal note, 1-rest note
                return note
            elif note['ntype'] == 2:  # 2-rest measure
                measure_left_margin = self.get_measure_left_margin(m['is_start'], pages)
                n = copy.deepcopy(note)
                n['x'] = n['x'] - n['defaultx'] + measure_left_margin
                n['defaultx'] = measure_left_margin
                return n
            else:
                pass


    def get_beats_in_measure(self, m, divisions, beat_type):
        "“” get beats number in measure """

        total = 0
        for n in m['staff1']:
            index = m['staff1'].index(n)
            if index == 0:
                total = n['duration']
            else:
                if n['x'] == m['staff1'][index-1]:
                    continue
                else:
                    total = total + n['duration']

        beats = int((total/divisions)*(beat_type/4.0))

        return beats

    def get_play_score_info(self, pages):
        """ get the play ball/line info"""

        attributes = self.get_attributes("P1")
        beats = int(attributes['time']['beats'])
        beat_type = int(attributes['time']['beat_type'])
        tempo = attributes['tempo']
        #beat_tempo = tempo /(4.0/beat_type)
        #duration = 60.0/beat_tempo
        duration = 60.0/tempo
        divisions = attributes['divisions']  #一个4分音符的divisions数量
        beat_divisions = int((4.0/beat_type) * divisions)  #1拍的divisions数量
        play_score_info = []
        rest_measure_margin_ratio = 0.1
        staff_balls = dict()

        for page in pages:
            npage = []
            for m in page:
                rest_measure_margin = m['width'] * rest_measure_margin_ratio
                for key in ('staff1', 'staff2', 'staff3'):
                    staff_balls[key] = []
                    staff = m[key]
                    if len(staff) == 0:
                        continue
                    total = 0  # 单位division
                    balls = []
                    staff.sort(key=lambda k: (k.get('x', 0)))
                    for n in staff:
                        if len(balls)>0 and (abs(n['x'] - balls[-1]['x']) < 50):
                            # 如果两个note x距离小于1个符头大小，则认为是和弦，跳过该音符
                            continue
                        if n['ntype'] in (0,1):  # nornal note 或 rest note
                            if total % beat_divisions ==0:  #当前是拍位
                                ball = dict(x=0, y=0, total=0, duration=duration, ntype=0)
                                ball['x'] = n['x']
                                ball['y'] = m['y']
                                ball['total'] = total
                                ball['ntype'] = n['ntype']
                                balls.append(ball)
                            total += n['duration'] 
                        elif n['ntype'] == 2:  # rest measure
                            ball = dict(x=0, y=0, total=0, duration=duration, ntype=0)
                            ball['x'] = m['x'] + rest_measure_margin
                            ball['y'] = m['y']
                            ball['total'] = total
                            ball['ntype'] = n['ntype']
                            balls.append(ball)
                            total += n['duration'] 

                    ball_list = []
                    for i in range(len(balls)):
                        next_total = 0
                        if i == len(balls)-1: # 最后1个ball
                            next_total = total  # 该小节的总时长，支持弱起场景
                            endx = m['x'] + m['width']  # 小节线坐标x
                        else:
                            next_total = balls[i+1]['total'] 
                            endx = balls[i+1]['x']  # 下一个球坐标x

                        ball_list.append(balls[i]) # 加入当前拍

                        diff = next_total - balls[i]['total']
                        n = diff/beat_divisions
                        if n > 1: # 插入n-1拍
                            step = 0
                            if i == len(balls)-1: # 最后1个ball
                                step = (endx - rest_measure_margin - balls[i]['x'])/(n-1)
                            else:
                                step = (endx -  balls[i]['x'])/n

                            for j in range(n-1):
                                b = copy.deepcopy(balls[i])
                                b['x'] = balls[i]['x'] + (j+1) * step
                                ball_list.append(b)
                    staff_balls[key] = ball_list

                mballs = []
                mlines = []
                #for i in range(beats):
                for i in range(len(staff_balls['staff1'])):  # 弱起小节可能不够beats数，因此用实际ball的个数
                    b1=b2=b3=None
                    bs = []
                    if len(staff_balls['staff1']) > 0:
                        b1 = staff_balls['staff1'][i]
                        bs.append(b1)
                    if len(staff_balls['staff2']) > 0:
                        b2 = staff_balls['staff2'][i]
                        bs.append(b2)
                    if len(staff_balls['staff3']) > 0:
                        b3 = staff_balls['staff3'][i]
                        bs.append(b3)
                    b = self.get_right_balls(bs)
                    mballs.append(b)
                    mlines.append(b)
                barline = dict(x=0, y=0, duration=duration)
                barline['x'] = m['x'] + m['width']
                mlines.append(barline)

                mplay = dict()
                mplay['mballs'] = mballs
                mplay['mlines'] = mlines
                mplay['page'] = pages.index(page)
                mplay['number'] = m['number']
                mplay['is_start'] = m['is_start']
                mplay['is_repeat_forward'] = m['is_repeat_forward']
                mplay['is_repeat_backward'] = m['is_repeat_backward']
                mplay['staff_height_list'] = m['staff_height_list']
                if mplay['is_start'] == 1: # new measure
                   mplay['x'] = m['x']
                   mplay['y'] = m['y']
                   mplay['height'] = m['height']
                npage.append(mplay)
            play_score_info.extend(npage)

        #handle repeat measure
        start = 0
        end = 0
        play_score_list = []
        for i in range(len(play_score_info)):
            mplay = play_score_info[i]
            play_score_list.append(mplay)
            if mplay['is_repeat_forward'] == 1:
                start = i
            if mplay['is_repeat_backward'] == 1:
                end = i
                play_score_list.extend(copy.deepcopy(play_score_info[start:end+1]))

        return play_score_list

    def get_right_balls(self, bs):

        #优先返回normal的坐标
        for b in bs:
            if b['ntype'] == 0:
                return b
            
        return bs[0]
