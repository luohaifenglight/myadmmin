#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
from utils.aes_upload import AES_Upload
from backend.video.models import Video

import time
import os


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('param', nargs='+', type=str)

    '''
       encrypt, decrypt by des
    '''

    def handle(self, *args, **options):
        for param in options['param']:
            if param == 'encrypt':
                videos = Video.objects.all()
                s_time = time.time()
                for video in videos:
                    # ids = [80, 81, 20, 15, 16] # 34, 55, 49, 71, 72,
                    # if int(video.id) in ids:
                    #     continue
                    if '127.0.0.1' in video.video_path:
                        continue
                    start_time = time.time()
                    aes_instance = AES_Upload()
                    print "video_path:%s" % (str(video.video_path))
                    try:
                        fpath = aes_instance.encrypt_by_url_and_upload_oss(video.video_path)
                    except :
                        print "-----error--- id:%s" % (str(video.id))
                        continue

                    if fpath == -1:
                        fpath = ''
                    if fpath:
                        video.video_path = fpath
                        video.save()
                    print '------id:%s,use time:%s--------' % (str(video.id), str(time.time()-start_time))
                print '------ALL,use time:%s--------' % (str(time.time() - s_time))

            if param == 'test-encrypt':
                #ids = [15, 16, 20]  # 20, 34, 55, 49, 71, 72
                ids = [17, 18, 19, 21, 22, 23]
                id_handle = [15, 16, 20]
                max = 24
                videos = Video.objects.filter(id__lt=max)
                for video in videos:
                    if int(video.id) in id_handle:
                        continue
                    aes_instance = AES_Upload()
                    fpath = aes_instance.encrypt_by_url_and_upload_oss(video.video_path)
                    if fpath:
                        video.video_path = fpath
                        video.save()

            if param == 'decrypt':
                dirs = 'decrypt_dirs'
                aes_instance = AES_Upload()
                aes_instance.batch_decrypt_dir(dirs)

            if param == 'backup':
                videos = Video.objects.all()
                for video in videos:
                    print video.id, video.video_path
                    cmd = 'wget %s' %(video.video_path)
                    os.system(cmd)

            if param == 'reupload':
                max = [17, 18, 19, 21, 22, 23]
                videos = Video.objects.filter(id__in=max)
                for video in videos:
                    aes_instance = AES_Upload()
                    try:
                        file_name = video.video_path.split('/')[-1]
                        print '----file_name:%s---' % (file_name)
                        encrypt_path = 'video_backup/%s' % str(file_name)
                        aes_instance.file_upload.delete_file(('other/%s' % file_name))
                        print 'start-uploadoss--'
                        fname, fpath = aes_instance.file_upload.oss_upload(file_name, encrypt_path)
                    except:
                        print 'error'
                        continue


