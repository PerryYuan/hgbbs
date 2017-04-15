# coding:utf8
from datetime import datetime
import constants
from exts import db
from models.commonmodels import PostModel, HighLightPostModel, PostStar, CommentModel, Board
import json

from utils.phredis import BBSRedis

class IndexModelsHelper(object):
    
    class PostSortType(object):
        CREATE_TIME = 1
        HIGHLIGH_TIME = 2
        STAR_COUNT = 3
        COMMENT_COUNT = 4

    @classmethod
    def get_posts(cls,page,sort_type,board_id):

        start = (page - 1) * constants.PAGE_COUNT
        end = start + constants.PAGE_COUNT
        posts = []
        if sort_type == cls.PostSortType.CREATE_TIME:
            posts = PostModel.query.filter(PostModel.is_removed == False).order_by(PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.HIGHLIGH_TIME:
            posts = db.session.query(PostModel).outerjoin(HighLightPostModel). \
                filter(PostModel.is_removed == False).order_by(HighLightPostModel.create_time.desc(),
                                                        PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.STAR_COUNT:
            posts = db.session.query(PostModel).filter(PostModel.is_removed == False).outerjoin(PostStar). \
                group_by(PostModel.id).order_by(db.func.count(PostStar.id).desc(), PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.COMMENT_COUNT:
            posts = db.session.query(PostModel).filter(PostModel.is_removed == False).outerjoin(CommentModel). \
                group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(), PostModel.create_time.desc())
        if board_id:
            posts = posts.filter(PostModel.board_id == board_id)

        total = posts.count()
        # boards = [json.loads(board) for board in BBSRedis.board.boards()]
        boards = Board.query.all()
        pages = []
        page_temp = page - 1
        while page_temp > 0 and page_temp % 5 != 0:
            pages.append(page_temp)
            page_temp -= 1

        page_total = total / constants.PAGE_COUNT
        if total % constants.PAGE_COUNT > 0:
            page_total += 1
        page_temp = page
        while page_temp <= page_total:
            pages.append(page_temp)
            if page_temp % 5 == 0:
                break
            page_temp += 1

        pages.sort()
        context = {'pages': pages, 'c_page': page, 'boards': boards, 'posts': posts.slice(start, end),
            'page_total': page_total, 'sort_type': sort_type, 'board_id': board_id}
        return context

    @classmethod
    def sort_post(cls,sort_type,start,end):

        posts = []
        if sort_type == cls.PostSortType.CREATE_TIME:
            posts = PostModel.query.filter(PostModel.is_removed == False).order_by(PostModel.create_time.desc()).slice(start,end)
        elif sort_type == cls.PostSortType.HIGHLIGH_TIME:
            posts = db.session.query(PostModel).outerjoin(HighLightPostModel). \
                filter(PostModel.is_removed == False).order_by(HighLightPostModel.create_time.desc(),
                                                        PostModel.create_time.desc()).slice(start,end)
        elif sort_type == cls.PostSortType.STAR_COUNT:
            posts = db.session.query(PostModel).filter(PostModel.is_removed == False).outerjoin(PostStar). \
                group_by(PostModel.id).order_by(db.func.count(PostStar.id).desc(), PostModel.create_time.desc()).slice(start,end)
        elif sort_type == cls.PostSortType.COMMENT_COUNT:
            posts = db.session.query(PostModel).filter(PostModel.is_removed == False).outerjoin(CommentModel). \
                group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(), PostModel.create_time.desc()).slice(start,end)

        return posts

    @classmethod
    def get_posts_cache(cls, page, sort_type, board_id):

        start = (page - 1) * constants.PAGE_COUNT
        end = start + constants.PAGE_COUNT
        if start >= 50:
            return cls.get_posts(page, sort_type, board_id)

        posts = []
        if sort_type == cls.PostSortType.CREATE_TIME:
            posts = BBSRedis.post.posts_create_time(start, end)
        elif sort_type == cls.PostSortType.HIGHLIGH_TIME:
            posts = BBSRedis.post.posts_highlight(start, end)
        elif sort_type == cls.PostSortType.STAR_COUNT:
            posts = BBSRedis.post.posts_star(start, end)
        elif sort_type == cls.PostSortType.COMMENT_COUNT:
            posts = BBSRedis.post.posts_comment(start, end)

        post_list = []
        for post in posts:
            post_list.append(json.loads(post))
        posts_temp = []
        boards = [json.loads(board) for board in BBSRedis.board.boards()]
        if board_id:
            for board in boards:
                if board.get('id') == board_id and board.get('post_count') < 50:
                    return cls.get_posts(page, sort_type, board_id)
            for post in post_list:
                if int(post.get('board_id')) == board_id:
                    posts_temp.append(post)
                    print 0
            posts = posts_temp
        else:
            posts = post_list
        total = int(BBSRedis.get('posts_count'))
        pages = []
        page_temp = page - 1
        while page_temp > 0 and page_temp % 5 != 0:
            pages.append(page_temp)
            page_temp -= 1

        page_total = total / constants.PAGE_COUNT
        if total % constants.PAGE_COUNT > 0:
            page_total += 1
        page_temp = page
        while page_temp <= page_total:
            pages.append(page_temp)
            if page_temp % 5 == 0:
                break
            page_temp += 1

        pages.sort()
        context = {'pages': pages, 'c_page': page, 'boards': boards, 'posts': posts,
                   'page_total': page_total, 'sort_type': sort_type, 'board_id': board_id}
        return context

