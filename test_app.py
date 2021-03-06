
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
        self.user_name = "anaborba"
        self.password = "012300a"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.user_name,
            self.password,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_Unauthorized_Permission(self):
        res = self.client().get('/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['success'], False)

    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer '+self.token_assistant})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

if __name__ == "__main__":
    unittest.main()