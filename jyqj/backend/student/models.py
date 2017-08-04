#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.db import models
from backend.teacher.models import Teacher, CourseSystem, Institution
from backend.classes.models import Class


class Student(models.Model):
    create_teacher = models.ForeignKey(Teacher, related_name='students')
    name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    icon = models.CharField(max_length=200)
    gender = models.IntegerField(default=0, blank=True, null=True)
    create_time = models.BigIntegerField(default=int(time.time()))
    status = models.IntegerField(default=0, blank=True, null=True)
    is_experience_num = models.IntegerField(default=0, blank=True, null=True)
    coin_num = models.IntegerField(default=0, blank=True, null=True)
    star_num = models.IntegerField(default=0, blank=True, null=True)
    classes = models.ManyToManyField(Class, verbose_name=u'学生老师', through='StudentClass',
                                           related_name='students')

    class Meta:
        db_table = 'tb_student'


class StudentClass(models.Model):
    student = models.ForeignKey(Student)
    classes = models.ForeignKey(Class, db_column='class_id')

    class Meta:
        auto_created = True
        db_table = 'tb_student_class'


class StudentClassRecord(models.Model):
    student = models.ForeignKey(Student)
    classes = models.ForeignKey(Class, db_column='class_id')
    command = models.IntegerField(default=0, blank=True, null=True)
    create_time = models.BigIntegerField(default=int(time.time()))

    class Meta:
        auto_created = True
        db_table = 'tb_student_class_record'


class InstitutionExperience(models.Model):
    institution = models.ForeignKey(Institution)
    student = models.ForeignKey(Student, related_name='experience_students')

    class Meta:
        db_table = 'tb_institution_experience'

