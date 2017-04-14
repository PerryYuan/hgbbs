# coding:utf8

from exts import mail
from flask_mail import Message

def send_mail(subject,recipients,body=None,html=None):
    if not recipients:
        return False
    if not subject:
        return False
    if not body and not html:
        return False
    if isinstance(recipients,str) or isinstance(recipients,unicode):
        recipients = [recipients]
    message = Message(subject,recipients=recipients,body=body,html=html)
    try:
        mail.send(message)
        return True
    except:
        return False
