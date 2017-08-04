#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import ScoreEnjoy, ScoreEnjoyManage
from backend.institution.models import CourseSystem

from .enumtype import SCORE_OPTIONAL_TYPE
from backend.score.enumtype import MUSIC_CATEGORY_TYPE
from utils.cmdhelper import CommandHelper, UploadFileType
import traceback


# ＝＝＝＝＝＝＝＝＝＝＝欣赏曲目＝＝＝＝＝＝＝＝＝＝＝＝＝
class ScoreEnjoyListDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_opt(self, obj, default=''):
        return {'status': obj.status,
                'publish': '已发布' if obj.status else '未发布',
                'score_id': obj.id,
                'edit': '查看详情' if obj.status else '编辑'}


class ScoreEnjoyListDQ(DataSQLQuery):
    model = ScoreEnjoy
    data_model = ScoreEnjoyListDB
    pass


class ScoreEnjoyCommand(CommandHelper):
    def __init__(self, data=None):
        super(ScoreEnjoyCommand, self).__init__(data)

    def _del(self, id):

        obj = ScoreEnjoy.objects.filter(id=id)
        if obj.count() > 0:
            obj.delete()

        obj = ScoreEnjoy.objects.filter(bkp_pic_id=id)
        if obj.count() > 0:
            obj.delete()

        if obj.count() > 0:
            return ('msg', '删除失败')
        else:
            return ('msg', '删除成功')

    def _copy(self, id):

        from django.forms import model_to_dict

        instance = ScoreEnjoy.objects.get(id=id)
        kwargs = model_to_dict(instance, exclude=['id', 'status'])
        new_instance = ScoreEnjoy.objects.create(**kwargs)

        # copy targets
        targets = ScoreEnjoy.objects.filter(bkp_pic_id=id).all()
        for t in targets:
            t.id = None
            t.bkp_pic_id = new_instance.id
            t.save()

        return ('msg', '复制成功')

    def _check_valid(self, entry):
        '''
        :return: 校验名字 seq是否重复   重复的无法发布
        '''
        obj = ScoreEnjoy.objects.filter(name=entry.name)
        if obj.count() > 1:  # 存在重复
            return False
        else:
            return True

    def _publish(self, id):
        obj = ScoreEnjoy.objects.filter(id=id)
        msg = ''
        if obj.count() > 0:
            entry = obj.get(id=id)
            if entry.status == 1:
                entry.status = 0
                entry.save()
                msg = '取消发布成功'

            else:
                if self._check_valid(entry):
                    entry.status = 1
                    entry.save()
                    msg = '发布成功'
                else:
                    return ('msg', '操作失败 名字重复')

            return ('msg', msg)
        else:
            return ('msg', '操作失败')

    def modify(self, data=None):
        try:
            if data is None:
                return None
            opt = data.get('opt')
            id = data.get('id')

            if opt == 'copy':
                return self._copy(id)
            elif opt == 'delete':
                return self._del(id)
            elif opt == 'edit' or opt == 'check':
                pass
            elif opt == 'publish':
                return self._publish(id)
        except Exception, e:
            print traceback.print_exc()

    def _modify_score(self, data=None, upfile=None):
        '''
        获取更新的参数
        :param data:
        :param upfile:
        :return:
        '''
        # score_enjoy_key=['name','audio_name','audio_path','poster_name','poster_path']
        name = data.get('name', '')
        status = data.get('status', 0)
        info = {}
        info['name'] = name

        info['status'] = 1 if status == 'on' else 0

        if upfile:
            if upfile.get('score_audio', ''):
                fname, fpath = self._recv_file_oss(f=upfile.get('score_audio'), type=UploadFileType.AUDIO)
                info['audio_name'] = fname
                info['audio_path'] = fpath

            if upfile.get('score_poster', ''):
                fname, fpath = self._recv_file_oss(f=upfile.get('score_poster'), type=UploadFileType.IMG)
                info['poster_name'] = fname
                info['poster_path'] = fpath

        return info

    def edit_score(self, data=None, upfile=None):
        try:
            score_id = data.get('score_id')
            score_update_map = self._modify_score(data=data, upfile=upfile)
            if score_update_map and score_id:
                num = ScoreEnjoy.objects.filter(id=score_id).update(**score_update_map)
                if num > 0:
                    print 'success update'
                return num

            elif score_update_map and not score_id:  # 新建
                entry = ScoreEnjoy.objects.create(**score_update_map)
                return entry.id
            return None
        except Exception, e:
            print traceback.print_exc()

    def score_get(self, score_id):
        """
          GET LIST BY id
          """
        if score_id is None:
            return None
        try:
            score = ScoreEnjoy.objects.get(id=score_id)
        except IntegrityError:
            print 'error'
        score_data = to_dict(score)

        return score_data


# ＝＝＝＝＝＝＝＝＝＝＝欣赏曲目管理＝＝＝＝＝＝＝＝＝＝＝＝＝

class ScoreEnjoyManageListDB(DataBuilder):
    def getval_score_num(self, obj, default=''):
        '''
        该课程体系下的歌曲数量  相同的多条算多条
        :return:
        '''
        score_num = ScoreEnjoyManage.objects.filter(course_system_id=obj.id).count()
        return score_num

    def getval_opt(self, obj, default=''):
        return {'course_sys_id': obj.id,
                'edit': '编辑'}


class ScoreEnjoyManageListDQ(DataSQLQuery):
    print 'score mangelist'
    model = CourseSystem
    data_model = ScoreEnjoyManageListDB
    pass


class CourseSystemCommand(object):
    '''
    处理课程体系下欣赏曲目函数
    '''

    def __init__(self, data=None):
        self.data = data

    def _valid_data(self,data):
        tmp=[]
        for score in data:
            print score
            if score['seq'] in tmp:
                return False
            else:
                tmp.append(score['seq'])

        return True

    def course_system_edit(self, course_system_id=None):
        '''
        更改提交 创建的  课程体系－欣赏曲库内容
        :param course_system_id:
        :return:
        '''
        score_optionals = self.data
        if score_optionals is None:
            return None
        if course_system_id is None:
            return None
        try:
            course_system = CourseSystem.objects.get(id=course_system_id)
        except IntegrityError:
            print 'error'
            raise IntegrityError

        if not self._valid_data(score_optionals): #校验seq
            return False

        course_system.score_enjoy.all().delete()
        try:
            for score in score_optionals:
                ScoreEnjoyManage.objects.create(**score)
        except Exception, e:
            print 'error', e
            raise
        return course_system_id

    def course_system_get(self, course_system_id):
        """
        获取课程体系－－欣赏曲库列表
        """
        if course_system_id is None:
            return None
        try:
            course_system = CourseSystem.objects.get(id=course_system_id)
        except IntegrityError:
            print 'error'

        score_enjoy_all = course_system.score_enjoy.all()
        course_system_data = [
            {
                'score_id': v.score_id,
                'score_text': u'{}:{}'.format(
                    v.score.id,
                    v.score.name,
                ),
                'seq': int(v.seq),
            }
            for v in score_enjoy_all]

        return course_system_data


def score_enjoy_office_choices(q='', music_type=0, page=1, num=30, initial=None):
    '''
    添加欣赏曲目到课程体系中下拉选项
    :param q:
    :return:
    '''
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    qry = qry & Q(status=1)
    query = ScoreEnjoy.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.name
            ),
        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}
