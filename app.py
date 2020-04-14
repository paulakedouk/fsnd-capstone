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

    @app.route('/logged-in')
    def loggedin():
        return render_template('logged-in.html', movies=Movies.query.all(), actors=Actors.query.all())


    # Actors
    
    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        actors = Actors.query.all()

        act_format = [act.format() for act in actors]

        result = {
            "success": True,
            "actors": act_format
        }
        return jsonify(result)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()
            actor.delete()

            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def edit_actor(payload, id):
        # try:
        #     actor = Actors.query.filter(Actors.id == id).one_or_none()
            
        #     if actor is None:
        #         abort(404)

        #     body = request.get_json()
        #     if 'name' in body:
        #         actor.name = body.get("name")
        #     if 'age' in body:
        #         actor.age = body['age']
        #     if 'gender' in body:
        #         actor.gender = body['gender']
        
        #     actor.update()
            
        #     return jsonify({
        #         'success': True,
        #     })

        # except Exception:
        #     abort(422)
        try:
            actor = Actors.query.filter(Actors.id == id).first()
            
            print(actor.name)
            actor.name = request.args.get("name")
            print(actor.name)
            actor.age = request.args.get("age")
            actor.gender = request.args.get("gender")
            actor.update()

            return jsonify({
                'code': 'success'
            })

        except:
            print("database error")
            abort(422)
        
           

       

    # Movies
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_Movies(payload):
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
        data = request.get_json()
        if not data:
            abort(400)

        new_title = data.get("title")
        new_release_date = data.get("release_date")
        
        new_movie = movies(title=new_title, release_date=new_release_date)

        try:
            new_movie.insert()
        except Exception:
            abort(401)

        return jsonify({"success": True, "movie": new_movie})



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