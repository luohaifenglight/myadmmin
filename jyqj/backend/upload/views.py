# -*- coding: UTF-8 -*-
import json
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from utils.decorators import json_http_response
from utils import upload_name
from converter import Converter
from utils.osshelper import OSSHelper
from utils.cmdhelper import CommandHelper, UploadFileType
import time

cmds = {
    'time_length': 'ffmpeg -i  %s  2>&1 | grep "Duration" | cut -d " " -f 4 | sed s/,//',
    'thmub': 'ffmpeg -i "%s" -y -f image2 -ss 1 -t 0.001 -s 350x240 "%s" '
}


def get_video_info(video_path, thmub_path):
    size = os.path.getsize(video_path)
    # c = Converter()
    # info = c.probe(video_path)
    # # prefix = info.format.format
    # time_length = info.format.duration
    # c.thumbnail(video_path, 10, thmub_path)
    ptime_len = os.popen(cmds['time_length'] % video_path)
    time_length = ptime_len.read()
    time_length = float(time_length.split(':')[0]) * 3600 + float(time_length.split(':')[1]) * 60 + \
                  float(time_length.split(':')[2])
    print time_length
    ptime_len.close()
    pthmub = os.popen(cmds['thmub'] % (video_path, thmub_path))
    thmub = pthmub.read()
    pthmub.close()
    return size, time_length


class UploadFile(OSSHelper):
    def __init__(self):
        super(UploadFile, self).__init__()
        self.size = ''
        self.time_length = ''
        self.thmub_path = ''
        self.name = ''
        self.address = ''
        self.romte_prefix = settings.OSS_UPLOAD_FILE_PATH

    def upload_file(self, o_file):
        dir_name = '.%s-temp' % str(int(time.time()))
        self.mkdir_temp(dir_name)
        ext = o_file.name.split('.')[-1]
        self.name = o_file.name
        save_name = upload_name(ext)
        original_path = '%s/%s' % (dir_name, save_name)
        destination = open(original_path, 'wb+')
        for chunk in o_file.chunks():
            destination.write(chunk)
        destination.close()
        thmub_name = upload_name('png')
        thmub_path = '%s/%s' % (dir_name, thmub_name)
        video_prefix = ['ogg', 'mkv', 'flv', 'mp4', 'mov', 'm4v', 'avi']
        zip_prefix = ['zip', 'app']
        if ext in zip_prefix:
            self.size = os.path.getsize(original_path) * 1.0 / 1024 /1024
            print 'size:%s' % self.size
        if ext in video_prefix:
            self.size, self.time_length = get_video_info(original_path, thmub_path)
            self.size = os.path.getsize(original_path) * 1.0 / 1024 / 1024
            from utils.aes_upload import AES_Commamd as AES_Command
            aes_upload = AES_Command()
            target_enpath = '%s.env' % original_path
            aes_upload.encrypt_pyroto(original_path, target_enpath)
            original_path = target_enpath
            a, b = self.oss_upload(thmub_name, thmub_path)
            self.thmub_path = b

        fname, fpath = self.oss_upload(save_name, original_path)
        self.remove_temp(dir_name)
        self.address = fpath
        return o_file.name, fpath

    def oss_upload(self, fname, file_path):
        fname = 'other/' + fname
        result = self.upload_file_small(fname, file_path)

        return 1, self.romte_prefix + fname

    def get_video_info(self):
        return self.size, self.time_length, self.thmub_path

    def mkdir_temp(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def remove_temp(self, file_name):
        os.system('rm -rf %s' % (file_name))

    def web_format_dict(self):
        return json_http_response({'file': self.name,
                                   'address': self.address,
                                   'thumb_url': self.thmub_path,
                                   'size': self.size,
                                   'time_l': self.time_length,
                                   }
                                  )


@csrf_exempt
def upload_image(request):
    _from = request.POST.get("from", "")
    image = request.FILES.get('file', None)
    if not image:
        print 'file not find'
    # use oss---
    file_upload = UploadFile()
    file_upload.upload_file(image)
    return file_upload.web_format_dict()
    # not use oss----
    ext = image.name.split('.')[-1]
    save_name = upload_name(ext)
    print 'abspath:%s,%s' % (settings.UPLOAD_FILE_PATH, settings.MEDIA_ROOT)
    destination = open(os.path.join(settings.UPLOAD_FILE_PATH, save_name), 'wb+')
    print image.name
    for chunk in image.chunks():
        destination.write(chunk)
    destination.close()
    size, time_length, thmub_path = '', '', ''
    video_prefix = ['ogg', 'mkv', 'flv', 'mp4', 'mov', 'm4v', 'avi']
    if ext in video_prefix:
        thmub_path = upload_name('png')
        thmub_path_a = os.path.join(settings.UPLOAD_FILE_PATH, thmub_path)
        print thmub_path_a
        size, time_length = get_video_info(os.path.join(settings.UPLOAD_FILE_PATH, save_name), thmub_path_a)

    print 'scuess'
    print   thmub_path
    if _from == 'web':
        return HttpResponseRedirect(request.get_full_path())
    else:
        return json_http_response({'file': image.name,
                                   'address': '%suploadfiles/%s' % (settings.NGINX_URL_PREFIX, save_name),
                                   'thumb_url': '%suploadfiles/%s' % (
                                       settings.NGINX_URL_PREFIX, thmub_path) if thmub_path else '',
                                   'size': size,
                                   'time_l': time_length,
                                   }
                                  )


@csrf_exempt
def upload_file_ajax(request):
    try:
        pass
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            data = request.FILES
            print data.dict().items()
            cmdhelper = CommandHelper()
            for k, v in data.dict().items():
                print k, v, '33333'
                f = data.get(k)
                print f.name
                fname, fpath = cmdhelper._recv_file_oss(f=f, type=UploadFileType.OTHER)
                print fname, fpath

            pass

    except Exception, e:
        print e
