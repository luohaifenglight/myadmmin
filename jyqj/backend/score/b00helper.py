# -*- coding: utf-8 -*-

import urllib
import mido
import os
import time
import struct
from django.conf import settings
from backend.upload.views import UploadFile
from mido import MidiFile, Message, tempo2bpm
from mido.midifiles.meta import build_meta_message, meta_charset


class B00Helper(object):
    """
    parse the B00 file
    """

    def __init__(self, midi_path):
        s = midi_path.split('/')
        self.dir_name = '.%s-temp' % str(int(time.time()))
        self.upload_path = settings.UPLOAD_FILE_PATH
        self.name_path = '%s.syx' % s[-1].split('.')[-2]
        # self.save_path = os.path.join(self.upload_path, name_path)
        # self.sql_path = '%suploadfiles/%s' % (settings.NGINX_URL_PREFIX, name_path)
        self.save_path = '%s/%s' % (self.dir_name, self.name_path)
        self.sql_path = ''
        fpath = os.path.join(self.upload_path, s[-1])
        # with open(fpath, 'rb') as f:
        #   data = f.read()
        f = urllib.urlopen(midi_path)
        data = f.read()
        f.close()
        self.b00 = map(ord, data)

    def get_data_num(self, data):
    
        BLL = (8-len(bin(data[0]).replace('0b','')))*"0" + bin(data[0]).replace('0b','')
        BML = (8-len(bin(data[1]).replace('0b','')))*"0" + bin(data[1]).replace('0b','')
        BMH = (8-len(bin(data[2]).replace('0b','')))*"0" + bin(data[2]).replace('0b','')
        BHH = (8-len(bin(data[3]).replace('0b','')))*"0" + bin(data[3]).replace('0b','')
        s = "0000"+BHH[1:]+BMH[1:]+BML[1:]+BLL[1:]
    
        return int(s,2), [int(BLL,2), int(BML,2), int(BMH,2), int(BHH,2)]

    def convert_data_len(self, num):

        s = (32-len(bin(num).replace('0b','')))*"0" + bin(num).replace('0b','')

        BLL = int("0"+s[25:32], 2)
        BML = int("0"+s[18:25], 2)
        BMH = int("0"+s[11:18], 2)
        BHH = int("0"+s[4:11], 2)

        return [BLL, BML, BMH, BHH]
    
    def to7bits(self, data):
    
        data_list = []
    
        for d in data:
            s = bin(d).replace('0b','')
            s = (8-len(bin(d).replace('0b','')))*"0" + bin(d).replace('0b','')
            if s[:2] != "00":
                b1 = int("01"+s[2:], 2)
                b2 = int("01"+s[:2]+"0000", 2)
                data_list.append(b1)
                data_list.append(b2)
            else:
                data_list.append(d)
    
        return data_list

    def dump_b00(self):
    
        data = self.b00
    
        data_len = len(data)
    
        head_len = 6
        did_len = 1
        fid_len = 1
        ddl_len = 4  # BLL, BML, BMH, BHH
        check_len = 1
        tail_len = 1
    
        index = 0
        data_list = []
        header = [0xF0,0x43,0x70,0x78,0x00,0x3C]
        b00_item_list = []

        while index < data_len:
            index += head_len
            while index < (data_len-head_len) and data[index] != 0xF7:
                b00_item = []
                did = data[index]
                index += did_len
                fid = data[index]
    
                index += fid_len
                ddl = data[index:index+ddl_len]
                index += ddl_len
                n, ddl_list = self.get_data_num(ddl)
    
                item = data[index:index+n]
                ddd = self.to7bits(item)
                b00_item.append(did)
                b00_item.append(fid)
                b00_item.extend(ddl_list)
                b00_item.extend(ddd)
                index += n
    
                data_check_sum = data[index:index+check_len]
                b00_item.extend(data_check_sum)
                b00_item_list.append(b00_item)
                index += check_len
    
            index += tail_len

        # compose new b00 midi packet
        data_list.extend(header)
        for i in (0,1,2,3,4,12,13,9,10,11,8):
            data_list.extend(b00_item_list[i])
        data_list.append(0xF7)

        msg = mido.Message("sysex",data=data_list[1:-1])

        return msg

    def make_b00_file(self):

        new_add_syx_0 = [
            0xF0,
            0x43,
            0x10,
            0x4C,
            0x00,
            0x00,
            0x7E,
            0x00,
            0xF7
        ]

        new_add_syx_1 = [
            0xF0,
            0x43,
            0x70,
            0x70,
            0x73,
            0xF7
        ]

        send_request = [
            0xF0,
            0x43,
            0x70,
            0x78,
            0x20,
            0xF7
        ]

        send_bank = [
            0xF0,
            0x43,
            0x70,
            0x78,
            0x44,
            0x7e,
            0x00,
            0x00,
            0x00,
            0xF7
        ]

        save_forbidden = [
            0xF0,
            0x43,
            0x70,
            0x78,
            0x44,
            0x7e,
            0x00,
            0x02,
            0x01,
            0xF7
        ]

        cancel_forbidden = [
            0xF0,
            0x43,
            0x70,
            0x78,
            0x44,
            0x7e,
            0x00,
            0x02,
            0x00,
            0xF7
        ]

        midi_new_add_syx0 = mido.parse(new_add_syx_0)
        midi_new_add_syx1 = mido.parse(new_add_syx_1)
        midi_cancel_forbidden = mido.parse(cancel_forbidden)
        midi_save_forbidden = mido.parse(save_forbidden)

        midi_send_request = mido.parse(send_request)

        midi_send_boo = self.dump_b00()

        midi_send_bank = mido.parse(send_bank)
        file_path = self.save_path

        messages = [
            midi_new_add_syx0,
            midi_new_add_syx1,
            midi_cancel_forbidden,
            midi_save_forbidden,
            midi_send_request,
            midi_send_boo,
            midi_send_bank,
        ]
        file_upload = UploadFile()
        file_upload.mkdir_temp(self.dir_name)
        mido.write_syx_file(file_path, messages)
        fname, fpath = file_upload.oss_upload(self.name_path, file_path)
        file_upload.remove_temp(self.dir_name)
        self.sql_path = fpath
        return self.sql_path

    @classmethod
    def get_tempo(cls, path):
        if not path:
            return None

        midi_file = urllib.urlopen(path)
        tempo = 40
        meta_message = MyMetaMessage(midi_file.read())
        midi_file.close()
        for message in meta_message.get_all_meta_message():
            if message.type == 'set_tempo':
                tempo = int(tempo2bpm(message.tempo))
                break

        return tempo


class MyMetaMessage(object):
    '''
        create a class get meta_message from file_data, not 
    '''
    def __init__(self, data=None):
        self.data = data
        self.index = 0

    def read(self, num):
        if int(num) > 0:
            current_num = self.index + num
            current_data = self.data[self.index: current_num]
            self.index = current_num
            return current_data

    def tell(self):
        return self.index

    def read_byte(self):
        byte = self.read(1)
        if byte == b'':
            print 'eoferror', self.tell()
            raise EOFError
        else:
            return ord(byte)

    def read_bytes(self, size):
        if size > 1000000:
            raise IOError('Message length {} exceeds maximum length {}'.format(
                size, 1000000))
        return [self.read_byte() for x in range(size)]

    def read_variable_int(self):
        delta = 0

        while True:
            byte = self.read_byte()
            delta = (delta << 7) | (byte & 0x7f)
            if byte < 0x80:
                return delta


    def read_chunk_header(self):
        header = self.read(8)
        if len(header) < 8:
            raise EOFError

        # Todo: check for b'RIFF' and switch endian?

        return struct.unpack('>4sL', header)

    def read_meta_message(self, delta):
        type = self.read_byte()
        length = self.read_variable_int()
        data = self.read_bytes(length)
        return build_meta_message(type, data, delta)

    def read_sysex(self, delta):
        length = self.read_variable_int()
        data = self.read_bytes(length)

        # Strip start and end bytes.
        # Todo: is this necessary?
        if data and data[0] == 0xf0:
            data = data[1:]
        if data and data[-1] == 0xf7:
            data = data[:-1]

        return Message('sysex', data=data, time=delta)

    def get_all_meta_message(self):
        start = self.tell()
        size = len(self.data)
        while True:
            if self.tell() - start == size:
                break
            delta = self.read_variable_int()
            status_byte = self.read_byte()
            if status_byte == 0xff:
                msg = self.read_meta_message(delta)
                yield msg

    def _get_all_messsage(self):
        messages = []
        name, size = self.read_chunk_header()
        print name, size

        if name != b'MTrk':
            raise IOError('no MTrk header at start of track')


        start = self.tell()
        last_status = None

        while True:
            # End of track reached.
            if self.tell() - start == size:
                break
            delta = self.read_variable_int()


            # Todo: not all messages have running status
            status_byte = self.read_byte()

            if status_byte < 0x80:
                if last_status is None:
                    raise IOError('running status without last_status')
                peek_data = [status_byte]
                status_byte = last_status
            else:
                if status_byte != 0xff:
                    # Meta messages don't set running status.
                    last_status = status_byte
                peek_data = []

            if status_byte == 0xff:
                msg = self.read_meta_message(delta)
            elif status_byte in [0xf0, 0xf7]:
                # Todo: I'm not quite clear on the difference between
                # f0 and f7 events.
                msg = self.read_sysex(delta)
            else:
                msg = self.read_message(status_byte, peek_data, delta)

            messages.append(msg)
            return messages

    def read_chunk_header(self):
        header = self.read(8)
        if len(header) < 8:
            raise EOFError

        # Todo: check for b'RIFF' and switch endian?

        return struct.unpack('>4sL', header)

    def read_file_header(self):
        name, size = self.read_chunk_header()

        if name != b'MThd':
            raise IOError('MThd not found. Probably not a MIDI file')
        else:
            data = self.read(size)

            if len(data) < 6:
                raise EOFError

            return struct.unpack('>hhh', data[:6])

    def get_all_messages(self):

        tracks = []
        with meta_charset('latin1'):

            (type,
             num_tracks,
             ticks_per_beat) = self.read_file_header()

            for i in range(num_tracks):
                tracks.append(self._get_all_messsage())

        return tracks



