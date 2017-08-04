#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Video, VideoSegment
from .enumtype import VIDEO_TYPE
from backend.institution.models import CourseSystem

import traceback


class VideoDB(DataBuilder):

    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_type(self, obj, default=''):
        return VIDEO_TYPE.getDesc(obj.type)


class VideoDQ(DataSQLQuery):
        model = Video
        data_model = VideoDB
        pass


class VideoCommand:

    def __init__(self, data=None):
        self.data = data

    def video_edit(self, video_id=None):
        video_info = self.data
        if video_info is None:
            return None
        segment = video_info.pop('segments', [])
        delete_id = video_info.pop('delete_id', '')
        video_info.pop('video_name')
        video_info['suffix'] = video_info['video_path'].split('.')[-1]
        if video_id is None:
            try:
                video = Video.objects.create(**video_info)
            except IntegrityError:
                traceback.print_exc()
                print 'error'
        else:
            try:
                video = Video.objects.get(id=video_id)
            except:
                traceback.print_exc()
                print 'error'
                return -1
            for k, v in video_info.iteritems():
                setattr(video, k, v)
            video.save()
        delete_segment_ids = list(set(delete_id.split(',')))
        if '' in delete_segment_ids:
            delete_segment_ids.remove('')
        VideoSegment.objects.filter(id__in=delete_segment_ids).delete()
        if segment:
            for seg in segment:
                seg['video_id'] = video.id
                if not seg['id']:
                    seg.pop('id', '')
                    VideoSegment.objects.create(**seg)
                else:
                    segment_instance = VideoSegment.objects.get(id=seg['id'])
                    for k, v in seg.iteritems():
                        setattr(segment_instance, k, v)
                        segment_instance.save()
        return video.id

    def video_get(self, video_id):
        """
        GET LIST BY id
        """
        if video_id is None:
            return None
        try:
            video = Video.objects.get(id=video_id)
        except IntegrityError:
            print 'error'
        video_data = to_dict(video)
        segment_all = video.video_segments.all()
        video_data['segments'] = [to_dict(v) for v in segment_all]
        return video_data

    @classmethod
    def reset_status(cls, id):
        video = Video.objects.get(id=id)
        video.status = 1 - video.status
        video.save()
        return True

    @classmethod
    def delete_video(cls, id):
        video = Video.objects.get(id=id)
        from backend.unit.models import SectionSegmentPlay, SectionVideoTeach
        from utils.aes_upload import AES_Upload
        segments = SectionSegmentPlay.objects.filter(video__id=id)
        videoteachs = SectionVideoTeach.objects.filter(video__id=id)
        if segments or videoteachs:
            return -1
        aes_instance = AES_Upload()
        file_name = video.video_path.split('/')[-1]
        aes_instance.file_upload.delete_file(('other/%s' % file_name))
        video.delete()

        return True


def video_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)| Q(type__contains=q)
    query = Video.objects.filter(qry).filter(status=1)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}:{}'.format(
                obj.id,
                VIDEO_TYPE.getDesc(obj.type),
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


def segment_choices(q='', page=1, num=30, video=None, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(label__contains=q)
    qry = qry & Q(video__id=video)
    query = VideoSegment.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.label,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}
