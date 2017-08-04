#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaes
import urllib
import os
import time
from Crypto.Cipher import AES
from backend.upload.views import UploadFile


class AES_Upload(object):
    def __init__(self, key="JYQJ_YYJS_AESKEY"):
        self.aes_command = AES_Commamd(key=key)
        self.dir_name = '.%s-encrypt' % str(int(time.time() * 1000))
        self.file_upload = UploadFile()

    def encrypt_by_url_and_upload_oss(self, url):
        '''

        :param url:  url is by database
        :return: 
        '''
        self.file_upload.mkdir_temp(self.dir_name)
        file_name = url.split('/')[-1]
        name_path = '%s/%s' % (self.dir_name, file_name)
        encrypt_path = '%s.enc' % name_path
        print 'get-file--'
        urllib.urlretrieve(url, name_path)
        if not self.is_get_file_scuess(name_path):
            print 'get file:%s, fail' % file_name
            self.file_upload.remove_temp(self.dir_name)
            return -1
        print 'start-encrypt--'
        sa = time.time()
        self.aes_command.encrypt_pyroto(name_path, encrypt_path)
        print 'use time:%s---' % (time.time() - sa)
        print 'delete--oss-file--'
        self.file_upload.delete_file(('other/%s' % file_name))
        print 'start-uploadoss--'
        fname, fpath = self.file_upload.oss_upload(file_name, encrypt_path)
        self.file_upload.remove_temp(self.dir_name)
        return fpath
        print '-------handle_file:%s, scuess--------' % file_name

    def batch_decrypt_dir(self, dir):
        for dirpath, dirnames, filenames in os.walk(dir):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                target_path = '%s.out.m4v' % fullpath
                self.aes_command.decrypt(fullpath, target_path)
                print "decrypt-file:%s,scuess" % file

    def is_get_file_scuess(self, filepath):
        binfile = open(filepath, 'rb')
        xml_code = [
            0x3C,
            0x3F,
            0x78,
            0x6D,
            0x6C
        ]
        html_code = [
            0x68,
            0x74,
            0x6D,
            0x6C,
            0x3E
        ]
        binfile.seek(0)
        file_prefix = binfile.read(5)
        binfile.close()
        if self._is_check_scuess(file_prefix, xml_code) and self._is_check_scuess(file_prefix, html_code):
            return True
        return False

    def _is_check_scuess(self, preifx, code):
        for index, num in enumerate(preifx):
            if ord(num) != code[index]:
                return True
        return False


class AES_Commamd(object):
    def __init__(self, key='JYQJ_YYJS_AESKEY'):
        self.key = key
        self.mode = pyaes.AESModeOfOperationECB(key)

    def encrypt(self, file_in_path, file_out_path):
        file_in = file(file_in_path)
        file_out = file(file_out_path, 'wb')
        pyaes.encrypt_stream(self.mode, file_in, file_out)

        # Close the files
        file_in.close()
        file_out.close()

    def encrypt_pyroto(self, filename, fileout):
        with open(filename, 'rb') as f:
            data = f.read()
        cryptor = AES.new(self.key, AES.MODE_ECB)
        pad = len(data) % 16
        if pad:
            data = data + chr(16 - pad) * (16 - pad)

        result = cryptor.encrypt(data)
        with open(fileout, 'wb+') as fo:
            fo.write(result)

    def decrypt(self, file_in_path, file_out_path):
        file_in = file(file_in_path)
        file_out = file(file_out_path, 'wb')
        pyaes.decrypt_stream(self.mode, file_in, file_out)

        # Close the files
        file_in.close()
        file_out.close()

