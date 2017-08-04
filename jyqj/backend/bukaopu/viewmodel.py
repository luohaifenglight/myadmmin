#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from utils.osshelper import OSSHelper
from utils.cmdhelper import CommandHelper, UploadFileType
from backend.teacher.models import Teacher
from .models import *
import traceback, copy
import os, sys, time

import hashlib
from django.conf import settings
from django.forms.models import model_to_dict


# from django.forms import model_to_dict


class BKPPicDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_create_time(self, obj, default=''):
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.create_time)) \
            if obj.create_time else ''

    def getval_type(self, obj, default=''):
        return '已冻结' if obj.status else '正常'

    def getval_opt(self, obj, default=''):
        return {'publish': '已发布' if obj.status else '未发布',
                'copy': obj.id,
                'picid': obj.id,
                'edit': '查看详情' if obj.status else '编辑'}


class BKPPicDQ(DataSQLQuery):
    model = BKPPic
    data_model = BKPPicDB
    pass


class BKPPicCommand(CommandHelper):
    def __init__(self, data=None):
        super(BKPPicCommand, self).__init__(data)

    def _del(self, id):

        obj = BKPPic.objects.filter(id=id)
        if obj.count() > 0:
            obj.delete()

        obj = BKPTarget.objects.filter(bkp_pic_id=id)
        if obj.count() > 0:
            obj.delete()

        if obj.count() > 0:
            return ('msg', '删除失败')
        else:
            return ('msg', '删除成功')

    def _copy(self, id):

        from django.forms import model_to_dict

        instance = BKPPic.objects.get(id=id)
        kwargs = model_to_dict(instance, exclude=['id', 'status'])
        new_instance = BKPPic.objects.create(**kwargs)

        # copy targets
        targets = BKPTarget.objects.filter(bkp_pic_id=id).all()
        for t in targets:
            t.id = None
            t.bkp_pic_id = new_instance.id
            t.save()

        return ('msg', '复制成功')

    def _check_valid(self, entry):
        '''
        :return: 校验名字 seq是否重复   重复的无法发布
        '''
        obj = BKPPic.objects.filter(name=entry.name)
        if obj.count() > 1:  # 存在重复
            return False
        else:
            return True

    def _publish(self, id):
        obj = BKPPic.objects.filter(id=id)
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

    def _upfile_handler(self, postfile=None):
        if postfile:
            if postfile.get('bkp_pic_bp', ''):
                bgp = {}
                fname, fpath = self._recv_file_oss(f=postfile.get('bkp_pic_bp'), type=UploadFileType.IMG)
                bgp['name'] = fname
                # bgp['path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                bgp['path'] = fpath
                return bgp

    def _modify_pic(self, data=None, upfile=None):
        # pic_info_key = ['name', 'element_num', 'path', 'description', 'status']
        pic_update_map = {}
        pic_update_map['name'] = data.get('name')
        pic_update_map['element_num'] = len(data.getlist('target_name'))
        # pic_update_map['path'] = ''
        pic_update_map['description'] = data.get('description')
        pic_update_map['status'] = 1 if data.get('status')  else 0

        if upfile:
            pic_update_map['path'] = self._upfile_handler(upfile).get('path')

        return pic_update_map

    def add_pic(self, data=None, upfile=None):
        try:
            pic_update_map = self._modify_pic(data=data, upfile=upfile)

            if pic_update_map:
                obj = BKPPic.objects.create(**pic_update_map)
                return obj.id

            return None
        except Exception, e:
            print traceback.print_exc()

    def edit_pic(self, data=None, upfile=None):
        try:
            pic_id = data.get('pic_id')
            pic_update_map = self._modify_pic(data=data, upfile=upfile)
            if pic_update_map:
                num = BKPPic.objects.filter(id=pic_id).update(**pic_update_map)
                if num > 0:
                    print 'success update'
                return num

            return None
        except Exception, e:
            print traceback.print_exc()

    def save_target(self, bkp_pic_id, data):

        namel = data.getlist('target_name')
        top_left_xl = data.getlist('top_left_x')
        top_left_yl = data.getlist('top_left_y')
        bottom_right_xl = data.getlist('bottom_right_x')
        bottom_right_yl = data.getlist('bottom_right_y')

        target_key = ['name', 'top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y']
        for item in zip(namel, top_left_xl, top_left_yl, bottom_right_xl, bottom_right_yl):

            update = dict(zip(target_key, item))
            update['bkp_pic_id'] = bkp_pic_id
            target = BKPTarget.objects.create(**update)
            if target:
                print 'save target', target.id

    def _find_extern_target_info(self, all, target_name):
        for k in all:
            save_name = k.get('name')
            if save_name == target_name:
                new = copy.deepcopy(k)
                return new
            else:
                continue

        return {}

    def edit_target(self, data):
        save_target_extern_info = {}

        bkp_pic_id = data.get('pic_id')

        namel = data.getlist('target_name')
        top_left_xl = data.getlist('top_left_x')
        top_left_yl = data.getlist('top_left_y')
        bottom_right_xl = data.getlist('bottom_right_x')
        bottom_right_yl = data.getlist('bottom_right_y')

        target_key = ['name', 'top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y']

        # 删除上一张图片的所有target 因为picid 相同  所以不能先创建再删除 注意！
        obj = BKPTarget.objects.filter(bkp_pic_id=bkp_pic_id)
        save_target_extern_info = obj.exclude(Q(target_audio_path='') | Q(desc_audio_path='')).values('name',
                                                                                                      'target_audio_name',
                                                                                                      'target_audio_path',
                                                                                                      'desc_audio_name',
                                                                                                      'desc_audio_path',
                                                                                                      'description').distinct()

        # 注意 queryset 类型  obj.delete() 后对象进行释放  save_target_extern_info 为空
        # model_to_dict() 无法使用  该对象没有meta   fix

        keep = []
        for k in save_target_extern_info:
            keep.append(k)

        # keep = model_to_dict(save_target_extern_info)
        if obj.count() > 0:
            # 查找到该图片已经配置过目标，保存所有目标的音频视频描述  ［｛ ｝,{ }］
            # save_target_extern_info = obj.exclude(Q(target_audio_path='') | Q(desc_audio_path='')).values('name','target_audio_name', 'target_audio_path', 'desc_audio_name', 'desc_audio_path', 'description').distinct()
            # save_target_extern_info = copy.deepcopy(save_target_extern_info)
            # 允许添加重复的行 无法区分那些是新增那些是修改 因此以当次提交的列表为准
            # save_target_extern_info = self.save_target_extern_info(model_to_dict(obj.distinct('name').all()))
            # print 'save target extern info',save_target_extern_info
            obj.delete()

        # 重新创建新的target   pic——ID仍然相同
        for item in zip(namel, top_left_xl, top_left_yl, bottom_right_xl, bottom_right_yl):
            update = dict(zip(target_key, item))
            update['bkp_pic_id'] = bkp_pic_id
            if keep:  # 逻辑和下面else 重复  fix this
                print 'find it', self._find_extern_target_info(keep, update['name'])
                update.update(self._find_extern_target_info(keep, update['name']))
            else:
                update.update(self.get_target_extern_info(update['name']))
            target = BKPTarget.objects.create(**update)
            if target:
                pass
                # print 'save target', target.id

    def get_target_extern_info(self, target_name):
        extern_info = {}
        extern_key = ['target_audio_name', 'target_audio_path', 'desc_audio_name', 'desc_audio_path', 'description']
        obj = BKPTarget.objects.filter(name=target_name).exclude(
            Q(target_audio_path='') | Q(desc_audio_path='')).first()
        if obj:  # 目标内容已经配置 获取其内容
            for k in extern_key:
                extern_info[k] = getattr(obj, k)
            return extern_info
        else:
            return {}

    def pic_get(self, pic_id):
        """
          GET LIST BY id
          """
        if pic_id is None:
            return None
        try:
            pic = BKPPic.objects.get(id=pic_id)
        except IntegrityError:
            print 'error'
        pic_data = to_dict(pic)
        segment_all = BKPTarget.objects.filter(bkp_pic_id=pic_id).all()
        pic_data['segments'] = [to_dict(v) for v in segment_all]

        return pic_data


# ＝＝＝＝目标录音和解析＝＝＝＝＝＝
class BKPTargetCommand(CommandHelper):
    def __init__(self, data=None):
        super(BKPTargetCommand, self).__init__(data)

    def _get_target_status(self, ele_name):

        obj = BKPTarget.objects.filter(name=ele_name)
        if obj.count() == 0:
            return '未发布'
        else:
            entry = obj.all()[0]
            if entry.desc_audio_name and entry.target_audio_name:
                return '已发布'
            elif entry.desc_audio_name or entry.target_audio_name:
                return '部分发布'
            else:
                return '未发布'

    def _get_id_by_name(self, ele_name):
        obj = BKPTarget.objects.filter(name=ele_name)
        if obj.count() > 0:
            return obj.all()[0].id
        else:
            return 0

    def get_target_list(self):
        target_list = BKPTarget.objects.all()
        target_list.query.group_by = ['name']
        res = []
        for i in target_list:
            tmp = {}
            tmp['name'] = i.name
            tmp['status'] = self._get_target_status(i.name)
            tmp['id'] = self._get_id_by_name(i.name)
            if tmp not in res:
                res.append(tmp)

        return res

    def target_by_id(self, target_id=None):
        if not target_id:
            return

        target = BKPTarget.objects.filter(id=target_id).all()[0]
        return to_dict(target)

    def _md5(self, str=''):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def _modify_target(self, data=None, upfile=None):

        target = self.target_by_id(data.get('target_id'))

        desc = data.get('description', '')

        target_name = target['name']

        try:
            entrys = BKPTarget.objects.filter(name=target_name).all()
            bkp = {}

            if upfile:
                if upfile.get('target_audio', ''):
                    fname, fpath = self._recv_file_oss(f=upfile.get('target_audio'), type=UploadFileType.AUDIO)
                    bkp['target_audio_name'] = fname
                    # bkp['target_audio_path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                    bkp['target_audio_path'] = fpath

                if upfile.get('desc_audio', ''):
                    fname, fpath = self._recv_file_oss(f=upfile.get('desc_audio'), type=UploadFileType.AUDIO)
                    bkp['desc_audio_name'] = fname
                    # bkp['desc_audio_path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                    bkp['desc_audio_path'] = fpath

            try:
                for entry in entrys:
                    for k in ['target_audio_name', 'target_audio_path', 'desc_audio_name', 'desc_audio_path']:
                        if bkp and bkp.has_key(k): setattr(entry, k, bkp.get(k))
                        setattr(entry, 'description', desc)
                    entry.save()
            except Exception, e:
                return ('msg', e.message)

            return ('msg', '保存成功')

        except Exception, e:
            return ('msg', '上传错误')

    def add_target(self, data=None, upfile=None):
        try:
            return self._modify_target(data=data, upfile=upfile)
        except Exception, e:
            print traceback.print_exc()


# ＝＝＝＝＝＝关卡＝＝＝＝＝＝＝＝＝＝＝
class BKPLevelDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已发布' if obj.status else '未发布'

    def getval_target(self, obj, default=''):
        entrys = BKPRound.objects.filter(bkp_level_id=obj.id).all()
        if entrys:
            return {'name': '   '.join(set([x.bkp_target_name.strip() for x in entrys if x is not None]))}
        else:
            return {'name': '未设置目标'}

    def getval_type(self, obj, default=''):
        # 0: 课后乐园
        # 1: 随堂游戏
        return '随堂游戏' if obj.type else '课后乐园'

    def getval_opt(self, obj, default=''):
        return {'publish': '已发布' if obj.status else '未发布',
                'copy': obj.id,
                'picid': obj.id,
                'edit': '查看详情' if obj.status else '编辑'}


class BKPLevelDQ(DataSQLQuery):
    model = BKPLevel
    data_model = BKPLevelDB
    pass


class BKPLevelCommand(CommandHelper):
    def __init__(self, data=None):
        super(BKPLevelCommand, self).__init__(data)

    def _del(self, id):

        obj = BKPLevel.objects.filter(id=id)
        if obj.count() > 0:
            obj.delete()

        obj = BKPRound.objects.filter(bkp_level_id=id)
        if obj.count() > 0:
            obj.delete()

        return ('msg', '删除成功')

    def _copy(self, id):
        from django.forms import model_to_dict
        instance = BKPLevel.objects.get(id=id)
        kwargs = model_to_dict(instance, exclude=['id', 'status'])
        new_instance = BKPLevel.objects.create(**kwargs)
        return ('msg', '复制成功')

    def _check_valid(self, entry):
        '''
        :return: 校验名字 seq是否重复   重复的无法发布
        '''
        obj = BKPLevel.objects.filter(type=entry.type).filter(Q(name=entry.name) | Q(seq=entry.seq))
        if obj.count() > 1:  # 存在重复
            return False
        else:
            return True

    def _publish(self, id):
        obj = BKPLevel.objects.filter(id=id)
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
                    return ('msg', '操作失败 名字或顺序重复')
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

    def _md5(self, str=''):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def _upfile_handler(self, postfile=None):
        if postfile:
            if postfile.get('bkp_bgm', ''):
                bgp = {}
                fname, fpath = self._recv_file_oss(f=postfile.get('bkp_bgm'), type=UploadFileType.AUDIO)
                bgp['name'] = fname
                # bgp['path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                bgp['path'] = fpath
                return bgp

    def _modify_level(self, data=None, upfile=None):
        level_info_key = ['name', 'type', 'seq', 'description', 'status']
        level_update_map = {}
        level_update_map['name'] = data.get('name')
        level_update_map['type'] = data.get('type', 0)
        level_update_map['seq'] = data.get('seq', 0)
        level_update_map['description'] = data.get('description')
        level_update_map['status'] = 1 if int(data.get('status', 0)) > 0 else 0

        if upfile:
            res = self._upfile_handler(upfile)
            level_update_map['bgm_name'] = res['name']
            level_update_map['bgm_path'] = res['path']

        return level_update_map

    def bkp_level_modify(self, data=None, upfile=None):
        try:
            level_update_map = self._modify_level(data=data, upfile=upfile)
            if level_update_map:
                obj = BKPLevel.objects.create(**level_update_map)
                return obj.id
            return None
        except Exception, e:
            print traceback.print_exc()

    def edit_level(self, data=None, upfile=None):
        try:
            level_id = data.get('level_id')
            level_update_map = self._modify_level(data=data, upfile=upfile)
            if level_update_map:
                num = BKPLevel.objects.filter(id=level_id).update(**level_update_map)
                if num > 0:
                    print 'success update'
                return num

            return None
        except Exception, e:
            print traceback.print_exc()

    @classmethod
    def del_round(cls, id):
        try:
            print 'roundid', id
            obj = BKPRound.objects.filter(id=id)
            if obj.count() > 0:
                obj.delete()
                return id
            return None
        except Exception, e:
            print traceback.print_exc()

    def save_round(self, bkp_level_id, data):

        # bkp_target_namel = data.getlist('target_name')
        bkp_target_namel = [x.split(u'＊')[0] for x in data.getlist('target_name')]
        timel = data.getlist('time')
        bkp_pic_idl = data.getlist('pic_id')

        # 生成序号  注意！  前端表格中的seq字段为自动填充
        obj = BKPRound.objects.filter(bkp_level_id=bkp_level_id).order_by('-seq')
        if obj.count() > 0:
            seq = obj.all()[0].seq
        else:
            seq = 0
        seql = [x for x in range(seq + 1, len(timel) + 1 + seq)]

        target_key = ['bkp_target_name', 'time', 'seq', 'bkp_pic_id', ]
        for item in zip(bkp_target_namel, timel, seql, bkp_pic_idl):
            update = dict(zip(target_key, item))
            update['bkp_level_id'] = bkp_level_id
            target = BKPRound.objects.create(**update)
            if target:
                print 'save target', target.id

    def _update_round(self, data):
        try:
            level_id = data.get('level_id')
            bkp_round_idl = data.getlist('bkp_round_id')
            pic_idl = data.getlist('bkp_pic_id')
            bkp_target_namel = data.getlist('bkp_target_name')
            bkp_time = data.getlist('bkp_time')

            round_key = ['id', 'bkp_pic_id', 'bkp_target_name', 'time']
            update = []
            for item in zip(bkp_round_idl, pic_idl, bkp_target_namel, bkp_time):
                tmp = dict(zip(round_key, item))
                tmp['bkp_level_id'] = level_id
                update.append(tmp)

            return update
        except Exception, e:
            print traceback.print_exc()

    def edit_round(self, data):
        level_id = data.get('level_id')
        self.save_round(level_id, data)

        db_update = self._update_round(data)
        if db_update:
            for item in db_update:
                if item['id']:
                    BKPRound.objects.filter(id=item['id']).update(**item)

    def level_get(self, level_id):
        """
          GET LIST BY id
          """
        if level_id is None:
            return None

        level = BKPLevel.objects.get(id=level_id)
        pic_data = to_dict(level)
        segment_all = BKPRound.objects.filter(bkp_level_id=level_id).order_by('seq').all()
        pic_data['segments'] = [to_dict(v) for v in segment_all]
        for item in pic_data['segments']:
            try:
                r = BKPPic.objects.get(id=item['bkp_pic_id'])
                item['bkp_pic_name'] = r.name if r  else '图片丢失'
            except:
                item['bkp_pic_name'] = '图片丢失'
        return pic_data

    @classmethod
    def get_all_pics(cls):
        pics = []
        entrys = BKPPic.objects.all()
        return [to_dict(k) for k in entrys]

    def add_level(self, data, upfile):
        try:
            return self.bkp_level_modify(data=data, upfile=upfile)
        except Exception, e:
            print traceback.print_exc()
