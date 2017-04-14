# coding:utf8


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from exts import db

class Helper(object):
    def insert(self,cls,*args,**kwargs):
        new_cls = cls(**kwargs)
        db.session.add(new_cls)
        db.session.commit()
        return new_cls

    def delete(self,cls,id):
        delete_cls = cls.query.filter(cls.id == id).first()
        db.session.delete(delete_cls)
        db.session.commit()

    def update(self,cls,id,**kwargs):
        update_cls = cls.query.filter(cls.id == id).first()
        for key,value in kwargs.iteritems():
            setattr(update_cls, key, value)
        db.session.commit()

    def query_one(self,cls,id):
        query_cls = cls.query.filter(cls.id == id).first()
        return query_cls

    def query_all(self,cls):
        query_cls_all = cls.query.all()
        return query_cls_all