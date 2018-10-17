''' controller and routes for users '''
import os
from flask import request, jsonify
from app import app, mongo, flask_bcrypt, jwt
import logger
import configparser
from app.schemas.user import validate_user
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

config = configparser.ConfigParser()
config.read('config.ini')

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, config['LOGGING']['FILENAME']))


@app.route('/user', methods=['GET', 'DELETE'])
@jwt_required
def user():
    if request.method == 'GET': #TODO: return all users if there was no argument specified
        #TODO: check if email address was provided in the query args
        query = request.args
        data = mongo.db.users.find_one(query)
        del data['password']
        return jsonify({'ok': True, 'data': data}), 200
    data = request.get_json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@app.route('/register', methods=['POST'])
def register():
    # register user endpoint
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        mongo.db.users.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/login', methods=['POST'])
def auth_user():
    # auth endpoint
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']})
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            user['token'] = create_access_token(identity=data)
            user['refresh'] = create_refresh_token(identity=data)
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # refresh token endpoint
    current_user = get_jwt_identity()
    ret = {
            'token': create_access_token(identity=current_user),
            'refresh': create_refresh_token(identity=current_user)
        }
    return jsonify({'ok': True, 'data': ret}), 200

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401
