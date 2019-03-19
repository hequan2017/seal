# 海豹  
![版本](https://img.shields.io/badge/release-0.1-blue.svg)
![语言](https://img.shields.io/badge/language-python3.6-blue.svg)
![语言](https://img.shields.io/badge/env-django2.1-red.svg)
![bootstrap4](https://img.shields.io/badge/model-bootstrap4-mauve.svg)
> django-base-templastes

> 因本项目开始时间为3月1日,是 国际海豹日,故项目起名为  海豹 seal 

> 主要为 django 基础开发平台, MVC 模式 开发.(非前后端分离) ,可以拿来直接开发 django项目。作者会在周末进行开发、更新。


## 介绍
* 基于bootstrap4+django2.1+python3.6+celery异步任务
* 前端模板 inspinia 2.9 
* 会尽量多加一些注释
* 采用cbv开发方式，提高开发效率
* python3.7 兼容性未做测试


## DEMO
![列表](document/demo/1.jpg)
![添加](document/demo/2.jpg)


## templates

* base      网页基本模板
* system    平台基本网页(首页/登录/修改密码)
* assets    资产管理  (增删改查例子)
* document  代码规范



## 部署

```bash
yum install  python-devel mysql-devel  -y

git clone https://github.com/hequan2017/seal
cd seal
python install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


python manage.py  runserver 0.0.0.0:80

```
* 扩展功能-异步1   推荐 定时任务用celery
```bash
#需要安装redis
#启动celery异步任务
cd seal
celery  -B   -A  seal  worker  -l  info
```

* 扩展功能-异步2   普通异步任务 用  dramatiq
```bash
cd system/decorator/asynchronous/
dramatiq  asynchronous  --watch  .  --log-file  /tmp/dramatiq.log

```


##  注意
* 如果想直接拿来做生产项目,请重新生成一个 settings 文件里面的 SECRET_KEY 
* 时区问题
```python
##因为开启了时区,所以django在数据库里面保存的为 utc 时间, 调用的时候会帮你 转为 东八区, celery会自动识别时间
from django.utils import timezone
for i in Users.objects.all():
    print(i.last_login)  ## 直接读取时间,会是 utc时间,未转换, 如果需要处理 请注意
    print(timezone.localtime(i.last_login).strftime("%Y-%m-%d %H:%M:%S"))  ## 时间格式化为 正常时间
    
## 2019-03-05 06:41:18.040809+00:00
## 2019-03-05 14:41:18

```


### 售后服务

* 有问题 可以加QQ群： 620176501  <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="django开发讨论群" title="django开发讨论群"></a>
* 欢迎提出你的需求和意见,或者来加入到本项目中一起开发。
* inspinia 2.9 model   前端基础模板,可以加群,在群共享里面有。
* bootstrap4 中文文档  https://code.z01.com/v4/
* cbv 中文文档  http://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/
 

## 作者
* 何全 

