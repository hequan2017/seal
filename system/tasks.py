import logging
import requests
import json
from celery import shared_task
from system.models import Users
from seal import settings
logger = logging.getLogger('system_celery')


@shared_task
def system_demo(one):
    ##因为开启了时区,所以django在数据库里面保存的为 utc 时间, 调用的时候会帮你 转为 东八区, celery会自动识别时间
    from django.utils import timezone
    for i in Users.objects.all():
        print(i.last_login)  ## 直接读取时间,会是 utc时间,未转换,如果需要处理 请注意
        print(timezone.localtime(i.last_login).strftime("%Y-%m-%d %H:%M:%S"))  ## 时间格式化为 正常时间
    print("celery定时任务demo 每分钟执行一遍",one)
    return


@shared_task
def ding_ding_to_info(content,type=None):
    """
    钉钉接口   异步调用     ding_ding_to_info.delay("报警1")
    :param content:  文本内容
    :param type:
    :return:
    """
    web_hook_url = getattr(settings, 'web_hook_url'),
    headers = {'content-type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [
            ],
        }
    }
    try:
        r = requests.post(web_hook_url[0], data=json.dumps(data), headers=headers)
        print(r.text)
    except Exception as e:
        logger.error(e)