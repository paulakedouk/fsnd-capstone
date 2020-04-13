
import os
from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time as time_
import json
from flask_migrate import Migrate

# database_name = "capstone"
# user_name = "anaborba"
# password = "012300a"
# database_path = "postgres://{}:{}@{}/{}".format(
#   user_name,
#   password,
#   'localhost:5432',
#   database_name)

os.environ['DATABASE_URL'] = 'postgres://heoxxydraglsmt:78b7fe5638a8b28c7a5e2e68568348f8b83ccb2003c5420d78535da083f82943@ec2-54-157-78-113.compute-1.amazonaws.com:5432/d7cu2pq6vjbrnc'
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = app
    db.init_app(app)
    # db.create_all()

    migrate = Migrate(app, db)

class Actors(db.Model):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    # movie = db.relationship("Movies", backref=db.backref('actor', lazy=True))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

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
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

class Movies(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    releaseDate = Column(db.DateTime(timezone=False), nullable=False)

    def __init__(self, title, releaseDate, actor_id):
        self.title = title
        self.releaseDate = releaseDate

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
            'releaseDate': self.releaseDate.strftime('%c'),
        }