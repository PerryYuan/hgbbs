# coding:utf8
from cms_exts import bp
import flask
from flask.views import MethodView

from models.modelshelper import IndexModelsHelper
from utils.helper import Helper
from models.cmsmodels import CMSUser,CMSRole,Permission
from models.frontmodels import FrontUser
from forms.cmsforms import CMSLoginForm,CMSReSetPWD,\
    CMSReSetMail,CMSAddUser,BoardForm,HighlightForm
import constants
from exts import db
from decorators.cms_decorators import login_required,is_super_required
from utils import xtjson,mailutils,captchautils,xtcache
from shortuuid import uuid
from models.commonmodels import Board,PostModel,HighLightPostModel, CommentModel
from datetime import datetime

@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')

class LoginView(MethodView):
    def get(self,message=None):
        return flask.render_template('cms/login.html',message=message)
    def post(self):
        login_forms = CMSLoginForm(flask.request.form)
        email = login_forms.email.data
        password = login_forms.password.data
        remember = login_forms.remember.data
        if login_forms.validate():
            user = CMSUser.query.filter(CMSUser.email==email).first()
            if user and user.check_pwd(password):
                if not user.is_active:
                    return self.get(message=u'你的账号已被拉黑。。')
                flask.session[constants.CMS_LOGIN_SESSION_ID] = user.id
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('cms.index'))
            else:
                return self.get(message=u'邮箱或密码错误')
        else:
            message = login_forms.get_errors()
            return self.get(message=message)

bp.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))

@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(constants.CMS_LOGIN_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return flask.render_template('cms/profile.html')

class ReSetPWD(MethodView):

    decorators = [login_required]

    def get(self):
        return flask.render_template('cms/resetpwd.html')

    def post(self):
        resetpwd_forms = CMSReSetPWD(flask.request.form)
        oldpwd = resetpwd_forms.oldpwd.data
        newpwd = resetpwd_forms.newpwd.data
        if resetpwd_forms.validate():
            user = flask.g.cms_user
            if user.check_pwd(oldpwd):
                user.password = newpwd
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(u'原密码有误！')
        else:
            message = resetpwd_forms.get_errors()
            return xtjson.json_params_error(message)
bp.add_url_rule('/resetpwd/',endpoint='resetpwd',view_func=ReSetPWD.as_view('resetpwd'))

class ReSetMail(MethodView):
    decorators = [login_required]

    def get(self):
        return flask.render_template('cms/resetmail.html')
    def post(self):
        captcha_forms = CMSReSetMail(flask.request.form)
        if captcha_forms.validate():
            mail = captcha_forms.mail.data
            if flask.g.cms_user.email == mail:
                return xtjson.json_params_error(u'邮箱与原邮箱一致，无需修改。')
            flask.g.cms_user.email = mail
            db.session.commit()
            xtcache.delete(mail)
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=captcha_forms.get_errors())
bp.add_url_rule('/resetmail/',endpoint='resetmail',view_func=ReSetMail.as_view('resetmail'))


@bp.route('/cmsusers/')
@login_required
@is_super_required
def cmsusers():
    users = CMSUser.query.all()
    context = {
        'users':users
    }
    return flask.render_template('cms/cms_users.html',**context)

@bp.route('/addcmsuser/',methods=['GET','POST'])
@login_required
@is_super_required
def add_cms_user():
    if flask.request.method == 'GET':
        roles = CMSRole.query.all()
        context = {
            'roles':roles
        }
        return flask.render_template('cms/add_cms_user.html',**context)
    else:
        form = CMSAddUser(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            username = form.username.data
            roles = flask.request.form.getlist('roles[]')
            if not roles:
                return xtjson.json_params_error(u'至少选择一个分组')
            user = CMSUser(email=email,password=password,username=username)
            for role in roles:
                cms_role = CMSRole.query.get(role)
                cms_role.users.append(user)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(form.get_errors())


@bp.route('/edit_cmsuser/',methods=['GET','POST'])
@login_required
@is_super_required
def edit_cmsuser():
    if flask.request.method == 'GET':
        user_id = flask.request.args.get('user_id')
        if not user_id:
            flask.abort(404)
        user = Helper().query_one(CMSUser,user_id)
        if not user:
            flask.abort(404)
        roles = Helper().query_all(CMSRole)
        user_roles = [role.id for role in user.roles]
        context = {
            'user':user,
            'roles':roles,
            'user_roles':user_roles
        }
        return flask.render_template('cms/cms_edit.html',**context)
    else:
        user_id = flask.request.form.get('user_id')
        role_id_list = flask.request.form.getlist('role_id_list[]')
        if not user_id:
            return xtjson.json_params_error(u'请传入用户信息')
        if not role_id_list:
            return xtjson.json_params_error(u'至少选择一个分组')
        user = Helper().query_one(CMSUser, user_id)
        if not user:
            return xtjson.json_params_error(u'请传入正确的用户信息')
        user.roles[:] = []
        for role_id in role_id_list:
            role = Helper().query_one(CMSRole,role_id)
            user.roles.append(role)
        db.session.commit()
        return xtjson.json_result()

@bp.route('/remove_black/',methods=['POST'])
@login_required
@is_super_required
def remove_black():
    user_id = flask.request.form.get('user_id')
    if not user_id:
        return xtjson.json_params_error(u'请传入用户信息')
    user = Helper().query_one(CMSUser, user_id)
    if not user:
        return xtjson.json_params_error(u'请传入正确的用户信息')
    user.is_active = not user.is_active
    db.session.commit()
    return xtjson.json_result()

@bp.route('/frontuser/')
@login_required
def cms_frontuser():
    sort_value = flask.request.args.get('sort',1,type=int)
    front_users = []
    if sort_value == 1:
        front_users = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    else:
        front_users = FrontUser.query.all()
    context = {
        'front_users':front_users,
        'sort_value':sort_value
    }
    return flask.render_template('cms/cms_frontuser.html',**context)

@bp.route('/editfrontuser/')
@login_required
def edit_frontuser():
    id = flask.request.args.get('id')
    if not id:
        flask.abort(404)
    user = FrontUser.query.get(id)
    if not user:
        flask.abort(404)
    context = {
        'front_user':user
    }
    return flask.render_template('cms/edit_frontuser.html',**context)

@bp.route('/frontuserblack/',methods=['POST'])
@login_required
def front_user_black():
    user_id = flask.request.form.get('user_id')
    if not user_id:
        return xtjson.json_params_error(u'请传入用户信息')
    user = Helper().query_one(FrontUser, user_id)
    if not user:
        return xtjson.json_params_error(u'请传入正确的用户信息')
    user.is_active = not user.is_active
    db.session.commit()
    return xtjson.json_result()

@bp.route('/board/')
@login_required
def board():
    boards = Board.query.all()
    context = {
        'boards':boards
    }
    return flask.render_template('cms/board.html',**context)

@bp.route('/addboard/',methods=['POST'])
@login_required
def add_board():
    board_name = flask.request.form.get('board_name')
    if Board.query.filter(Board.name == board_name).first():
        return xtjson.json_params_error(u'板块已存在')
    board = Board(name=board_name)
    board.author = flask.g.cms_user
    db.session.commit()
    return xtjson.json_result()

@bp.route('/editboard/',methods=['POST'])
@login_required
def edit_board():
    form = BoardForm(flask.request.form)
    if form.validate():
        id = form.board_id.data
        name =form.board_name.data
        board = Board.query.get(id)
        if board.name == name:
            return xtjson.json_params_error(u'板块名称与原名一致，无须修改。')
        board.name = name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(form.get_errors())

@bp.route('/deleteboard/',methods=['POST'])
@login_required
def delete_board():
    id = flask.request.form.get('board_id')
    if not id:
        return xtjson.json_params_error(u'请传入板块id。')
    board = Board.query.get(id)
    if not board:
        return xtjson.json_params_error(u'请传入正确的信息。')
    #如果帖子数大于0，不能删除
    if board.posts.count() > 0:
        return xtjson.json_params_error(u'板块存在帖子，不能删除')
    db.session.delete(board)
    db.session.commit()
    return xtjson.json_result()

@bp.route('/cms_post/')
@login_required
def cms_post():
    sort_type = flask.request.args.get('sort', 1, type=int)
    board_id = flask.request.args.get('board', 0, type=int)
    page = flask.request.args.get('page', 1, type=int)
    context = IndexModelsHelper.get_posts(page, sort_type, board_id)
    return flask.render_template('cms/cms_post.html',**context)

@bp.route('/highlight/',methods=['POST'])
@login_required
def highlight():
    form = HighlightForm(flask.request.form)
    print 'fdasfds'
    if form.validate():
        is_highlight = form.is_highlight.data
        post_id = form.post_id.data
        post = PostModel.query.filter(PostModel.id==post_id).first()
        if not post:
            return xtjson.json_params_error(u'请传入正确的信息')
        if is_highlight:
            if post.highlight:
                return xtjson.json_params_error(u'已经加精，无需再次操作')
            n_highlight = HighLightPostModel()
            post.highlight = n_highlight
            db.session.commit()
            print n_highlight.create_time
            return xtjson.json_result()
        if not post.highlight:
            return xtjson.json_params_error(u'该帖没有加精，无需操作')
        db.session.delete(post.highlight)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(form.get_errors())

@bp.route('/remove_post/',methods=['POST'])
@login_required
def remove_post():
    post_id = flask.request.form.get('post_id')
    if not post_id:
        return xtjson.json_params_error('请传入帖子id')
    post = PostModel.query.filter(PostModel.id==post_id).first()
    if not post:
        return xtjson.json_params_error('请传入正确的信息')
    post.is_removed = True
    db.session.commit()
    return xtjson.json_result()

@bp.route('/cms_comment/')
@login_required
def cms_comment():
    comments = CommentModel.query.filter_by(is_removed=False)
    return flask.render_template('cms/cms_comment.html',comments=comments)

@bp.route('/remove_comment/',methods=['POST'])
def cms_remove_comment():
    comment_id = flask.request.form.get('comment_id')
    if not comment_id:
        return xtjson.json_params_error(u'请传入信息')
    comment = CommentModel.query.filter_by(id=comment_id).first()
    if not comment:
        return xtjson.json_params_error(u'请传入正确的信息')
    comment.is_removed = True
    db.session.commit()
    return xtjson.json_result()

@bp.route('/captcha/')
def get_captcha():
    mail = flask.request.args.get('mail')
    captcha = captchautils.get_captcha(4)
    if xtcache.get(mail):
        return xtjson.json_params_error(u'该邮箱已发过验证码，无须再发送。')
    import re
    r = re.compile(r'\w+@\w+.\w+')
    if not r.findall(mail):
        return xtjson.json_params_error(u'邮箱格式不正确')
    if mailutils.send_mail(subject=u'验证码',recipients=mail,body=u'您的验证码是：%s'%captcha):
        xtcache.set(mail,captcha)
        return xtjson.json_result()
    else:
        return xtjson.json_server_error(u'网络错误。')

@bp.context_processor
def cms_user():
    id = flask.session.get(constants.CMS_LOGIN_SESSION_ID)
    if id:
        user = Helper().query_one(CMSUser,id)
        return {'cms_user':user}
    else:
        return {}

@bp.before_request
def before_request_get_cms_user():
    id = flask.session.get(constants.CMS_LOGIN_SESSION_ID)
    if id:
        user = Helper().query_one(CMSUser,id)
        flask.g.cms_user = user

@bp.errorhandler(404)
def page_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_server_error()
    else:
        return flask.render_template('cms/cms_404.html'),404

@bp.errorhandler(401)
def auth_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.render_template('cms/cms_401.html'),401
