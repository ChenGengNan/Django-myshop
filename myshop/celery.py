from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# Celery 是一个分发队列，它可以处理大量的信息。它既可以执行实时操作也支持任务调度。
#使用 Celery 不仅可以让你很轻松的创建异步任务还可以让这些任务尽快执行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#app.autodiscover_tasks()