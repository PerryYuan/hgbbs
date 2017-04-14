# coding:utf8
import os

SECRET_KEY = os.urandom(24)

USERNAME = ''
PASSWORD = ''
HOST = ''
PORT = ''
DB_NAME = ''

DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (USERNAME,PASSWORD,HOST,PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = ''

MAIL_SERVER = ''
MAIL_PORT = ''
# MAIL_USE_TLS = 'True'
MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False



