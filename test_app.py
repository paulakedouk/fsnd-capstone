
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
import datetime

TOKEN_PRODUCER = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9ESkdSa00yT0RaR1JrRXdSVFUxUmpGQ01EZzRSRUkzTmpjelJEQkZRamd3UXpaRFFURXlOUSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRwYXVsYS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5MGUyYmY1NGMzMjIwYzY5NzIyODg0IiwiYXVkIjoiYXBpIiwiaWF0IjoxNTg2NTUzNTUzLCJleHAiOjE1ODY1NjA3NTMsImF6cCI6IkVIVUY2bnI2UXBZSlNNWU85QlFGamw0eXFUc1FqWjJtIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.SFhzHnszqVfz4huZnBLZoSF13pKfnbgpMVjUoUTHfJ7IPY7ivrUYO7c4osLkkqEwthIF_1cWokt7SgzQbxaormgD32_JEHfv81ZwBnJSusjY-FJNmjvZTqTNEa4DymwVzxINLFRqVpJ7ThQaoBVvKgdrl9ZYA_ukQMEtNoj1IkwnHjPjM2h54Qn8dLtetDeob0g8K9ZYKQxAaLlCP2EzUGbX6t6VSVqLVqPGwq8JT-inYeGM2R9cHy37Pe_sIgxi7pDggPav_vy0cGXPUbQfWLBqoijm3d3GMVFIMA8-17TPpNu638toaMqFkKwjWXj1isKo0E57NeTgRqSX1EQ7KQ'

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""

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