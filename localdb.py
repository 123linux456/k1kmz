#-*- coding=utf-8 -*-
from sqlalchemy import Column, String, create_engine,Integer,Boolean
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

basedir=os.path.abspath('.')
db_path=os.path.join(basedir,'local.db')
# 创建对象的基类:
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    poster=Column(String(200))
    category=Column(String(50))
    status=Column(Boolean)

    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)




class Picture(Base):
    __tablename__ = 'pictures'

    pid = Column(Integer, primary_key=True)
    subid = Column(Integer, primary_key=True)
    url=Column(String(200))

    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)



# 初始化数据库连接:
engine = create_engine('sqlite:///'+db_path)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
if not os.path.exists(db_path):
    Base.metadata.create_all(engine)


class DB():
    def __init__(self,table):
        self.type=table
        self.session=DBSession()

    def insertnew(self,**kwargs):
        exists=True
        if self.type=='Post':
            id=kwargs['id']
            table=Post
            if self.session.query(table).filter(table.id==id).first() is None:
                exists=False
        else:
            pid=int(kwargs['pid'])
            subid=int(kwargs['subid'])
            table=Picture
            if self.session.query(table).filter(table.pid==pid,table.subid==subid).first() is None:
                exists=False
        if not exists:
            if self.type=='Post':
                new_item=Post(**kwargs)
            else:
                new_item=Picture(**kwargs)
            self.session.add(new_item)
            self.session.commit()

    def update(self,**kwargs):
        if self.type=='Post':
            id=int(kwargs['id'])
            status=kwargs['status']
            item=self.session.query(Post).filter(Post.id==id).first()
            item.status=status
            self.session.add(item)
            self.session.commit()
        else:
            pass

    def get_a_item(self):
        #post=self.session.query(Post).order_by(func.rand()).first() #mysql
        post=self.session.query(Post).filter(Post.status==False).order_by(func.random()).first() #pgsql/sqlite
        pictures=self.session.query(Picture).filter(Picture.pid==post.id).all()
        return post,pictures





# session = DBSession()
# # 创建新User对象:
# new_user = User(id='5', name='Bob')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()
