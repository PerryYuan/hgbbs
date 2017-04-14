# coding:utf8
from datetime import datetime

import json


class RedisHelper(object):
    @classmethod
    def to_dict(cls, model):
        if hasattr(model,'__table__'):
            columns = model.__table__.columns
            model_dict = {}
            for column in columns:
                value = getattr(model, column.name)
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                model_dict[column.name] = value
            return model_dict
        return None

    @classmethod
    def to_json(cls, model, **kwargs):
        model_dict = cls.to_dict(model)
        for key, value in kwargs.iteritems():
            model_dict[key] = cls.to_dict(value) if cls.to_dict(value) else value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime) else value
        return json.dumps(model_dict)