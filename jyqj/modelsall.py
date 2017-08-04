# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbAdmin(models.Model):
    department = models.IntegerField()
    mobile = models.CharField(max_length=40)
    status = models.IntegerField()
    type = models.IntegerField()
    create_time = models.BigIntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    institution_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_admin'


class TbBalloonGlobalSetting(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    star1 = models.IntegerField()
    star2 = models.IntegerField()
    star3 = models.IntegerField()
    star4 = models.IntegerField()
    star5 = models.IntegerField()
    double_rate = models.IntegerField()
    triple_rate = models.IntegerField()
    minus_point = models.IntegerField()
    plus_point = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_balloon_global_setting'


class TbBalloonLevel(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    type = models.IntegerField()
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_balloon_level'


class TbBalloonOctave(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    sub_level_id = models.IntegerField(blank=True, null=True)
    octave_type = models.CharField(max_length=5, blank=True, null=True)
    keyboard = models.CharField(max_length=3)
    c = models.IntegerField()
    d = models.IntegerField()
    e = models.IntegerField()
    f = models.IntegerField()
    g = models.IntegerField()
    a = models.IntegerField()
    b = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_balloon_octave'


class TbBalloonPlayRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField()
    sub_level_id = models.IntegerField()
    point = models.IntegerField(blank=True, null=True)
    star_num = models.IntegerField(blank=True, null=True)
    coin_num = models.IntegerField(blank=True, null=True)
    right_num = models.IntegerField(blank=True, null=True)
    wrong_num = models.IntegerField(blank=True, null=True)
    total_num = models.IntegerField(blank=True, null=True)
    time = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_balloon_play_record'


class TbBalloonSubLevel(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    level_id = models.IntegerField()
    name = models.CharField(max_length=20, blank=True, null=True)
    seq = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    pitch_rate = models.IntegerField(blank=True, null=True)
    sing_rate = models.IntegerField(blank=True, null=True)
    score_rate = models.IntegerField(blank=True, null=True)
    hint_rate = models.IntegerField(blank=True, null=True)
    pop_interval = models.IntegerField()
    fly_time = models.IntegerField()
    level_time = models.IntegerField(blank=True, null=True)
    bgm_name = models.CharField(max_length=20, blank=True, null=True)
    bgm_path = models.CharField(max_length=200, blank=True, null=True)
    bgp_name = models.CharField(max_length=20, blank=True, null=True)
    bgp_path = models.CharField(max_length=200, blank=True, null=True)
    status = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tb_balloon_sub_level'


class TbBkpGlobalSetting(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    star1 = models.IntegerField()
    star2 = models.IntegerField()
    star3 = models.IntegerField()
    star4 = models.IntegerField()
    star5 = models.IntegerField()
    minus_point = models.IntegerField()
    plus_point = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_bkp_global_setting'


class TbBkpLevel(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    type = models.IntegerField()
    seq = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    bgm_name = models.CharField(max_length=20, blank=True, null=True)
    bgm_path = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bkp_level'


class TbBkpPic(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    element_num = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bkp_pic'


class TbBkpPlayRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField()
    bkp_level_id = models.IntegerField()
    point = models.IntegerField(blank=True, null=True)
    star_num = models.IntegerField(blank=True, null=True)
    coin_num = models.IntegerField(blank=True, null=True)
    right_num = models.IntegerField(blank=True, null=True)
    wrong_num = models.IntegerField(blank=True, null=True)
    total_num = models.IntegerField(blank=True, null=True)
    time = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bkp_play_record'


class TbBkpRound(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    bkp_level_id = models.IntegerField()
    bkp_target_name = models.CharField(max_length=100)
    time = models.IntegerField()
    seq = models.IntegerField()
    bkp_pic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bkp_round'


class TbBkpTarget(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    bkp_pic_id = models.IntegerField()
    name = models.CharField(max_length=20, blank=True, null=True)
    top_left_x = models.IntegerField()
    top_left_y = models.IntegerField()
    bottom_right_x = models.IntegerField()
    bottom_right_y = models.IntegerField()
    target_audio_name = models.CharField(max_length=100, blank=True, null=True)
    target_audio_path = models.CharField(max_length=255, blank=True, null=True)
    desc_audio_name = models.CharField(max_length=100, blank=True, null=True)
    desc_audio_path = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_bkp_target'


class TbCity(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    province_id = models.IntegerField()
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_city'


class TbClass(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    create_teacher_id = models.IntegerField()
    teacher_id = models.IntegerField()
    name = models.CharField(max_length=100)
    course_system_id = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.BigIntegerField()
    create_time = models.BigIntegerField()
    course_rate = models.IntegerField(blank=True, null=True)
    class_status = models.IntegerField()
    share_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_class'


class TbClassSectionRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    course_id = models.IntegerField()
    class_id = models.IntegerField()
    unit_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section_type = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_class_section_record'


class TbClassShare(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    class_id = models.IntegerField()
    original_teacher_id = models.IntegerField()
    share_teacher_id = models.IntegerField()
    share_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tb_class_share'


class TbClassTransfer(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    class_id = models.IntegerField()
    original_teacher_id = models.IntegerField()
    current_teacher_id = models.IntegerField()
    admin_id = models.IntegerField()
    transfer_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tb_class_transfer'


class TbCourse(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    course_system_id = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=20, blank=True, null=True)
    seq = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_course'


class TbCourseClass(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    class_id = models.IntegerField()
    course_id = models.IntegerField()
    teacher_id = models.IntegerField(blank=True, null=True)
    teach_time = models.BigIntegerField(blank=True, null=True)
    course_status = models.IntegerField()
    unit_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_course_class'


class TbCourseRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    course_class_id = models.IntegerField()
    student_id = models.IntegerField()
    complete_num = models.IntegerField(blank=True, null=True)
    star_num = models.IntegerField(blank=True, null=True)
    coin_num = models.IntegerField(blank=True, null=True)
    error_num = models.IntegerField(blank=True, null=True)
    miss_num = models.IntegerField(blank=True, null=True)
    slow_num = models.IntegerField(blank=True, null=True)
    fast_num = models.IntegerField(blank=True, null=True)
    time_num = models.IntegerField(blank=True, null=True)
    total_num = models.IntegerField(blank=True, null=True)
    complete_time = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    keyboard = models.CharField(max_length=3, blank=True, null=True)
    right_num = models.IntegerField(blank=True, null=True)
    unit_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section_type = models.IntegerField(blank=True, null=True)
    course_type = models.IntegerField(blank=True, null=True)
    score_id = models.IntegerField(blank=True, null=True)
    fast_off_num = models.IntegerField(blank=True, null=True)
    slow_off_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_course_record'


class TbCourseStudent(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    course_class_id = models.IntegerField()
    student_id = models.IntegerField()
    rank = models.IntegerField(blank=True, null=True)
    complete_num = models.IntegerField(blank=True, null=True)
    is_online = models.IntegerField()
    star_num = models.IntegerField(blank=True, null=True)
    coin_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_course_student'


class TbCourseSystem(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_course_system'


class TbCourseUnit(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    course_id = models.IntegerField()
    unit_id = models.IntegerField()
    seq = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_course_unit'


class TbFileManagement(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=100)
    type = models.IntegerField()
    time = models.BigIntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_file_management'


class TbHomeworkPractice(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    section_id = models.IntegerField()
    score_id = models.IntegerField()
    star_num = models.IntegerField()
    keyboard = models.CharField(max_length=3, blank=True, null=True)
    times = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_homework_practice'


class TbHomeworkSubmitRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    class_id = models.IntegerField()
    course_id = models.IntegerField()
    student_id = models.IntegerField()
    score_id = models.IntegerField()
    unit_id = models.IntegerField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    section_type = models.IntegerField(blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_homework_submit_record'


class TbHzqScore(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    whole_score_id = models.IntegerField()
    staff1_score_id = models.IntegerField()
    staff2_score_id = models.IntegerField(blank=True, null=True)
    staff3_score_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)
    staff1_name = models.CharField(max_length=10)
    staff2_name = models.CharField(max_length=10)
    staff3_name = models.CharField(max_length=10)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_hzq_score'


class TbInstitution(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    city_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    concurrent_num = models.IntegerField(blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_institution'


class TbInstitutionCourseSystem(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    institution_id = models.IntegerField()
    course_system_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_institution_course_system'


class TbModule(models.Model):
    name = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_module'


class TbOperationLog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    admin_id = models.IntegerField(blank=True, null=True)
    visitor_ip = models.CharField(max_length=20, blank=True, null=True)
    visit_time = models.BigIntegerField(blank=True, null=True)
    operation_path = models.CharField(max_length=20, blank=True, null=True)
    action = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_operation_log'


class TbPermission(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    module = models.ForeignKey(TbModule, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tb_permission'


class TbProvince(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_province'


class TbPush(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    push_id = models.CharField(max_length=20)
    token = models.CharField(max_length=32, blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_push'


class TbRole(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'tb_role'


class TbRoleMembers(models.Model):
    backendgroup = models.ForeignKey(TbRole, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tb_role_members'
        unique_together = (('backendgroup', 'user'),)


class TbRolePermissions(models.Model):
    backendgroup = models.ForeignKey(TbRole, models.DO_NOTHING)
    backendpermission = models.ForeignKey(TbPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tb_role_permissions'
        unique_together = (('backendgroup', 'backendpermission'),)


class TbScore(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    admin_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)
    music_type = models.IntegerField(blank=True, null=True)
    music_category = models.IntegerField(blank=True, null=True)
    score_type = models.IntegerField(blank=True, null=True)
    ratio = models.IntegerField(blank=True, null=True)
    keyboard = models.CharField(max_length=3)
    xml_name = models.CharField(max_length=20)
    xml_path = models.CharField(max_length=100)
    b00_name = models.CharField(max_length=20)
    b00_path = models.CharField(max_length=100)
    b00_syx = models.CharField(max_length=200, blank=True, null=True)
    sample_midi_name = models.CharField(max_length=20)
    sample_midi_path = models.CharField(max_length=100)
    compare_midi_name = models.CharField(max_length=20)
    compare_midi_path = models.CharField(max_length=100)
    sample_audio_name = models.CharField(max_length=20, blank=True, null=True)
    sample_audio_path = models.CharField(max_length=100, blank=True, null=True)
    is_weak = models.IntegerField()
    is_repeat = models.IntegerField()
    poster_name = models.CharField(max_length=20, blank=True, null=True)
    poster_path = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.BigIntegerField()
    status = models.IntegerField()
    weak_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_score'


class TbScoreOptional(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    score_id = models.IntegerField()
    type = models.IntegerField()
    seq = models.IntegerField()
    course_system_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_score_optional'


class TbScorePic(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    score_id = models.IntegerField()
    pic_name = models.CharField(max_length=20)
    pic_path = models.CharField(max_length=100)
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_score_pic'


class TbScoreSegment(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    score_id = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField(blank=True, null=True)
    type = models.IntegerField()
    label = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_score_segment'


class TbScoreTimbre(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    score_id = models.IntegerField()
    timbre_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_score_timbre'


class TbSectionAudioTeach(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    section_name = models.CharField(max_length=20)
    pic_name = models.CharField(max_length=200, blank=True, null=True)
    pic_path = models.CharField(max_length=200, blank=True, null=True)
    audio_name = models.CharField(max_length=200, blank=True, null=True)
    audio_path = models.CharField(max_length=255, blank=True, null=True)
    play_type = models.IntegerField()
    is_auto_play = models.IntegerField(blank=True, null=True)
    teach_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_section_audio_teach'


class TbSectionFullPlay(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    score_id = models.IntegerField()
    section_name = models.CharField(max_length=20)
    teach_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_section_full_play'


class TbSectionGame(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    level_id = models.IntegerField()
    section_name = models.CharField(max_length=20)
    type = models.IntegerField()
    teach_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_section_game'


class TbSectionHomework(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    section_name = models.CharField(max_length=20)
    teach_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_section_homework'


class TbSectionSegmentPlay(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    video_id = models.IntegerField()
    video_segment_id = models.IntegerField()
    score_id = models.IntegerField()
    score_segment_id = models.IntegerField()
    section_name = models.CharField(max_length=20)
    keyboard = models.CharField(max_length=3)
    teach_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_section_segment_play'


class TbSectionVideoTeach(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    video_id = models.IntegerField()
    video_segment_id = models.IntegerField(blank=True, null=True)
    section_name = models.CharField(max_length=20)
    poster_name = models.CharField(max_length=200, blank=True, null=True)
    poster_path = models.CharField(max_length=100, blank=True, null=True)
    play_type = models.IntegerField(blank=True, null=True)
    is_auto_play = models.IntegerField(blank=True, null=True)
    teach_status = models.IntegerField()
    b00_name = models.CharField(max_length=200, blank=True, null=True)
    b00_path = models.CharField(max_length=200, blank=True, null=True)
    b00_syx = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tb_section_video_teach'


class TbStudent(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    create_teacher_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    gender = models.IntegerField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.BigIntegerField()
    coin_num = models.IntegerField(blank=True, null=True)
    star_num = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    login_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_student'


class TbStudentClass(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField()
    class_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_student_class'


class TbStudentScoreHzq(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField()
    score_id = models.IntegerField()
    create_time = models.BigIntegerField()
    course_id = models.IntegerField()
    class_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_student_score_hzq'


class TbTeacher(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    institution_id = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    school_area = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    login_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_teacher'


class TbTeacherAppVersion(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    zip_name = models.CharField(max_length=100)
    zip_path = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True, null=True)
    version_type = models.IntegerField(blank=True, null=True)
    public_type = models.IntegerField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    create_time = models.BigIntegerField()
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_teacher_app_version'


class TbTeacherCourseSystem(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    teacher_id = models.CharField(max_length=255)
    course_system_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tb_teacher_course_system'


class TbTimbre(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tb_timbre'


class TbUnit(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    show_name = models.CharField(max_length=20)
    type = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_unit'


class TbUnitSection(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    unit_id = models.IntegerField()
    section_id = models.IntegerField()
    type = models.IntegerField()
    seq = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tb_unit_section'


class TbVideo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    video_path = models.CharField(max_length=100)
    thumb_path = models.CharField(max_length=100)
    name = models.CharField(max_length=20, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_video'


class TbVideoSegment(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    video_id = models.IntegerField()
    start = models.FloatField()
    end = models.FloatField()
    label = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_video_segment'
