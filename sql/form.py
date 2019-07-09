from django import forms
from sql.models import database
import re
import logging
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets

logger = logging.getLogger('create-form')


class DatabaseForm(forms.ModelForm):
    data_base = Ffields.CharField(
        label='数据库库名',
        widget=Fwidgets.Select(attrs={'class': 'select2',
                                      'data-placeholder': '----请选择库名----'}),
    )
    table = Ffields.CharField(
        label='数据库表名',
        widget=Fwidgets.Select(attrs={'class': 'select2',
                                      'data-placeholder': '----请选择库名----'}),
    )
    # ps = Ffields.CharField(
    #     label='提交说明',
    #     widget=Fwidgets.TextInput(
    #
    #     ),
    # )

    backup = Ffields.BooleanField(
        label='是否备份',
    )

    class Meta:
        model = database
        fields = ['region', 'name', 'data_base', 'table','backup']

        widgets = {
            'region': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '----请选择区域----'}
            ),
            'name': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '----请选择RDS----'}),
            'data_base': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '----请选择库名----'}),
            # 'table_name': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': '----请选择表名----'}),
            # 'InstanceType': forms.Select(attrs={'class': 'select2',
            #                                     'data-placeholder': '----请选择实例模板----'}),
            # 'ImageId': forms.Select(attrs={'class': 'select2',
            #                                     'data-placeholder': '----请选择镜像----'}),
            # 'Vpc': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': '----请选择Vpc----'}),
            # 'VSwitchId': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': '----请选择交换机----'}),
            # 'SecurityGroupId': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': '----请选择安全组----'},
            # ),
            # 'Size': forms.Select(attrs={'class': 'select2'}),
        }
        help_texts = {
            'region': '* 必填 ',
            'name': '* 必填 ',
            'data_base': '* 必填 ',
        }
