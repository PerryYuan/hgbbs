# coding:utf8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from exts import db
from hgbbs import app
from models import cmsmodels,frontmodels,commonmodels
from utils.helper import Helper

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

CMSUser = cmsmodels.CMSUser
CMSRole = cmsmodels.CMSRole
Permisson = cmsmodels.Permission
FrontUser = frontmodels.FrontUser
Board = commonmodels.Board

@manager.option('-u',dest='username')
@manager.option('-p',dest='password')
@manager.option('-e',dest='email')
@manager.option('-s',dest='permissions')
def add_cms_user(username,password,email,permissions):
    user = CMSUser.query.filter(CMSUser.email==email).first()
    if user:
        print u'cms用户已存在'
        return
    cms_role = CMSRole.query.filter(CMSRole.name == permissions.decode('gbk').encode('utf8')).first()
    print cms_role.name
    if not cms_role:
        print u'没有这个角色。'
    user = Helper().insert(CMSUser,username=username,password=password,email=email)
    user.roles.append(cms_role)
    db.session.commit()
    print u'添加成功'

@manager.option('-n',dest='name')
@manager.option('-d',dest='desc')
@manager.option('-p',dest='permissions')
def add_cms_role(name,desc,permissions):
    cms_role = CMSRole(name=name.decode('gbk').encode('utf8'),desc=desc.decode('gbk').encode('utf8'),permission=permissions)
    db.session.add(cms_role)
    db.session.commit()
    return u'角色添加成功'
@manager.option('-t',dest='telephone')
@manager.option('-u',dest='username')
@manager.option('-p',dest='password')
def add_front_user(telephone,username,password):
    front_user = FrontUser.query.filter_by(telephone=telephone).first()
    if front_user:
        print u'该用户已存在'
        return
    front_user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(front_user)
    db.session.commit()
    print u'用户添加成功'

@manager.option('-n',dest='name')
@manager.option('-a',dest='author_id')
def add_board(name,author_id):
    if Board.query.filter_by(name=name).first():
        print u'该板块已存在'
        return
    board = Board(name=name)
    author = CMSUser.query.get(author_id)
    if not author:
        print u'没有这个作者'
    author.boards.append(board)
    db.session.commit()
    print u'板块添加成功'

if __name__ == '__main__':
    manager.run()