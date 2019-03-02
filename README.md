# 海豹  
> django-base-templastes

> 因本项目开始时间为3月1日,是 世界海豹日,故项目起名为  海豹 seal 

> 主要为 django 基础开发平台, MVC 模式 开发.(非前后端分离) ,可以拿来直接开发 django项目。作者会在周末进行开发、更新。


## 版本
* v0.1

## 介绍
* 基于bootstrap4+django2.1+python3.7 
* 会尽量多加一些注释
* 采用cbv开发方式，提高开发效率

## DEMO
![列表](document/demo/1.jpg)
![添加](document/demo/2.jpg)


## static

>  inspinia 2.9 model   前端基础模板(实际线上可以删除掉本目录)

## templates

* base  网页基本模板
* system 平台基本网页(首页/登录/修改密码)
* assets  资产管理  (增删改查例子)

## 部署

```bash
git clone https://github.com/hequan2017/seal
cd seal
python install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


python manage.py  runserver 0.0.0.0:80


```

### 售后服务

* 有问题 可以加QQ群： 620176501  <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="django开发讨论群" title="django开发讨论群"></a>
* 欢迎提出你的需求和意见,或者来加入到本项目中一起开发。

## 作者
* 何全 

