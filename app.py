import os
from flask import Flask, request, abort, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    #CORS Headers
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
    def index():
        return render_template('login.html')

    # Actors

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actors.query.all()

        actors = []

        for actor in selection:
            actors.append(actor.format())

        return jsonify({
            'status': True,
            'actors': actors
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            act = Actors.query.filter_by(id=id).one_or_none()
            act.delete()
            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)


    # Movies
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_Movies(payload):
        '''
        This endpoint is responsible for returning all Movies from DB
        '''
        movies = Movies.query.all()
        mov_format = [mov.format() for mov in movies]
        result = {
            "success": True,
            "movies": mov_format
        }
        return jsonify(result)



    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)