from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class CzUser(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    name = models.CharField(verbose_name="姓名", max_length=30, null=True, blank=True)
    birthday = models.DateField(verbose_name="出生年月", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=6, choices=GENDER_CHOICES, default="female")
    phone = models.CharField(verbose_name="电话", max_length=11, null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱", max_length=100, null=True, blank=True)
    userpic = models.CharField(verbose_name="用户头像", max_length=255, blank=True, null=True)
    qq = models.CharField(verbose_name="qq号码", max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(verbose_name="验证码", max_length=10)
    phone = models.CharField(verbose_name="电话", max_length=11)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
