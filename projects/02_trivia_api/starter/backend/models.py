import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"

# When submitting, use the first path that has no user name or password.
#database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  #category = Column(String)
  difficulty = Column(Integer)
  category = Column(Integer, db.ForeignKey('categories.id'), nullable=False)

  def __init__(self, question, answer, difficulty, category=1):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty
    self.category = category

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  questions = db.relationship('Question', backref='parent_cate', lazy=True, cascade='all, delete-orphan')

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

  @classmethod
  def get_all(cls):
    categories = Category.query.order_by(Category.id).all()
    cate_ressult = {}
    
    for cate in categories:
      cate_ressult[cate.id] = cate.type
    
    return cate_ressult