# coding:utf8
from base_form import BaseForm
from wtforms import StringField,BooleanField,ValidationError,IntegerField,TextField
from wtforms.validators import InputRequired,Email,Length,EqualTo,URL
from utils.captcha.xtcaptcha import Captcha
from utils import xtcache
import re
from models.frontmodels import FrontUser

class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码')])

    def validate_graph_captcha(self, field):
        captcha = field.data
        if Captcha.check_captcha(captcha):
            return True
        else:
            raise ValidationError(u'验证码输入错误。')

class FrontRegistForm(BaseForm):
    telephone = StringField(validators=[InputRequired(message=u'请输入手机号码。')])
    alidayu_captcha = StringField(validators=[InputRequired(message=u'请输入手机验证码')])
    username = StringField(validators=[InputRequired(u'用户名不能为空！')])
    password = StringField(validators=[InputRequired(u'密码不能为空！'),Length(6,20,message=u'密码格式不正确！')])
    password_repeat = StringField(validators=[EqualTo('password',message=u'两次密码不一致！')])
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码')])

    def validate_alidayu_captcha(self,field):
        captcha = field.data
        telephone = self.telephone.data
        cache_captcha = xtcache.get(telephone)
        if cache_captcha and captcha.lower() == cache_captcha.lower():
            return True
        else:
            raise ValidationError(u'手机验证码输入错误。')

    def validate_graph_captcha(self, field):
        captcha = field.data
        if Captcha.check_captcha(captcha):
            return True
        else:
            raise ValidationError(u'验证码输入错误。')

    def validate_telephone(self,field):
        telephone = field.data
        r = re.compile("^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$")
        if r.match(telephone):
            return True
        else:
            raise ValidationError(u'手机号码格式错误')

class FrontLoginForm(BaseForm):
    telephone = StringField(validators=[InputRequired(message=u'请输入手机号码。')])
    password = StringField(validators=[InputRequired(u'密码不能为空！')])
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入验证码')])
    remember = BooleanField()

    def validate_graph_captcha(self, field):
        captcha = field.data
        if Captcha.check_captcha(captcha):
            return True
        else:
            raise ValidationError(u'验证码输入错误。')

class AddCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(u'必须输入帖子id')])
    content = StringField(validators=[InputRequired(u'请输入内容')])
    comment_id = IntegerField()

class PostStarForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(u'必须输入帖子id。')])
    is_star = BooleanField(validators=[InputRequired(u'必须输入点赞行为。')])

class UserSettingForm(BaseForm):
    username = StringField(validators=[InputRequired(u'用户名不能为空！')])
    realname = StringField(validators=[Length(min=2,message=u'姓名必须大于两个字')])
    email = StringField(validators=[Email(message=u'邮箱格式不正确')])
    qq = StringField()
    avatar = StringField(validators=[URL(u'头像格式不正确')])
    signature = StringField()

    def validate_qq(self,field):
        qq = field.data
        if qq.isdigit():
            return True
        raise ValidationError(u'qq格式不正确')