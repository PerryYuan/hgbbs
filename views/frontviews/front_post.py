# coding:utf8
from front_exts import bp
import flask
from decorators.front_decorators import login_required
import front_common
from models.commonmodels import Board,PostModel,CommentModel, PostStar, HighLightPostModel
from models.frontmodels import FrontUser
from forms.commonforms import PostForm
from forms.frontforms import AddCommentForm, PostStarForm
from utils import xtjson
from exts import db
import qiniu
import constants
from datetime import datetime
from models.modelshelper import IndexModelsHelper
import cProfile

@bp.route('/')
def index():
    return page_deal(1,1,0)

@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    if flask.request.method == 'GET':
        boards = Board.query.all()
        return flask.render_template('front/front_addpost.html',boards=boards)
    else:
        postform = PostForm(flask.request.form)
        if postform.validate():
            title = postform.title.data
            content = postform.content.data
            board_id = postform.board_id.data
            board = Board.query.filter(Board.id == board_id).first()
            if not board:
                return xtjson.json_params_error(u'板块id不存在。')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = flask.g.front_user
            db.session.add(post)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(postform.get_errors())

@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    post = PostModel.query.filter(PostModel.id==post_id,PostModel.is_removed==False).first()
    if not post:
        flask.abort(404)
    post.read_count += 1
    db.session.commit()
    comments = CommentModel.query.filter(CommentModel.post_id==post_id).order_by(CommentModel.create_time.desc())
    post_stars = PostStar.query.filter(PostStar.post_id == post_id)
    if post_stars:
        post_star_ids = [star.author.id for star in post_stars]
    context = {
        'post': post,
        'comments': comments,
        'post_star_ids': post_star_ids
    }
    return flask.render_template('front/front_postdetail.html',**context)

@bp.route('/list/<int:page>/<int:sort_type>/<int:board_id>/')
def page_deal(page,sort_type,board_id):
    # cprofile = cProfile.Profile()
    # cprofile.runcall(IndexModelsHelper.get_posts,page,sort_type,board_id)
    context = IndexModelsHelper.get_posts(page,sort_type,board_id)
    # print cprofile.print_stats()
    return flask.render_template('front/front_index.html',**context)

@bp.route('/add_comment/',methods=['GET','POST'])
@login_required
def add_comment():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id')
        comment_id = flask.request.args.get('comment_id')
        post = PostModel.query.get(post_id)
        context = {
            'post': post,
        }
        if comment_id:
            comment = CommentModel.query.get(comment_id)
            context['comment'] = comment
        return flask.render_template('front/add_comment.html',**context)
    else:
        form = AddCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data
            post = PostModel.query.filter(PostModel.id == post_id).first()
            if not post:
                return xtjson.json_params_error(u'请传入正确的信息')
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = flask.g.front_user
            if comment_id:
                origin_comment = CommentModel.query.filter(CommentModel.id == comment_id).first()
                if origin_comment:
                    comment.origin_comment = origin_comment
            db.session.add(comment)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(form.get_errors())


@bp.route('/post_star/',methods=['POST'])
@login_required
def post_star():
    form = PostStarForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data
        post = PostModel.query.filter(PostModel.id == post_id).first()
        if not post:
            return xtjson.json_params_error(u'请传入正确的信息。')
        post_star_model = PostStar.query.filter_by(post_id=post_id,author_id=flask.g.front_user.id).first()
        if is_star:
            if post_star_model:
                return xtjson.json_params_error(u'一点过赞，无须再点啦！')
            n_post_star = PostStar()
            n_post_star.post = post
            n_post_star.author = flask.g.front_user
            db.session.commit()
            return xtjson.json_result()
        else:
            if post_star_model:
                db.session.delete(post_star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(u'没点过赞，不能取消！')
    else:
        return xtjson.json_params_error(form.get_errors())

@bp.route('/test/')
def test():
    # user = FrontUser.query.first()
    # post = PostModel.query.first()
    # comment = CommentModel(content='aaaa')
    # comment.author = user
    # comment.post = post
    # db.session.add(comment)
    # board = Board.query[0]
    # for x in range(100):
    #     title = u'标题，%s' % x
    #     content = u'内容，%s' % x
    #     post = PostModel(title=title,content=content)
    #     post.board = board
    #     post.author = user
    # db.session.commit()
    from utils.phredis import BBSRedis
    # posts = PostModel.query.filter(PostModel.is_removed==False).order_by(PostModel.create_time.desc()).slice(0,50)
    # posts = db.session.query(PostModel).outerjoin(HighLightPostModel). \
    #             filter(PostModel.is_removed == False).order_by(HighLightPostModel.create_time.desc(),
    #
    #                                        PostModel.create_time.desc()).slice(0,50)
    # post_create_time = IndexModelsHelper.sort_post(1,0,50)
    # post_highlight = IndexModelsHelper.sort_post(2,0,50)
    post_star = IndexModelsHelper.sort_post(3,0,50)
    # post_comment = IndexModelsHelper.sort_post(4,0,50)
    for i in range(post_star.count()):
    #     BBSRedis.post.add_post_highlight(post_highlight[i])
    #     BBSRedis.post.add_posts_create_time(post_create_time[i])
        BBSRedis.post.add_post_star(post_star[i])
    #     BBSRedis.post.add_post_comment(post_comment[i])
        # if post.highlight:
        #     BBSRedis.post.add_post(post,author=post.author,highlight=post.highlight)
        # else:
        #     BBSRedis.post.add_post(post, author=post.author)
    # BBSRedis.set('posts_count',PostModel.query.filter(PostModel.is_removed==False).count())

    boards = Board.query.all()
    for board in boards:
        BBSRedis.board.add_board(board)
    return 'success'

@bp.route('/qiniu_token/')
def qiniu_token():
    # import qiniu.config
    # 构建鉴权对象
    q = qiniu.Auth(constants.QINIU_ACCESS_KEY, constants.QINIU_SECRET_KEY)
    # 要上传的空间
    bucket_name = 'hgbbs'
    # 上传到七牛后保存的文件名
    # key = 'my-python-logo.png';
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    return flask.jsonify({'uptoken':token})
    # # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = qiniu.put_file(token, key, localfile)