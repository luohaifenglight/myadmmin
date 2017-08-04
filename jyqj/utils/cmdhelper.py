#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osshelper import OSSHelper
from django.conf import settings
import time, sys, os, hashlib
import traceback


class UploadFileType(object):
    IMG = 'img/'
    AUDIO = 'audio/'
    VIEDO = 'video/'
    OTHER = 'other/'


class CommandHelper(object):
    '''
    各个模块操作的公共方法提取
    '''

    def __init__(self, data=None):
        self.data = data

    def _enum(*sequential, **named):
        '''
        :param sequential: 生成enum 对象
        :param  newtype = _enum('zero','one','two')
        :       print newtype.zero  ----> 0
        :return:
        '''
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)

    def _md5(self, str=''):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def _recv_file_oss(self, f, type='other/'):
        '''
        :param type: 资源类型
        :param f: 资源对象  post报文中文件
        :return: （资源名称，访问资源的路径）
        '''
        # TODO 校验上传是否成功
        try:
            if f is None:
                return None
            file_name = self._md5(f.name + str(time.time())) + '.' + f.name.split('.')[-1]
            osshelper = OSSHelper()
            osshelper.upload_file_post(type + file_name, f.chunks())
            print (f.name, settings.OSS_UPLOAD_FILE_PATH + type + file_name)
            return (f.name, settings.OSS_UPLOAD_FILE_PATH + type + file_name)
        except Exception, e:
            print traceback.print_exc()

    def _recv_file(self, f=None, save_to=settings.UPLOAD_FILE_PATH):
        try:
            if f is None:
                return None
            else:
                file_name = ""
                path = save_to + '/' + time.strftime('%Y%m%d/')
                if not os.path.exists(path):
                    os.makedirs(path)

                fetch_file_path = time.strftime('%Y%m%d/') + self._md5(f.name + str(time.time())) + '.' + \
                                  f.name.split('.')[-1]
                file_name = path + self._md5(f.name + str(time.time())) + '.' + \
                            f.name.split('.')[-1]

                with open(file_name, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

                return (f.name, fetch_file_path)
        except Exception, e:
            print traceback.print_exc()
