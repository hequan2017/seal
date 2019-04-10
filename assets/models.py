from django.db import models


class Ecs(models.Model):
    TYPE_CHOICES = (
        ('阿里云', '阿里云'),
        ('腾讯云', '腾讯云'),
        ('华为云', '华为云'),
        ('亚马逊', '亚马逊'),
        ('其他', '其他'),
        (None,None),
    )
    hostname = models.CharField(max_length=96, verbose_name='主机名', blank=True, null=True, )
    type = models.CharField(choices=TYPE_CHOICES, max_length=16, verbose_name='主机类型', blank=True, null=True, )
    instance_id = models.CharField(max_length=64, verbose_name='实例ID', unique=True)
    instance_name = models.CharField(max_length=96, verbose_name='标签', blank=True, null=True, )
    os_name = models.CharField(max_length=64, verbose_name='系统版本', blank=True, null=True, )
    cpu = models.IntegerField(verbose_name='CPU', blank=True, null=True)
    memory = models.IntegerField(verbose_name='内存', blank=True, null=True)
    private_ip = models.GenericIPAddressField(verbose_name='内网IP', blank=True, null=True)
    public_ip = models.GenericIPAddressField(verbose_name='外网IP', blank=True, null=True)

    c_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', blank=True)
    u_time = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间', blank=True)

    class Meta:
        db_table = "ecs"
        verbose_name = "主机"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname
