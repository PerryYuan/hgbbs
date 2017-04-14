# coding:utf8
from flask import session
import constants
import flask
from models.cmsmodels import CMSUser,Permission
from functools import wraps
from utils import xtjson

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user_id = session.get(constants.CMS_LOGIN_SESSION_ID)
        user = CMSUser.query.filter(CMSUser.id == user_id).first()
        if user:
            if not user.is_active:
                return flask.abort(401)
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))
    return wrapper

def permission_required(permission):
    def deco(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return flask.abort(401)

        return wrapper
    return deco

def is_super_required(func):
    return permission_required(Permission.SuperPermission)(func)
