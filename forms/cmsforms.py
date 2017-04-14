# coding:utf8

from base_form import BaseForm
from wtforms import StringField,BooleanField,ValidationError,IntegerField
from wtforms.validators import InputRequired,Email,Length,EqualTo
from utils import xtcache
from models.cmsmodels import CMSUser
from models.commonmodels import Board

class CMSLoginForm(BaseForm):
    email = StringField(validators=[InputRequired(u'邮箱不能为空！'),Email(u'邮箱格式不正确！')])
    password = StringField(validators=[InputRequired(u'密码不能为空！'),Length(6,20,message=u'密码格式不正确')])
    remember = BooleanField()

class CMSReSetPWD(BaseForm):
    oldpwd = StringField(validators=[InputRequired(u'原密码不能为空！')])
    newpwd = StringField(validators=[InputRequired(u'新密码不能为空！'),Length(6,20,message=u'新密码格式不正确！')])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd',message=u'两次密码不一致！')])

class CMSReSetMail(BaseForm):
    mail = StringField(validators=[InputRequired(u'新邮箱不能为空。'),Email(u'邮格式不正确。')])
    captcha = StringField(validators=[InputRequired(u'验证码不能为空。'),Length(4,4,message=u'验证码输入不正确。')])

    def validate_captcha(self,field):
        captcha = field.data
        mail = self.mail.data
        if xtcache.get(mail).lower() == captcha.lower():
            return True
        else:
            raise ValidationError(u'验证码输入错误。')

class CMSAddUser(BaseForm):
    email = StringField(validators=[InputRequired(u'邮箱不能为空！'), Email(u'邮箱格式不正确！')])
    username = StringField(validators=[InputRequired(u'用户名不能为空！')])
    password = StringField(validators=[InputRequired(u'密码不能为空！'), Length(6, 20, message=u'密码格式不正确')])

    def validate_email(self,field):
        email = field.data
        if CMSUser.query.filter(CMSUser.email==email).first():
            raise ValidationError(u'邮箱已存在。')
        return True

class BoardForm(BaseForm):
    board_id = IntegerField(InputRequired(message=u'请传入板块id'))
    board_name = StringField(InputRequired(message=u'请传入板块名称'))

    def validate_board_id(self,field):
        id = field.data
        board = Board.query.get(id)
        if not board:
            raise ValidationError(u'信息传入有误。')
        return True

    def validate_board_name(self,field):
        name = field.name
        if Board.query.filter(Board.name == name).first():
            raise ValidationError(u'板块名称已存在。')
        return True

class HighlightForm(BaseForm):
    is_highlight = BooleanField(validators=[InputRequired(message=u'必须传入加精信息')])
    post_id = IntegerField(validators=[InputRequired(message=u'必须传入post_id')])


