# coding:utf8
from exts import db
from datetime import datetime
from shortuuid import uuid
from werkzeug.security import check_password_hash,generate_password_hash
class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET = 3

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=uuid())
    telephone = db.Column(db.String(11), nullable=False,unique=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime)
    old_login_time = db.Column(db.DateTime)
    qq = db.Column(db.String(20))
    realname = db.Column(db.String(20))
    avatar = db.Column(db.String(100))
    gender = db.Column(db.Integer, default=GenderType.SECRET)
    signature = db.Column(db.String(100)) #个性签名
    points = db.Column(db.Integer, default=0) #论坛积分

    def __init__(self,telephone,username,password):
        self.telephone = telephone
        self.password = password
        self.username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_pwd(self,newpwd):
        return check_password_hash(self.password,newpwd)