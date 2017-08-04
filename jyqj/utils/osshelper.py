# -*- coding: utf-8 -*-
import oss2
from oss_common import *
import sys, os
#from PIL import Image
from django.conf import settings


class OSSHelper(object):
    def __init__(self):
        self._init_conf()

    def _init_conf(self):
        self.OSS_ID = settings.OSSCONF_OSS_ID
        self.OSS_SECRET = settings.OSSCONF_OSS_SECRET
        self.ENDPOINT = settings.OSSCONF_END_POINT
        self.bucket_key = settings.OSSCONF_BUCKET_KEY

        self.auth = oss2.Auth(self.OSS_ID, self.OSS_SECRET)
        self.bucket = oss2.Bucket(self.auth, self.ENDPOINT, self.bucket_key)

    def create_bucket_private(self):
        # 创建私有bucket
        str = ('test-static' + random_string(10)).lower()
        bucket = oss2.Bucket(self.auth, 'http://oss-cn-hangzhou.aliyuncs.com', str)
        bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)

    def bucket_list(self):
        # 查看bucket 列表
        service = oss2.Service(self.auth, 'http://oss-cn-hangzhou.aliyuncs.com')
        print([b.name for b in oss2.BucketIterator(service)])

    #def get_image_info(self, image_file):
    #    """获取本地图片信息
    #    :param str image_file: 本地图片
    #    :return tuple: a 3-tuple(height, width, format).
    #    """
    #    im = Image.open(image_file)
    #    print (im.height, im.width, im.format)

    def upload_file_large(self, fname, fpath):
        result = oss2.resumable_upload(self.bucket, fname, fpath, multipart_threshold=200 * 1024, part_size=None)
        result = self.bucket.get_object(fname)
        if result.headers['x-oss-object-type'] == 'Multipart':
            return True
        else:
            return False

    def batch_delete_file(self, file_list):
        '''
        :param file_list: 批量删除文件列表 传入［ ］
        :return:
        '''
        if isinstance(file_list, list):
            self.bucket.batch_delete_objects(file_list)
            return True
        else:
            return False

    def delete_file(self, file_name):
        '''
        # 注意：重复删除motto.txt，并不会报错x
        # 删除某个目录下的  得提供完整路径才可以删除，如果该目录下只有要删除的文件   则文件夹一同删除
        ＃不支持删除文件夹
        '''
        # 删除名为motto.txt的Object
        self.bucket.delete_object(file_name)
        return self.bucket.object_exists(file_name)

    def upload_file_small(self, fname, fpath):
        '''
        :param fpath:
        :return:
        '''
        result = oss2.resumable_upload(self.bucket, fname, fpath)
        result = self.bucket.get_object(fname)

    def upload_file_post(self, fname, fchunks):
        '''
        :param fname:上传post
        :param fchunks:
        :return:
        '''
        self.bucket.put_object(fname, fchunks)
        # with open(oss2.to_unicode('本地座右铭.txt'), 'rb') as f:
        #     self.bucket.put_object('云上座右铭.txt', f)

    def object_list(self):
        for i, object_info in enumerate(oss2.ObjectIterator(self.bucket)):
            print("{0} {1}".format(object_info.last_modified, object_info.key))

    def get_object_to_file(self, fname, save_name):
        # 下载到本地文件f
        self.bucket.get_object_to_file('motto.txt', '本地文件名.txt')


if __name__ == '__main__':
    osshelper = OSSHelper()
    # osshelper.create_bucket_private()
    osshelper.bucket_list()
    # osshelper.get_image_info('/Users/ducs/Downloads/WechatIMG2.png')
    # osshelper.upload_file_small(fname='uploadfiles/20170321/test.png', fpath='/Users/ducs/Downloads/WechatIMG2.png')
    # osshelper.upload_file_small(fname='uploadfiles/20170321/test2.png', fpath='/Users/ducs/Downloads/WechatIMG2.png')
    # osshelper.object_list()
    osshelper.delete_file('uploadfiles/20170321/')
