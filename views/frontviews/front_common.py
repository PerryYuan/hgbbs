# coding:utf8
from front_exts import bp
import flask
import constants
from models.frontmodels import FrontUser
from utils import xtjson

@bp.before_request
def front_before_request():
    id = flask.session.get(constants.FRONT_LOGIN_SESSION_ID)
    if id:
        front_user = FrontUser.query.get(id)
        if front_user:
            flask.g.front_user = front_user

@bp.context_processor
def front_context_processor():
    if hasattr(flask.g,'front_user'):
        return {'front_user':flask.g.front_user}
    return {}

@bp.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    return flask.redirect(flask.url_for('front.login'))

@bp.errorhandler(404)
def page_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error(u'你访问的页面不存在')
    return flask.render_template('front/404.html'),404

@bp.errorhandler(405)
def post_auth_forbidden2(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    return flask.render_template('front/402.html'),405