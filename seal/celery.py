from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seal.settings')
# celery 5 移除了 celery.platforms，允许 root 运行改用环境变量
os.environ.setdefault('C_FORCE_ROOT', 'true')

app = Celery('seal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


##定时任务
app.conf.update(
    beat_schedule={
        'demo1': {
            'task': 'system.tasks.system_demo',
            'schedule': timedelta(seconds=10),
            'args': [111]
        },
        'demo2': {
            'task': 'system.tasks.system_demo',
            'schedule': crontab(minute=00, hour=00, day_of_month=1),
            'args': [222]
        },
    }
)
