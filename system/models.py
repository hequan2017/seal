from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User


class Users(AbstractUser):
    """
    基于django表  添加字段 , 如有需要调用user的情况,请使用此表
    """
    position = models.CharField(max_length=64, verbose_name='职位信息', blank=True, null=True)
    avatar = models.CharField(max_length=256, verbose_name='头像', blank=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

