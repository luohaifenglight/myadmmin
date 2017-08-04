# -*- coding: utf-8 -*-

import urllib
import mido
import os
from django.conf import settings
from backend.upload.views import UploadFile


class B00Helper(object):
    """
    parse the B00 file
    """

    def __init__(self, midi_path):
        s = midi_path.split('/')
        self.upload_path = settings.UPLOAD_FILE_PATH
        self.name_path = '%s.syx' % s[-1].split('.')[-2]
        #self.save_path = os.path.join(self.upload_path, name_path)
        #self.sql_path = '%suploadfiles/%s' % (settings.NGINX_URL_PREFIX, name_path)
        self.save_path = '/temp/%s' % (self.name_path)
        self.sql_path = ''
        fpath = os.path.join(self.upload_path, s[-1])
        #with open(fpath, 'rb') as f:
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
        file_upload.mkidr_temp()
        mido.write_syx_file(file_path, messages)
        fname, fpath = file_upload.oss_upload(self.name_path, file_path)
        file_upload.remove_temp()
        self.sql_path = fpath
        return self.sql_path


