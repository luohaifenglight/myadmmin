#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.dataquery import DataBuilder, DataSQLQuery
from django.db.models import Q
from .models import BalloonSubLevel, BalloonLevel, BalloonSubLevelOctave
from django.forms import model_to_dict
import traceback

from .models import BalloonSubLevel, BalloonLevel, BalloonSubLevelOctave
from .forms import SublevelInfo
from django.conf import settings
from utils.cmdhelper import CommandHelper, UploadFileType


class BalloonLevelDB(DataBuilder):
    pass


class BalloonLevelDQ(DataSQLQuery):
    model = BalloonLevel
    data_model = BalloonLevelDB
    pass


class BalloonLevelCommand(CommandHelper):
    def __init__(self, data=None):
        super(BalloonLevelCommand, self).__init__(data)

    def _copy(self, id):
        instance = BalloonSubLevel.objects.filter(id=id).get(id=id)
        kwargs = model_to_dict(instance, exclude=['id', 'status'])
        new_instance = BalloonSubLevel.objects.create(**kwargs)
        # copy oct
        oct = BalloonSubLevelOctave.objects.filter(sub_level_id=id).all()
        for t in oct:
            t.id = None
            t.sub_level_id = new_instance.id
            t.save()

    def _del(self, id):
        BalloonSubLevel.objects.filter(id=id).delete()
        sql = BalloonSubLevelOctave.objects.filter(sub_level_id=id)
        if sql.count() > 0:
            sql.delete()

    def _check_valid(self, entry):
        '''
        :return: 校验名字 seq是否重复   重复的无法发布
        '''
        # obj = BalloonSubLevel.objects.filter(status=1).filter(Q(name=entry.name) | Q(seq=entry.seq))
        obj = BalloonSubLevel.objects.filter(status=1).filter(level_id=entry.level_id, name=entry.name)
        if obj.count() >= 1:  # 存在重复
            return False

        if BalloonSubLevel.objects.filter(status=1).filter(
                        Q(level_id=entry.level_id, name=entry.name) & Q(seq=entry.seq)).count() >= 1:
            return False

        return True

    def _publish(self, id):
        obj = BalloonSubLevel.objects.filter(id=id)
        if obj.count() > 0:
            entry = obj.get(id=id)
            if self._check_valid(entry):
                entry.status = 1
                entry.save()
                msg = '发布成功'
            else:
                return ('msg', '操作失败 名字重复或顺序重复')

            return ('msg', msg)
        else:
            return ('msg', '操作失败')

    def _cancelpublish(self, id):
        sublevel_info = BalloonSubLevel.objects.filter(id=id)
        if len(sublevel_info) > 0:
            sublevel_info[0].status = 0
            sublevel_info[0].save()
            return ('msg', '操作成功')
        else:
            return ('msg', '操作失败')

    def get_all_sublevel(self, lid):
        res = []
        # todo fix  不再封装  直接查询进行返回
        sublevel_info = BalloonSubLevel.objects.filter(level_id=lid).order_by("seq").all()
        for item in sublevel_info:
            tmp = {}
            tmp['name'] = item.name
            tmp['seq'] = item.seq
            tmp['id'] = item.id
            tmp['seq'] = item.seq
            tmp['status'] = item.status
            tmp['level_id'] = item.level_id
            res.append(tmp)
        return res

    def modify(self, data=None):
        try:
            if data is None:
                return None
            opt = data.get('opt')
            id = data.get('id')
            lid = data.get('lid')

            if opt == 'copy':
                return self._copy(id)
            elif opt == 'del':
                return self._del(id)
            elif opt == 'edit' or opt == 'check':
                pass
            elif opt == 'publish':
                return self._publish(id)
            elif opt == 'cancelpublish':
                return self._cancelpublish(id)
        except Exception, e:
            print traceback.print_exc()

    def _check_postbody_with_db(self, pmap, instance, opt):
        if pmap is None:
            return ('msg', '元素参数错误')

        # print 'pmap ',pmap
        if opt == 'add':
            if 'name' in pmap:
                if instance.filter(name=pmap['name'], level_id=pmap['level_id']).count() > 0:
                    return ('msg', '名字重复')

                    # 处理元素部分   只勾选 不填写百分比［pitch, sing,score］

        sumv = 0
        for rate in ['pitch_rate', 'sing_rate', 'score_rate']:
            if rate in pmap:

                if int(pmap[rate]) > 100:
                    return ('msg', '元素参数错误 数值超过100%')

                sumv += int(pmap[rate])
        if sumv != 100:
            return ('msg', '元素参数错误 总和100%')

        return None

    def _ave_elem(self, pmap):
        # 处理元素部分   只勾选 不填写百分比［pitch, sing,score］
        ele = ['pitch', 'sing', 'score']
        new = {}
        if 'pitch_rate' in pmap or 'sing_rate' in pmap or 'score_rate' in pmap:
            return {}
        else:
            count = 0
            who = []
            for index, key in enumerate(ele):
                if key in pmap:
                    count += 1
                    who.append(1)
                else:
                    who.append(0)

            new['pitch_rate'] = 100 * who[0] / count
            new['sing_rate'] = 100 * who[1] / count
            new['score_rate'] = 100 * who[2] / count
            return new

    def _check_oct_value(self, oct_list=None, instance=None):
        if oct_list is None:
            return {'msg', '请填写音域'}

        if len(oct_list) > 2:
            return ('msg', '音域只能选择两组')

        sumv = 0
        for oct in oct_list:
            for ele in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                if ele in oct:
                    if sumv > 100:
                        return ('msg', '数值错误（所有百分比之和为100%）')
                    sumv += int(oct[ele])

        if sumv != 100:
            return ('msg', '数值错误（所有百分比之和为100%）')

        return None

    def _sublevel_edit(self, postbody=None, postfile=None, opt='add'):
        try:
            if postbody is None:
                return ('msg', '不能为空')

            sublevel_info = SublevelInfo(data=postbody)
            if sublevel_info.is_valid():
                update_map = {}
                for k in postbody:
                    v = sublevel_info.data.get(k, '')
                    if v:
                        newk = k if 'sublevel_' not in k else k.replace('sublevel_', '')
                        update_map[newk] = v
                    else:  # 未填写占比
                        pass
                # 添加特别的字段校验
                res = self._check_postbody_with_db(update_map, BalloonSubLevel.objects, opt)

                if res: return res

                oct_list = []
                for item in [sublevel_octave_up_o1, sublevel_octave_up_o, sublevel_octave_down_o1,
                             sublevel_octave_down_o]:
                    oct_map = {}
                    up = '0'
                    down = '0'
                    foot = '0'
                    for k in item:
                        v = postbody.get(k, '')
                        if v:
                            oct_map['sub_level_id'] = update_map['id'] if 'id' in update_map else ''
                            if 'up' in k: up = '1'
                            if 'down' in k: down = '1'

                            if '1' in k:
                                oct_map['octave_type'] = 'o1'
                            else:
                                oct_map['octave_type'] = 'o'

                            newk = k.split('_')[2].replace('1', '')
                            oct_map[newk] = v
                        else:  # 未填写占比
                            pass
                    if len(oct_map) > 0:
                        oct_map['keyboard'] = up + down + foot
                        oct_list.append(oct_map)

                # 校验音域输入正确与否
                res = self._check_oct_value(oct_list)
                if res: return res

                # 处理文件上传
                upfile = {}
                if postfile:
                    if postfile.get('sublevel_background', ''):
                        bgp = {}
                        fname, fpath = self._recv_file_oss(postfile.get('sublevel_background'), UploadFileType.IMG)
                        bgp['bgp_name'] = fname
                        # bgp['bgp_path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                        bgp['bgp_path'] = fpath
                        upfile['bgp'] = bgp

                    if postfile.get('sublevel_backmusic', ''):
                        bgm = {}
                        fname, fpath = self._recv_file_oss(postfile.get('sublevel_backmusic'), UploadFileType.AUDIO)
                        bgm['bgm_name'] = fname
                        # bgm['bgm_path'] = settings.NGINX_URL_PREFIX + 'uploadfiles/' + fpath
                        bgm['bgm_path'] = fpath
                        upfile['bgm'] = bgm

                if opt == 'add':
                    # 处理 sublevel 信息
                    # todo 校验数据项目 返回msg
                    if len(update_map) > 0:
                        if 'id' in update_map:
                            update_map.pop('id')

                        new_update = {}

                        for k in sublevel_key:
                            if k in update_map:
                                try:
                                    new_update[k] = int(update_map[k])
                                except Exception, e:
                                    new_update[k] = update_map[k]

                        try:
                            if 'id' in new_update:
                                new_update.pop('id')
                            new_level = BalloonSubLevel.objects.create(**new_update)

                        except Exception, e:
                            print 'create ', traceback.print_exc()
                    else:
                        return ('msg', '参数未空，添加失败')

                    # 处理文件上传
                    if len(upfile) > 0 and new_level:
                        if 'bgp' in upfile:
                            new_level.bgp_name = upfile['bgp']['bgp_name']
                            new_level.bgp_path = upfile['bgp']['bgp_path']
                            new_level.save()

                        if 'bgm' in upfile:
                            new_level.bgm_name = upfile['bgm']['bgm_name']
                            new_level.bgm_path = upfile['bgm']['bgm_path']
                            new_level.save()

                    # 处理音域设置问题
                    if oct_list:
                        for item in oct_list:
                            item['sub_level_id'] = new_level.id

                            BalloonSubLevelOctave.objects.create(**item)
                        return ('msg', '创建成功')

                elif opt == 'edit':
                    curlevel = BalloonSubLevel.objects.get(id=update_map['id'])
                    if curlevel:
                        for k, v in update_map.items():
                            if v == getattr(curlevel, k):
                                continue
                            else:
                                setattr(curlevel, k, v)

                        curlevel.save()
                        if len(upfile) > 0:
                            if 'bgp' in upfile:
                                curlevel.bgp_name = upfile['bgp']['bgp_name']
                                curlevel.bgp_path = upfile['bgp']['bgp_path']
                                curlevel.save()

                            if 'bgm' in upfile:
                                curlevel.bgm_name = upfile['bgm']['bgm_name']
                                curlevel.bgm_path = upfile['bgm']['bgm_path']
                                curlevel.save()

                    # 音域是一对多，如果需要修改音域，则删掉该关卡下的两个音域，重新建立
                    if oct_list and len(oct_list) > 0:
                        try:
                            sql = BalloonSubLevelOctave.objects.filter(sub_level_id=update_map['id'])
                            if sql.count() > 0:
                                sql.delete()
                        except Exception, e:
                            print e

                        for item in oct_list:
                            BalloonSubLevelOctave.objects.create(**item)

                    return ('msg', '保存成功')
                else:
                    return ('msg', '没有操作')

            else:  # 序列化出错 提示缺省内容
                msg = []
                for k in sublevel_info.errors:
                    newk = k if 'sublevel_' not in k else k.replace('sublevel_', '')

                    if newk in sublevel_key:
                        msg.append(sublevel_key.get(newk))

                return ('msg', '参数错误:' + ' '.join(msg))
        except Exception, e:
            print traceback.print_exc()


sublevel_key = {'id': '主键', 'name': '关卡名称', 'level_id': '所属关卡', 'seq': '关卡顺序',
                'description': '关卡描述', 'pitch_rate': '音名占比',
                'sing_rate': '唱名占比', 'score_rate': '五线谱占比',
                'hint_rate': '有提示占比', 'pop_interval': '气球出现速度',
                'fly_time': '气球停留时间', 'level_time': '关卡时长', 'bgm_name': '背景音乐名称',
                'bgm_path': '背景音乐路径', 'bgp_name': '背景图片', 'bgp_path': '背景图片路径',
                # 'lock_status': '解锁状态',
                'status': '发布状态'}

sublevel_octave_up_o1 = ['up_little_' + x + '1_rate' for x in ['c', 'd', 'e', 'f', 'g', 'a', 'b']]
sublevel_octave_up_o = ['up_little_' + x + '_rate' for x in ['c', 'd', 'e', 'f', 'g', 'a', 'b']]

sublevel_octave_down_o1 = ['down_little_' + x + '1_rate' for x in ['c', 'd', 'e', 'f', 'g', 'a', 'b']]
sublevel_octave_down_o = ['down_little_' + x + '_rate' for x in ['c', 'd', 'e', 'f', 'g', 'a', 'b']]

sublevel_octave_form = sublevel_octave_up_o1 + sublevel_octave_up_o + sublevel_octave_down_o1 + sublevel_octave_down_o

sublevel_octave = {'sub_level_id': '', 'octave_type': '', 'keyboard': '',
                   'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'a': '', 'b': ''}
