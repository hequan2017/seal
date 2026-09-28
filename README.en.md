[简体中文](README.md) | [English](README.en.md)

# Seal (海豹)

> django-base-templates — a Django development DEMO platform, supporting both non-separated (server-rendered) and separated (front-end / back-end) modes

![Version](https://img.shields.io/badge/release-0.3-blue.svg)
![Language](https://img.shields.io/badge/language-python3.6-blue.svg)
![Env](https://img.shields.io/badge/env-django2.2-red.svg)
![Bootstrap3](https://img.shields.io/badge/model-bootstrap3-mauve.svg)
![RESTful](https://img.shields.io/badge/api-RESTful-blue.svg)
![GraphQL](https://img.shields.io/badge/api-GraphQL-blue.svg)

> The project started on March 1st, which is International Seal Day, hence the name "Seal" (海豹).

## Introduction

Seal is a Django base development platform template built with the MVC pattern. It supports both **non-separated** development (Django template rendering) and **separated** development (RESTful / GraphQL APIs), so you can use it as a reference when building your own Django projects.

It is based on Django 2.2 + Python 3.6 + Celery 4 for async tasks, uses the Inspinia 2.7 front-end template (Bootstrap3), and is developed entirely with CBVs (Class-Based Views). It also ships with DRF RESTful API examples, GraphQL examples, Kubernetes management, and SQL audit/execution modules as real-world references.

Beyond being a base template, the project includes two complete ops-oriented implementations: a **K8s web console** (Node / Service / Pod lists + Pod WebSSH, executing commands via the Kubernetes API) and a **SQL audit & execution engine** (goInception / soar).

The author develops and updates this project on weekends.

## ✨ Features

- **Base development templates**: `base` web layout template + `system` platform pages (home / login / password change), front-end template Inspinia 2.7 (Bootstrap3)
- **Asset management example**: the `assets` app provides a complete CRUD (CBV) example to reference when developing your own modules
- **RESTful API**: DRF-based API examples with Token authentication (`/api/token`), plus two built-in API docs endpoints (`/api/docs/` and Swagger-style `/api/docs2/`)
- **GraphQL**: graphene-django Query / Mutation examples (user list, single query, create/update/delete) with a built-in GraphiQL playground (`/graphql/`)
- **Kubernetes management**: Node / Service / Pod lists and Pod details, plus **Pod WebSSH** (django-channels + WebSocket, executing commands inside Pods via the Kubernetes API)
- **SQL audit & execution**: goInception for SQL checking / execution (with backup support) and soar for SQL optimization advice; supports multiple database environments
- **Two async task options**: Celery (recommended for scheduled tasks, with django-celery-beat / django-celery-results / flower) and dramatiq (ordinary async tasks)
- **Permission control**: login authentication + Django Permission-based page-level checks; the Django admin is prettified with django-simpleui

## Roadmap

* Phase 1: base templates (done)
* Phase 2: Kubernetes management platform (in progress)
    * node/service/pod lists (done)
    * pod webssh (done, executing commands via the Kubernetes API)
* Phase 3: MySQL SQL statement audit (done)
    * SQL check and execution
* Phase 4: in progress — rebuilding the front end <https://github.com/hequan2017/seal-d2-admin>

## 🛠 Tech Stack

**Backend**

- Python 3.6 / Django 2.2.4 (CBV style)
- Django REST framework 3.9.2 + django-rest-swagger (API and docs)
- graphene-django 2.2.0 (GraphQL)
- celery 4.1.1 + django-celery-beat + django-celery-results + flower; dramatiq 1.5.0 (async tasks)
- django-channels 2.2.0 + channels-redis (WebSocket channel for Pod WebSSH)
- kubernetes 9.0.0 (official Kubernetes Python client), PyMySQL / mysqlclient, paramiko, psutil

**Front-end**

- Bootstrap3 + Inspinia 2.7 template (non-separated mode)
- Vue-based front ends: <https://github.com/hequan2017/seal-vue> and <https://github.com/hequan2017/seal-d2-admin>

**Storage & services**

- MySQL 5.7 / SQLite
- Redis (broker and backend for celery / dramatiq / channels)

**SQL audit tools**

- goInception / soar (executables are bundled in the repo under `sql/bin/`)

## 🚀 Quick Start

Requirements: Python 3.6, MySQL 5.7 (or SQLite), Redis.

```bash
yum install python-devel mysql-devel python36-devel.x86_64 -y

git clone https://github.com/hequan2017/seal
cd seal

## Django 2.2 does not support older versions of SQLite. If you want to use
## SQLite for storage, please upgrade it following this blog post:
## https://www.jianshu.com/p/cdacf4b74646

python36 -m pip install -r requirements.txt
python36 manage.py makemigrations
python36 manage.py migrate
python36 manage.py createsuperuser

python36 manage.py runserver 0.0.0.0:8001

// Run in the background
// nohup python36 manage.py runserver 0.0.0.0:8001 >> /tmp/http.log 2>&1 &
```

### K8s Module

Edit the K8s settings in `seal/settings.py` (see `k8s/k8sApi/获取k8s admin token的方法.md` for how to get the admin token):

```python
## K8S
Token = "<dashboard-admin-token>"
APISERVER = 'https://192.168.100.111:6443'
```

### SQL Module

Enter the project directory `cd seal`. The backup server can be configured in `sql/bin/config/config.toml`; for details, search for goInception on GitHub:

```bash
chmod +x sql/bin/soar
chmod +x sql/bin/goInception

./sql/bin/goInception -config=sql/bin/config/config.toml
```

### Async Tasks

* Async option 1: Celery is recommended for scheduled tasks

```bash
cd seal
celery -B -A seal worker -l info
```

* Async option 2: dramatiq for ordinary async tasks

```bash
cd system/decorator/asynchronous/
dramatiq asynchronous --watch . --log-file /tmp/dramatiq.log
```

### Notes

* If you plan to use this in production, regenerate the SECRET_KEY in the settings file.
* Timezone: timezone support is enabled, so Django stores UTC times in the database and converts them to UTC+8 when you read them through the timezone API; Celery recognizes the timezone automatically.

```python
from django.utils import timezone
for i in Users.objects.all():
    print(i.last_login)  ## Reading the field directly returns a UTC time; handle it carefully if needed
    print(timezone.localtime(i.last_login).strftime("%Y-%m-%d %H:%M:%S"))  ## Format into local time

## 2019-03-05 06:41:18.040809+00:00
## 2019-03-05 14:41:18
```

## 📁 Directory Structure

```
seal/
├── assets/      # Asset management (CRUD example)
├── k8s/         # Kubernetes management (node/service/pod lists, pod detail, webssh)
├── sql/         # SQL audit & execution (goInception / soar; executables in bin/)
├── system/      # System module (login / users / password / async task examples)
├── document/    # Demo screenshots, SQL notes, coding standards
├── templates/   # Page templates (base/system/assets/k8s/sql)
├── static/      # Static assets (inspinia, ace, echarts, ueditor, etc.)
└── seal/        # Project configuration (settings / urls / schema / routing / celery)
```

## 📸 DEMO / Screenshots

> Demo: <http://129.28.156.219:8001>

> Account: admin　Password: 1qaz.2wsx

> API docs: <http://129.28.156.219:8001/api/docs/>

![List](document/demo/1.jpg)
![Create](document/demo/2.jpg)
![API](document/demo/3.jpg)
![API](document/demo/4.jpg)
![API](document/demo/5.jpg)
![K8S](document/demo/6.jpg)
![K8S](document/demo/7.jpg)
![SQL](document/demo/8.jpg)

## 🔗 Related Projects

* **seal-vue**: Vue-based front end (in active development): <https://github.com/hequan2017/seal-vue>
* **seal-d2-admin**: Phase 4 front-end rebuild (D2Admin): <https://github.com/hequan2017/seal-d2-admin>

## GraphQL Examples

See `seal/schema.py` for the code. Endpoint: <http://localhost/graphql>

GraphQL request examples:

```
query{
  users{
    id,
    username,
    email
  }
}

query{
  singleUser(pk: 1){
    username,
    email
  }
}

mutation createUser {
 createUser (username: "test1") {
     info {
         id,
     },
     ok
 }
}

mutation updateUser {
 updateUser (pk:2,username: "test2") {
     info {
         id,
     },
     ok
 }
}

mutation deleteUser {
 deleteUser (pk:2) {
     ok
 }
}
```

## 📄 License

[MIT](LICENSE) © 2019 He Quan (何全)

## Support / Resources

* CBV documentation: <http://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/>
* GraphQL reference (Chinese): <https://passwo.gitbook.io/graphql/index/drf>

### Community

* For questions, join the QQ group: 620176501 <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="django开发讨论群" title="django开发讨论群"></a>
* Feature requests, feedback, and contributions are welcome.

### Author

* 何全 (He Quan)
