
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
import datetime

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.token_assistant = os.environ['assistant_token']
        self.token_director = os.environ['director_token']
        self.token_producer = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        selection = Movies.query.filter(Movies.title == 'GoGo').all()
        for movie in selection:
            movie.delete()
        # selection = Actor.query.filter(Actor.name == 'John Smith').all()
        # for actor in selection:
        #     actor.delete()
        pass

if __name__ == "__main__":
    unittest.main()