# coding:utf8

from celery import Celery

from utils import mailutils
from exts import app
from utils.sendsmsutil import send_sms


def make_celery(app):
    celery = Celery(app.import_name,backend='redis://123.207.85.226:6379/0',broker='redis://123.207.85.226:6379/0')
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def celery_send_mail(subject, recipients, body=None, html=None):
    with app.app_context():
        return mailutils.send_mail(subject, recipients, body, html)

@celery.task
def celery_send_sms(captcha,telephone):
    with app.app_context():
        return send_sms(captcha,telephone)