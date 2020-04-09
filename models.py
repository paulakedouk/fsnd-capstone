
import os
# from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time as time_
import json
from flask_migrate import Migrate

database_name = "capstone"
# user_name = "anaborba"
# password = "012300a"
# database_path = "postgres://{}:{}@{}/{}".format(
#   user_name,
#   password,
#   'localhost:5432',
#   database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()
    
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = app
    db.init_app(app)
    db.create_all()

    migrate = Migrate(app, db)

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()


