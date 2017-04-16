# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import config

app = Flask('hgbbs')
app.config.from_object(config)

db = SQLAlchemy(app)
mail = Mail(app)