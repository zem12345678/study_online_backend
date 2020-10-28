from django.db import models
from common import sys_dict


class Category(models.Model):
    """
    课程分类
    """
    name = models.CharField(max_length=32, verbose_name='分类名称')
    label = models.CharField(max_length=32, blank=True, null=True, verbose_name='分类标签')
    parentid = models.ForeignKey("self", db_column='parentid', null=True, blank=True, verbose_name="父结点ID",
                                 related_name="children", on_delete=models.deletion.CASCADE)
    isshow = models.NullBooleanField(blank=True, null=True, verbose_name='是否显示')
    orderby = models.IntegerField(blank=True, null=True, verbose_name='排序字段')
    isleaf = models.NullBooleanField(blank=True, null=True, verbose_name='是否叶子')

    class Meta:
        managed = True
        db_table = 'category'


class CourseBase(models.Model):
    """
    课程基础信息
    """
    name = models.CharField(max_length=32, verbose_name='课程名称')
    subtitle = models.CharField(max_length=200, null=True, verbose_name='课程子标题')
    users = models.CharField(max_length=500, blank=True, null=True, verbose_name='适用人群')
    target = models.CharField(max_length=500, blank=True, null=True, verbose_name='教学目标')
    mt = models.IntegerField(verbose_name='课程大分类')
    grade = models.CharField(max_length=32, verbose_name='课程等级')
    serialize = models.CharField(max_length=32, null=True, verbose_name='课程连载状态')
    studymodel = models.CharField(max_length=32, verbose_name='学习模式')
    teachmode = models.CharField(max_length=32, blank=True, null=True, verbose_name='授课模式')
    description = models.TextField(blank=True, null=True, verbose_name='课程介绍')
    st = models.IntegerField(verbose_name='课程小分类')
    status = models.CharField(max_length=32, blank=True, null=True, default=sys_dict.COURSE_STATUS_MAKING, verbose_name='课程状态')
    study_num = models.IntegerField(null=True, verbose_name='学习人数')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    is_deleted = models.NullBooleanField(default=False, verbose_name='是否显示')

    class Meta:
        managed = True
        db_table = 'course_base'


class CourseMarket(models.Model):
    """
    课程营销信息
    """
    charge = models.CharField(max_length=32, verbose_name='收费规则')
    valid = models.CharField(max_length=32, verbose_name='有效性')
    expires = models.DateTimeField(blank=True, null=True, verbose_name='过期时间')
    qq = models.CharField(max_length=32, blank=True, null=True, verbose_name='咨询QQ')
    price = models.FloatField(blank=True, null=True, verbose_name='价格')
    price_old = models.FloatField(blank=True, null=True, verbose_name='原价')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='课程有效期-开始时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='课程有效期-结束时间')

    class Meta:
        managed = True
        db_table = 'course_market'


class CoursePic(models.Model):
    """
    课程图片信息
    """
    courseid = models.IntegerField(primary_key=True, verbose_name='课程ID')
    pic = models.CharField(max_length=256, verbose_name='图片路径')

    class Meta:
        managed = True
        db_table = 'course_pic'

    @classmethod
    def find_by_course_id(cls, course_id):
        return cls.objects.filter(courseid=course_id).first()


class CoursePub(models.Model):
    """
    课程发布
    """
    name = models.CharField(max_length=32,verbose_name='课程名称')
    users = models.CharField(max_length=500, verbose_name='适用人群')
    mt = models.IntegerField(verbose_name='课程大分类')
    st = models.IntegerField(verbose_name='课程小分类')
    grade = models.CharField(max_length=32, verbose_name='课程等级')
    studymodel = models.CharField(max_length=32, verbose_name='学习模式')
    teachmode = models.CharField(max_length=32, blank=True, null=True, verbose_name='授课模式')
    description = models.TextField(verbose_name='课程介绍')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='时间戳logstash使用')
    charge = models.CharField(max_length=32, verbose_name='收费规则')
    valid = models.CharField(max_length=32, verbose_name='有效性')
    qq = models.CharField(max_length=32, blank=True, null=True, verbose_name='咨询QQ')
    price = models.FloatField(blank=True, null=True, verbose_name='价格')
    price_old = models.FloatField(blank=True, null=True, verbose_name='原价')
    expires = models.CharField(max_length=32, blank=True, null=True, verbose_name='过期时间')
    start_time = models.CharField(max_length=32, blank=True, null=True, verbose_name='课程有效期-开始时间')
    end_time = models.CharField(max_length=32, blank=True, null=True, verbose_name='课程有效期-结束时间')
    pic = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片路径')
    teachplan = models.TextField(verbose_name='课程计划')
    pub_time = models.CharField(max_length=32, blank=True, null=True, verbose_name='课程发布时间')

    class Meta:
        managed = True
        db_table = 'course_pub'


class Teachplan(models.Model):
    """
    课程计划
    """
    pname = models.CharField(max_length=64, verbose_name='计划名称')
    parentid = models.ForeignKey("self", db_column='parentid', null=True, blank=True, verbose_name="父计划ID",
                                 related_name="children", on_delete=models.deletion.CASCADE)
    grade = models.CharField(max_length=1, default='1', verbose_name='层级')
    ptype = models.CharField(max_length=1, blank=True, null=True, verbose_name='课程类型')
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name='章节及课时介绍')
    timelength = models.FloatField(blank=True, null=True, verbose_name='时长')
    courseid = models.IntegerField(verbose_name='课程ID')
    orderby = models.CharField(max_length=32, blank=True, null=True, verbose_name='排序字段')
    status = models.CharField(max_length=1, verbose_name='状态')
    trylearn = models.NullBooleanField(blank=True, null=True, verbose_name='是否试学')

    class Meta:
        managed = True
        db_table = 'teachplan'


class TeachplanMedia(models.Model):
    """
    课程计划媒体文件
    """
    teachplan_id = models.CharField(primary_key=True, max_length=32, verbose_name='课程计划ID')
    media_id = models.CharField(max_length=32, verbose_name='媒资文件ID')
    media_fileoriginalname = models.CharField(max_length=128, verbose_name='媒资文件的原始名称')
    media_url = models.CharField(max_length=256, verbose_name='媒资文件访问地址')
    courseid = models.IntegerField(verbose_name='课程ID')

    class Meta:
        managed = True
        db_table = 'teachplan_media'


class TeachplanMediaPub(models.Model):
    """
    课程计划媒体文件发布
    """
    teachplan_id = models.CharField(primary_key=True, max_length=32, verbose_name='课程计划ID')
    media_id = models.CharField(max_length=32, verbose_name='媒资文件ID')
    media_fileoriginalname = models.CharField(max_length=128, verbose_name='媒资文件的原始名称')
    media_url = models.CharField(max_length=256, verbose_name='媒资文件访问地址')
    courseid = models.IntegerField(verbose_name='课程ID')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='时间戳，供Logstash使用')

    class Meta:
        managed = True
        db_table = 'teachplan_media_pub'
