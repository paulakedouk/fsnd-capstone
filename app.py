import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def welcome():
        message = 'Welcome to the Casting Agency'
        return jsonify(message)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            movies_list = [movie.format() for movie in movies]
            
            return jsonify({
                'success': True,
                'movies_list': movies_list
            }), 200

        except Exception:
            abort(422)

    return app

app = create_app()
