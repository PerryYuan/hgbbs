# coding:utf8

from wtforms import StringField,BooleanField,ValidationError,IntegerField,TextAreaField
from wtforms.validators import InputRequired,Email,Length,EqualTo
from forms.frontforms import GraphCaptchaForm

class PostForm(GraphCaptchaForm):
    title = StringField(validators=[InputRequired(message=u'标题不能为空。')])
    board_id = IntegerField(validators=[InputRequired(message=u'板块id不能为空。')])
    content = StringField(validators=[InputRequired(message=u'内容不能为空。')])
