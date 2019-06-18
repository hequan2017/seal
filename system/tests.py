from django.test import TestCase

# Create your tests here.
from datetime import timedelta, datetime

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'jifeng.si',
    'depends_on_past': False,
    # 'depends_on_past': True,
    #'start_date': airflow.utils.dates.days_ago(2),
    'start_date': datetime(2018, 5, 2),
    'email': ['1219957063@qq.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_hello_world_dag',
    default_args=default_args,
    description='my first DAG',
    schedule_interval='*/25 * * * *',
    start_date=datetime(2018, 5, 28)
)

dummy_operator = DummyOperator(task_id='dummy_task', dag=dag)

hello_operator = BashOperator(
    task_id='sleep_task',
    depends_on_past=False,
    bash_command='echo `date` >> /home/py/test.txt',
    dag=dag
)

dummy_operator >> hello_operator