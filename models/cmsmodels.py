# coding:utf8
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Permission(object):
    SuperPermission = 255
    GeneralPermission = 1

    Permission_Map = {
        SuperPermission:(u'超级管理员',u'拥有至高无上的权利'),
        GeneralPermission:(u'普通管理员',u'拥有管理前端用户的权利')
    }

cms_user_role = db.Table('cms_user_role',
                         db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
                         db.Column('user_id', db.Integer,db.ForeignKey('cms_user.id'),primary_key=True))

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    permission = db.Column(db.Integer,nullable=False,default=Permission.GeneralPermission)
    desc = db.Column(db.String(100),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)
    is_active = db.Column(db.Boolean,default=True)
    roles = db.relationship('CMSRole',secondary=cms_user_role,backref='users')

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,pwd):
        self._password = generate_password_hash(pwd)

    def check_pwd(self,pwd):
        return check_password_hash(self.password,pwd)

    @property
    def is_superrole(self):
        return self.has_permission(Permission.SuperPermission)

    def has_permission(self,permission):
        if not self.roles:
            return False
        all_permission = 0
        for role in self.roles:
            all_permission |= role.permission
        return all_permission & permission == permission

    @property
    def permission(self):
        if not self.roles:
            return None
        all_permission = 0
        for role in self.roles:
            all_permission |= role.permission
        permissions = []
        for key,value in Permission.Permission_Map.iteritems():
            if all_permission & key == key:
                permissions.append({key:value})
        return permissions


