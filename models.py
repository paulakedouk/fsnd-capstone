
import os
from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_name = "capstone"
user_name = "anaborba"
password = "012300a"
database_path = "postgres://{}:{}@{}/{}".format(
  user_name,
  password,
  'localhost:5432',
  database_name)
  
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release = Column(Float)
    
    def __init__(self, title, release):
        self.title = title
        self.release = release
    
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
          'title': self.title,
          'release': self.release,
        #   'actors': [x.name for x in self.Actors]
        }

