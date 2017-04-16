# coding:utf8
import flask
from flask import views,session

from decorators.front_decorators import login_required
from front_exts import bp
import constants
from task import celery_send_sms
from utils import xtjson,xtcache,captchautils
from utils.captcha.xtcaptcha import Captcha
from forms.frontforms import FrontRegistForm,FrontLoginForm, UserSettingForm
from models.frontmodels import FrontUser
from exts import db
from datetime import datetime
import front_common

try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

class FrontRegistView(views.MethodView):
    def get(self,message=None,**kwargs):
        context = {
            'message':message
        }
        context.update(kwargs)
        return flask.render_template('front/front_regist.html',**context)

    def post(self):
        form = FrontRegistForm(flask.request.form)
        telephone = form.telephone.data
        username = form.username.data
        if form.validate():
            password = form.password.data
            if FrontUser.query.filter(FrontUser.telephone == telephone).first():
                return self.get(message=u'该手机号码已经注册了')
            front_user = FrontUser(telephone,username,password)
            db.session.add(front_user)
            db.session.commit()
            return flask.redirect(flask.url_for('front.index'))
        else:
           return self.get(message=form.get_errors(),telephone=telephone,username=username)
bp.add_url_rule('/regist/',endpoint='regist',view_func=FrontRegistView.as_view('regist'))

class FrontLoginView(views.MethodView):
    def get(self,message=None,**kwargs):
        context = {
            'message':message
        }
        context.update(kwargs)
        return flask.render_template('front/front_login.html',**context)
    def post(self):
        form = FrontLoginForm(flask.request.form)
        telephone = form.telephone.data
        if form.validate():
            password = form.password.data
            remember = form.remember.data
            front_user = FrontUser.query.filter(FrontUser.telephone==telephone).first()
            if not (front_user and front_user.check_pwd(password)):
                return self.get(message=u'手机号码或密码错误。', telephone=telephone)
            if not front_user.is_active:
                return self.get(message=u'你已拉黑，暂不能登录，请联系管理员', telephone=telephone)
            session[constants.FRONT_LOGIN_SESSION_ID] = front_user.id
            session.permanent = remember
            if front_user.old_login_time:
                front_user.last_login_time = front_user.old_login_time
            front_user.old_login_time = datetime.now()
            db.session.commit()
            return flask.redirect(flask.url_for('front.index'))
        else:
            return self.get(message=form.get_errors(),telephone=telephone)

bp.add_url_rule('/login/',endpoint='login',view_func=FrontLoginView.as_view('login'))


@bp.route('/alidayu_captcha/')
def alidayu_captcha():
    telephone = flask.request.args.get('telephone')
    if not telephone:
        return xtjson.json_params_error(message=u'手机不能为空。')
    if xtcache.get(telephone):
        return xtjson.json_params_error(message=u'短信已发送，短时间内不能重复发送')
    captcha = captchautils.get_captcha(4)
    req = celery_send_sms(captcha,telephone)
    try:
        resp = req.getResponse()
        print(resp)
        xtcache.set(telephone,captcha)
        return xtjson.json_result()
    except Exception, e:
        print(e)
        return xtjson.json_server_error()

@bp.route('/user_setting/',methods=['GET','POST'])
@login_required
def user_setting():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_user_setting.html')
    else:
        form = UserSettingForm(flask.request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            email = form.email.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            user = flask.g.front_user
            if user.username != username:
                user.username = username
            if realname:
                user.realname = realname
            if email:
                user.email = email
            if qq:
                user.qq = qq
            if avatar:
                user.avatar = avatar
            if signature:
                user.signature = signature
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(form.get_errors())

@bp.route('/logout/')
def logout():
    session.pop(constants.FRONT_LOGIN_SESSION_ID)
    return flask.redirect(flask.url_for('front.login'))

@bp.route('/user_info/<string:user_id>/')
def user_info(user_id):
    user = FrontUser.query.filter_by(id=user_id,is_active=True).first()
    if not user:
        return flask.abort(404)
    context = {
        'active':0,
        'user':user
    }
    return flask.render_template('front/front_user_info.html',**context)

@bp.route('/user_post/<string:user_id>/')
def user_post(user_id):
    user = FrontUser.query.filter_by(id=user_id, is_active=True).first()
    if not user:
        return flask.abort(404)
    context = {
        'active': 1,
        'user': user
    }
    return flask.render_template('front/front_user_post.html', **context)

@bp.route('/graph_captcha/')
def graph_captcha():
    out = StringIO()
    text,image = Captcha.gene_code()
    image.save(out,'png')
    out.seek(0)

    response = flask.make_response(out.read())
    response.content_type = 'image/png'
    xtcache.set(text.lower(),text.lower(),timeout=2*60)
    return response


