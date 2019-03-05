from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from datetime import timedelta
from celery import Celery, platforms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seal.settings')

app = Celery('seal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


##定时任务
app.conf.update(
    CELERYBEAT_SCHEDULE={
        'demo1': {
            'task': 'system.tasks.system_demo',
            'schedule': timedelta(seconds=10),
            'args': [111]
        },
        'demo2': {
            'task': 'system.tasks.system_demo',
            'schedule': crontab(minute=00, hour=00,day_of_month=1),
            'args': [222]
        },
    }
)
