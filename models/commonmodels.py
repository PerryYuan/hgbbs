# coding:utf8

from exts import db
from datetime import datetime

class Board(db.Model):
    __tablename__ ='board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),unique=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

    author_id = db.Column(db.Integer,db.ForeignKey('cms_user.id'))
    author = db.relationship('CMSUser',backref='boards')

class HighLightPostModel(db.Model):
    __tablename__ = 'highlightpost'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_removed = db.Column(db.Boolean, default=False)

    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    highlight_id = db.Column(db.Integer,db.ForeignKey('highlightpost.id'))

    board = db.relationship('Board',backref=db.backref('posts',lazy='dynamic'))
    author = db.relationship('FrontUser', backref=db.backref('posts',lazy='dynamic'))
    highlight = db.relationship('HighLightPostModel',backref='post',uselist=False)

class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_removed = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    author = db.relationship('FrontUser',backref=db.backref('comments',lazy='dynamic'))
    post = db.relationship('PostModel',backref='comments')

    origin_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    origin_comment = db.relationship('CommentModel',backref='replys',remote_side=[id])

class PostStar(db.Model):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))

    post = db.relationship('PostModel',backref='stars')
    author = db.relationship('FrontUser',backref='stars')