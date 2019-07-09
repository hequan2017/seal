# !/usr/bin/env python
# -*- coding: utf-8 -*-

import django

import sys

import logging

import os

sys.path.append('/opt/argus')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'argus.settings')
django.setup()
logger = logging.getLogger('api')


def sql_data_perm():
    from sql.models import sqluser

    data = []
    for i in sqluser.objects.all():

        for j in i.perm.all():
            data.append({
                'ddl': j.ddl,
                'dml': j.dml,
                'select': j.select,
                "approver": [x.username for x in j.approver.all()],
                'ddl_data': [x.name for x in j.ddl_data.all()],
                'dml_data': [x.name for x in j.dml_data.all()],
                'select_data': [x.name for x in j.select_data.all()]
            })
    data2 = {
        "ddl": False,
        'dml': False,
        "select": False,
        "approver": [],
        "ddl_data": [],
        "dml_data": [],
        "select_data": [],
    }
    for i in data:
        for z in ["ddl", 'dml', 'select']:
            if i[z]:
                data2[z] = True
        for j in ['approver', 'ddl_data', 'dml_data', 'select_data']:
            for x in i[j]:
                data2[j].append(x)

    for i in ['approver', 'ddl_data', 'dml_data', 'select_data']:
        data2[i] = list(set(data2[i]))
    return data2



