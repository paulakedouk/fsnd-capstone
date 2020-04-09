import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,PATCH')
        return response

    @app.route('/')
    def welcome():
        message = 'Welcome to the Casting Agency'
        return jsonify(message)

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_Actors(payload):
        '''
        This endpoint is responsible for returning all Actors from DB
        '''
        actors = Actors.query.all()
        act_format = [act.format() for act in actors]
        result = {
            "success": True,
            "Actors": act_format
        }
        return jsonify(result)

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        '''
        This endpoint is responsible for returning all Movies from DB
        '''
        movies = Movies.query.all()
        movies_list = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies_list': movies_list
        }), 200


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)