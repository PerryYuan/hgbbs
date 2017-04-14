# coding:utf8
from functools import wraps
import constants
import flask
from models.frontmodels import FrontUser

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(flask.g,'front_user'):
            if not flask.g.front_user.is_active:
                flask.abort(405)
            return func(*args,**kwargs)
        else:
            flask.abort(401)
    return wrapper