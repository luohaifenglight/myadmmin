#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.db.models import Q
from django.db import connection
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .models import Institution, CourseSystem, Province, City
from backend.student.models import InstitutionExperience, Student
from backend.teacher.models import Teacher
from .enumtype import INSTITUTION_TYPE


class InstitutionDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已冻结' if obj.status else '正常'

    def getval_create_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.create_time) \
            if obj.create_time else ''

    def getval_type(self, obj, default=''):
        return INSTITUTION_TYPE.getDesc(obj.type)


class InstitutionDQ(DataSQLQuery):
    model = Institution
    data_model = InstitutionDB

    def filter_create_time(self, srch_key, srch_val, regex=False):
        if not isinstance(srch_val, list) or len(srch_val) != 2:
            return Q()
        start, end = srch_val
        import time
        start = int(time.mktime(time.strptime(start,'%Y-%m-%d')))
        end = int(time.mktime(time.strptime(end, '%Y-%m-%d')))
        print start, end
        if start and end:
            suf = 'range'
            val = [start, end]
        elif not start and not end:
            return Q()
        elif not start:
            suf = 'lt'
            val = end
        elif not end:
            suf = 'gte'
            val = start
        return Q(**{'{}__{}'.format(srch_key, suf): val})


class InstitutionCommand:

    def __init__(self, data=None):
        self.data = data

    def institution_edit(self, institution_id=None):
        institution_info = self.data
        course_system = institution_info.pop('course_system', [])
        institution_info['city_id'] = institution_info.pop('city', None)
        if institution_info is None:
            return None
        if institution_id is None:
            try:
                institution = Institution.objects.create(**institution_info)
                print 'inis_id:%s' % (institution.id)
            except IntegrityError:
                print 'error'
        else:
            try:
                institution = Institution.objects.get(id=institution_id)
            except:
                print 'error'

            for k, v in institution_info.iteritems():
                setattr(institution, k, v)
            institution.save()
        if course_system:
            new_s = set(CourseSystem.objects.filter(id__in=course_system))
            old_s = set(institution.course_system.all())
            institution.course_system.add(*(new_s - old_s))
            institution.course_system.remove(*(old_s - new_s))
            create_experience_num(institution.id, institution.experience_student_num)
        return institution.id

    def institution_get(self, institution_id):
        """
        GET LIST BY id
        """
        if institution_id is None:
            return None
        try:
            institution = Institution.objects.get(id=institution_id)
        except IntegrityError:
            print 'error'
        institution_data = to_dict(institution)
        institution_data['province'] = {
            'id': institution.city.province.id,
            'text': institution.city.province.name,
        }
        institution_data['city_name'] = institution.city.name
        return institution_data

    @classmethod
    def reset_status(cls, id, reset_type=0):
        if reset_type:
            teacher = Teacher.objects.get(id=id)
            teacher.status = 1 - teacher.status
            teacher.save()
            return True
        institution = Institution.objects.get(id=id)
        institution.status = 1 - institution.status
        # add 2017.7.12 10:00 机构冻结，机构下所有老师与所有管理员冻结
        teachers = institution.teachers.all()
        for teacher_temp in teachers:
            teacher_temp.status = institution.status
            teacher_temp.save()
        admins = institution.admins.all()
        for admin in admins:
            admin.status = institution.status
            admin.save()
        institution.save()
        return True

    @classmethod
    def get_course(cls, id):
        groups = CourseSystem.objects.filter(institutions__id=id)
        results = [
            {
                'id': obj.id,
                'text': u'{}:{}'.format(
                    obj.id,
                    obj.name,
                ),

            } for obj in groups
            ]
        return results


def province_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    query = Province.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


def city_choices(q='', page=1, num=30, province=None, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    if province:
        qry = qry & Q(province__id=province)
    query = City.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


def course_system_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q)
    query = CourseSystem.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}'.format(
                obj.id,
                obj.name,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}


def get_password(password):
    import hmac
    return hmac.new('JYQJ@FLYYJS', password).hexdigest()


def create_experience_num(institution_id, number):
    if number >= 0:
        current_num = InstitutionExperience.objects.filter(institution_id=institution_id).count()
        start_num = number - current_num
        if start_num < 0:
            all_ex = InstitutionExperience.objects.filter(institution_id=institution_id).order_by('-id')
            need_delete = all_ex[0:(-1)*start_num]
            others_tables = [
                "tb_course_student",
                "tb_score_student_record",
                "tb_student_class_record",
                "tb_student_score_hzq",
                "tb_homework_submit_record",
                "tb_balloon_play_record",
                "tb_bkp_play_record",
                "tb_course_record",
                "tb_student_class",
                "tb_student_class_record",
            ]
            delete_sql = 'delete from `%s`'
            for ex_stu in need_delete:
                student_id = ex_stu.student.id
                for table in others_tables:
                    excute_sql = delete_sql % str(table)
                    excute_sql = excute_sql + ' where student_id=%s'
                    cursor = connection.cursor()
                    cursor.execute(excute_sql, [student_id])
                mobile = ex_stu.student.mobile
                push_sql = 'delete from tb_push where push_id=%s and type=3'
                cursor = connection.cursor()
                cursor.execute(push_sql, [mobile])
                ex_stu.student.delete()
                #....
            for ex_tu_d in need_delete:
                ex_tu_d.delete()

        for num in xrange(current_num, number):
            middle_string = '00000%s' % str(institution_id)
            end_string = '0%s' % str(num)
            middle_string = middle_string[-6:]
            end_string = end_string[-2:]
            format_string = '199%s%s' % (middle_string, end_string)
            gender = int(num) % 2
            import time
            icon = "http://yyjs-online.oss-cn-beijing.aliyuncs.com/img/girl_default.png"
            if int(gender):  # 1-boy  2-girl  gender：1-boy  0-girl
                icon = "http://yyjs-online.oss-cn-beijing.aliyuncs.com/img/boy_default.png"
            student_data = {
                'name': '体验%s' % str(num),
                'password': get_password(format_string[-6:]),
                'mobile': format_string,
                'gender': gender,
                'create_time': int(time.time()),
                'icon': icon,
                'is_experience_num': 1,

            }
            print 'tayanzhenghao:', str(student_data)
            student_id = Student.objects.create(**student_data)
            student_expreiment_data = {
                'student_id': student_id.id,
                'institution_id': institution_id,
            }
            InstitutionExperience.objects.create(**student_expreiment_data)
            push_sql = '''insert into tb_push(push_id, type) values (%s, 3)'''
            cursor = connection.cursor()
            cursor.execute(push_sql, [format_string])



def get_student_ids(inis_id=None):
    all_ids = []
    if inis_id:
        all_student = InstitutionExperience.objects.filter(institution_id=inis_id)
    else:
        all_student = InstitutionExperience.objects.all()
    all_ids = [x.student_id for x in all_student]
    return all_ids


def reset_student_password(id, pwd):
    student = Student.objects.get(id=id)
    if student:
        password = get_password(pwd)
        student.password = password
        student.save()



