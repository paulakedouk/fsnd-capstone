import os
from flask import Flask, request, abort, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actors, Movies
import datetime
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
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('login.html')
    @app.route('/logged-in')
    def loggedin():
        return render_template('logged-in.html', movies=Movies.query.all(), actors=Actors.query.all())


    # Actors
    
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.all()

        act_format = [act.format() for act in actors]

        result = {
            "success": True,
            "actors": act_format
        }
        return jsonify(result)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor(payload):
        try:
            name = request.args.get("name")
            age = request.args.get("age")
            gender = request.args.get("gender")

            new_actor = Actors(name=name, age=age, gender=gender)
            new_actor.insert()
        except:
            abort(422)

        finally:
            db.session.close()
            return jsonify({
                'name': name,
                'age': age,
                'gender': gender
            })
    
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        selection_id = Actors.query.get(id)
        if not selection_id:
                abort(404)

        try:
            selection = Actors.query.filter(Actors.name == selection_id.name).all()
            for actor in selection:
                actor.delete()
            return jsonify({
                'status': True,
                'actor': selection_id.name
            })

        except Exception:
                abort(422)

    @app.route('/actors/<int:id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        try:
            actor = Actors.query.filter_by(id=id).first()
            
            uptated_name = request.args.get("name")
            uptated_age = request.args.get("age")
            uptated_gender = request.args.get("gender")

            uptaded_actor = Actors(name=uptated_name, age=uptated_age, gender=uptated_gender)
            uptaded_actor.update()

            return jsonify({
                'code': 'success'
            })
        
        except Exception:
            abort(422)

    
    # Movies
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        '''
        This endpoint is responsible for returning all Movies from DB
        '''
        movies = Movies.query.all()
        # print(movies)
        mov_format = [mov.format() for mov in movies]

        result = {
            "success": True,
            "movies": mov_format
        }
        return jsonify(result)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()
        print(body)
        
        release_date = request.get_json()['release_date']
        actor_id = request.get_json()['actor_id']
        
        movie = Movies(title=title, release_date=release_date, actor_id=actor_id)
        movie.insert()
        
        return jsonify({
            'title': movie.title,
            'release_date': movie.release_date,
            'actor_id': movie.actor_id
        })

    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        selection_id = Movies.query.get(id)

        if not selection_id:
            abort(404)

        try:
            selection = Movies.query.filter(Movies.title == selection_id.title).all()
            for movie in selection:
                movie.delete()
            return jsonify({
                'status': True,
                'movie': selection_id.title
            })

        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
    
        try:
            movie = Movies.query.filter_by(id=id).first()
            
            uptated_title = request.args.get("title")
            uptated_release_date = request.args.get("release_date")
            uptated_actor_id = request.args.get("actor_id")

            uptaded_movie = Movies(title=uptated_title, release_date=uptated_release_date, actor_id=uptated_actor_id)
            uptaded_movie.update()

            return jsonify({
                'code': 'success'
            })
        
        except Exception:
            abort(422)
    

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
        }), 500

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)