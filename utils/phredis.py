# coding:utf8
import redis
from models.redishelper import RedisHelper

class PostRedis(object):

    def __init__(self, cache):
        self.cache = cache

    def add_posts_create_time(self,post_model):
        self.cache.rpush('posts_create_time', self.add_post(post_model))
    def add_post_highlight(self,post_model):
        self.cache.rpush('posts_highlight', self.add_post(post_model))
    def add_post_star(self,post_model):
        self.cache.rpush('post_star', self.add_post(post_model))
    def add_post_comment(self,post_model):
        self.cache.rpush('post_comment', self.add_post(post_model))

    def add_post(self,post_model):
        post_temp = None
        context = {
            'author': post_model.author
        }
        if post_model.highlight:
            context['highlight'] = post_model.highlight.create_time
        else:
            context['highlight'] = None

        post_temp = RedisHelper.to_json(post_model,**context)
        return post_temp

    def posts_create_time(self,start,end):
        return self.cache.lrange('posts_create_time',start,end)

    def posts_highlight(self, start, end):
        return self.cache.lrange('posts_highlight', start, end)

    def posts_star(self, start, end):
        return self.cache.lrange('post_star', start, end)

    def posts_comment(self, start, end):
        return self.cache.lrange('post_comment', start, end)

class BoardRedis(object):
    def __init__(self, cache):
        self.cache = cache

    def add_board(self,board):
        self.cache.rpush('boards',RedisHelper.to_json(board,post_count=board.posts.filter_by(is_removed=False).count()))
    def boards(self):
        return self.cache.lrange('boards',0,-1)


class BBSRedis(object):
    _pool = redis.ConnectionPool(host='127.0.0.1', port=2224)
    cache = redis.Redis(connection_pool=_pool)
    post = PostRedis(cache)
    board = BoardRedis(cache)
    @classmethod
    def set(cls,name,value):
        cls.cache.set(name,value)

    @classmethod
    def get(cls,name):
        return cls.cache.get(name)


