#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from utils.dict_mixin import DictMixin
from backend.institution.models import Institution
import time


class BackendModule(DictMixin, models.Model):
    name = models.CharField(u'模块名', max_length=100, unique=True)
    title = models.CharField(u'模块名称', max_length=100)

    def init_perms(self):
        # init can_view, can_create, can_modify as default perms
        DEFAULT_PERMS = [
            {'name': 'can_view', 'title': u'查看'},
            {'name': 'can_create', 'title': u'新增'},
            {'name': 'can_modify', 'title': u'修改'},
        ]
        for perm in DEFAULT_PERMS:
            BackendPermission.objects.get_or_create(
                name=perm['name'],
                title=perm['title'],
                module=self,
            )

    class Meta:
        db_table = 'tb_module'


class BackendPermission(DictMixin, models.Model):
    name = models.CharField(u'权限名', max_length=100)
    title = models.CharField(u'权限名称', max_length=100)
    module = models.ForeignKey(BackendModule, verbose_name=u'所属模块')

    class Meta:
        unique_together = (('name', 'module'),)

    def __unicode__(self):
        return self.code

    @property
    def code(self):
        return '%s.%s' % (self.module.name, self.name)

    @property
    def codename(self):
        return u'%s-%s' % (self.module.title, self.title)

    class Meta:
        db_table = 'tb_permission'


class BackendGroup(DictMixin, models.Model):
    name = models.CharField(u'组标题', max_length=100)
    members = models.ManyToManyField(User, verbose_name=u'组内成员', blank=True,
                                     related_name='belong_groups')
    permissions = models.ManyToManyField(BackendPermission, blank=True)
    status = models.IntegerField(verbose_name=u'z', default=0)
    create_time = models.BigIntegerField(default=time.time())

    class Meta:
        db_table = 'tb_role'


class Admin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accountuser')
    department = models.IntegerField(verbose_name=u'部门类型', default=0)
    mobile = models.CharField(max_length=40)
    status = models.BooleanField(default=False)
    type = models.IntegerField(verbose_name=u'管理员类型', default=0)
    create_time = models.BigIntegerField(default=time.time())
    institution = models.ForeignKey(Institution, verbose_name=u'机构', related_name="admins")

    class Meta:
        db_table = 'tb_admin'

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Admin.objects.get(user=self.user)
                self.pk = p.pk
            except Admin.DoesNotExist:
                pass

        super(Admin, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Admin()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)
