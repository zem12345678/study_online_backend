from django.db import models


class CzLearningCourse(models.Model):
    """

    """
    course_id = models.IntegerField(verbose_name='课程id')
    user_id = models.IntegerField(verbose_name='用户id')
    charge = models.CharField(verbose_name='收费规则', max_length=32, null=True)
    price = models.FloatField(verbose_name='课程价格', null=True)
    valid = models.CharField(verbose_name='收费规则', max_length=32, null=True)
    start_time = models.DateTimeField(verbose_name='开始时间', null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True)
    status = models.CharField(verbose_name='选课状态', max_length=32, null=True)

    class Meta:
        db_table = 'cz_learning_course'
