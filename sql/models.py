from django.db import models
import re
from cryptography.fernet import Fernet
from system.models import Users
from assets.models import Ecs


# import base64
# import os
# print(base64.urlsafe_b64encode(os.urandom(32)))

cipher_key = 'isSxtA8i5slddH9PrYEu8V5jzTeKCO5vwlu5pUT3eEc='


class database(models.Model):

    region = models.CharField(max_length=16, verbose_name='机房',choices=Ecs.TYPE_CHOICES)
    name = models.CharField(max_length=64, verbose_name='RDS名称',unique=True)
    address = models.CharField(max_length=64, verbose_name='地址', )
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=128, verbose_name='用户名', blank=True, null=True, )
    password = models.CharField(max_length=128, verbose_name='密码', blank=True, null=True, )

    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    def get_password(self):
        if self.password is not None and re.search("gAAAAA", self.password, ) != None:
            f = Fernet(cipher_key)
            p1 = self.password.encode()
            token = f.decrypt(p1)
            p2 = token.decode()
            return p2
        return None

    def save(self, *args, **kwargs):
        if self.password is not None and re.search("gAAAAA", self.password, ) == None:
            f = Fernet(cipher_key)
            p1 = self.password.encode()
            token = f.encrypt(p1)
            p2 = token.decode()
            self.password = p2
        super().save(*args, **kwargs)

    class Meta:
        db_table = "database"
        verbose_name = "数据库"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





