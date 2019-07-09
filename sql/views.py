import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, View, CreateView, UpdateView, DetailView
from django.shortcuts import render, HttpResponse
from sql.form import DatabaseForm
from sql.models import database
import json
from django.db.models import Q
import subprocess
from sql.handle import con_database
import pymysql
import prettytable as pt
tb = pt.PrettyTable()
logger = logging.getLogger('sql')


class SqlDdl(LoginRequiredMixin, CreateView):
    model = database
    form_class = DatabaseForm
    template_name = 'sql/sql-ddl.html'


class SqlDdlQuery(LoginRequiredMixin, View):
    model = database

    def get(self, request, pk):
        region = request.GET.get("region")
        name = request.GET.get("name")
        data_base = request.GET.get("data_base")
        table = request.GET.get("table")
        ret = {"data": []}
        if pk == "name":
            obj = database.objects.filter(region=region)
            for i in obj:
                ret['data'].append(i.name)

        elif pk == "databases":
            obj = database.objects.get(name=name)
            try:
                with con_database.SQLgo(
                        ip=obj.address,
                        user=obj.username,
                        password=obj.get_password(),
                        port=obj.port
                ) as f:
                    ret['data'] = f.baseItems(sql='show databases')
            except Exception as e:
                print(e)
        elif pk == "tables":
            obj = database.objects.get(name=name)
            try:
                with con_database.SQLgo(
                        ip=obj.address,
                        user=obj.username,
                        password=obj.get_password(),
                        port=obj.port,
                        db=data_base
                ) as f:
                    ret['data'] = f.baseItems(sql='show tables')
            except Exception as e:
                print(e)
        elif pk == "structure":
            obj = database.objects.get(name=name)
            try:
                with con_database.SQLgo(
                        ip=obj.address,
                        user=obj.username,
                        password=obj.get_password(),
                        port=obj.port,
                        db=data_base
                ) as f:
                    field = f.gen_alter(table_name=table)  # 表结构详情
                    idx = f.index(table_name=table)  # 索引

                    ret['data'] = {'idx': idx, 'field': field}
            except Exception as e:
                print(e)
        else:
            pass
        print(ret)
        return HttpResponse(json.dumps(ret))

    def post(self, request, pk):
        ret = {"data": []}
        name = request.GET.get("name")
        backup = request.GET.get("backup")
        # 语法检查
        if pk == "advice":
            sql = request.POST.get("sql")
            sql = sql.replace("\"", "'")

            sql_cmd = f'echo "{sql}" | ./sql/bin/soar '
            print(sql_cmd)
            cmd = subprocess.Popen(sql_cmd, shell=True, stdout=subprocess.PIPE)
            cmd = cmd.communicate()
            cmd = cmd[0].decode().rstrip()
            ret['data'] = cmd
        # SQL检测
        elif pk == "sql_test":
            sql_post = request.POST.get("sql")
            sql_post = sql_post.replace("\"", "'")
            obj = database.objects.get(name=name)
            sql = f'''/*--user={obj.username};--password={obj.get_password()};--host={obj.address};--check=1;--port={obj.port};--execute=0;--backup={backup};*/
            inception_magic_start;
            {sql_post}
            inception_magic_commit;'''

            conn = pymysql.connect(host='127.0.0.1', user='', passwd='',
                                   db='', port=4000, charset="utf8mb4")
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()

            tb.field_names = [i[0] for i in cur.description]
            for row in result:
                tb.add_row(row)
            print(tb)

            for i in result:
                ret['data'].append({
                    "order_id":i[0],
                    "stage": i[1],
                    "error_level": i[2],
                    "stage_status": i[3],
                    "error_message": i[4],
                    "sql": i[5],
                    "affected_rows": i[6],
                })
            ret['error'] = 0
            for j in ret['data']:
                if j['error_level'] != 0:
                    ret['error'] = 1

        # sql执行
        elif pk == "sql_exe":
            sql_post = request.POST.get("sql")
            sql_post = sql_post.replace("\"", "'")
            obj = database.objects.get(name=name)
            # 先检查
            sql1 = f'''/*--user={obj.username};--password={obj.get_password()};--host={obj.address};--check=1;--port={obj.port};--execute=0;--backup={backup};*/
                  inception_magic_start;
                  {sql_post}
                  inception_magic_commit;'''
            conn = pymysql.connect(host='127.0.0.1', user='', passwd='',
                                   db='', port=4000, charset="utf8mb4")
            cur = conn.cursor()
            cur.execute(sql1)
            result = cur.fetchall()
            cur.close()
            conn.close()

            tb.field_names = [i[0] for i in cur.description]
            for row in result:
                tb.add_row(row)
            print(tb)

            for i in result:
                ret['data'].append({
                    "order_id": i[0],
                    "stage": i[1],
                    "error_level": i[2],
                    "stage_status": i[3],
                    "error_message": i[4],
                    "sql": i[5],
                    "affected_rows": i[6],
                })

            for j in ret['data']:
                if j['error_level'] != 0:
                    ret['error'] = "检查未通过，禁止执行"
                    return HttpResponse(json.dumps(ret))
            # 检查通过 执行
            sql2 = f'''/*--user={obj.username};--password={obj.get_password()};--host={obj.address};--check=0;--port={obj.port};--execute=1;--backup={backup};*/
                              inception_magic_start;
                              {sql_post}
                              inception_magic_commit;'''

            conn = pymysql.connect(host='127.0.0.1', user='', passwd='',
                                   db='', port=4000, charset="utf8mb4")
            cur = conn.cursor()
            cur.execute(sql2)
            result = cur.fetchall()
            cur.close()
            conn.close()

            tb.field_names = [i[0] for i in cur.description]
            for row in result:
                tb.add_row(row)
            print(tb)
            ret = {"data": []}
            for i in result:
                ret['data'].append({
                    "order_id":i[0],
                    "stage": i[1],
                    "error_level": i[2],
                    "stage_status": i[3],
                    "error_message": i[4],
                    "sql": i[5],
                    "affected_rows": i[6],
                })
        else:
            pass
        print(ret)
        return HttpResponse(json.dumps(ret))
