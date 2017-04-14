# coding:utf8
from datetime import datetime

from flask import Flask
import flask
from exts import db,mail
import config
from views.cmsviews import cms_views
from views.frontviews import front_view,front_exts,front_post
from flask_wtf import CSRFProtect



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
app.register_blueprint(cms_views.bp)
app.register_blueprint(front_exts.bp)
CSRFProtect(app)
mail.init_app(app)


@app.template_filter('time_filter')
def time_filter(time_f):
    if not isinstance(time_f,datetime):
        return time_f
    now = datetime.now()
    total_s = (now - time_f).total_seconds()
    if total_s < 60:
        return u'刚刚'
    elif total_s >= 60 and total_s < 60*60:
        return u'%s分钟之前' % int(total_s/60)
    elif total_s >= 60*60 and total_s < 60*60*24:
        return u'%s小时之前' % int(total_s/(60*60))
    elif total_s >= 60*60*24 and total_s < 60*60*24*30:
        return u'%s天之前' % int(total_s/(60*60*24))
    elif now.year == time_f.year:
        return time_f.strftime('%m-%d %H:%M:%S')
    else:
        return time_f.strftime('%Y-%m-%d %H:%M:%S')



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='192.168.56.1',debug=True) #qq 微信分享要用ip
