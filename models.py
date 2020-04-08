
import os
from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

os.environ['DATABASE_URL'] = '''postgres://heoxxydraglsmt:78b7fe5638a8b28c7a5e2e68568348f8b83ccb2003c5420d78535da083f82943@ec2-54-157-78-113.compute-1.amazonaws.com:5432/d7cu2pq6vjbrnc'''
db = SQLAlchemy()

def setup_db(app):
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://anaborba:012300a@localhost:5432/capstone'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

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

