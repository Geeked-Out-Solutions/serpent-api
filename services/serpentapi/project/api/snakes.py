

from sqlalchemy import exc
from flask import Flask, Blueprint, jsonify, request
from project.api.models.snake import Snake, SnakeSchema
from project.api.models.user import User
from project import db
from project.api.utils import authenticate, is_admin
import logging

snakes_blueprint = Blueprint('snakes', __name__, template_folder='./templates')
snake_schema = SnakeSchema()


app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers

@snakes_blueprint.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@snakes_blueprint.route('/api/snake', methods=['POST'])
@authenticate
def add_snake(resp):
    # get post data
    post_data = request.get_json()
    post_data['owner_id'] = resp
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    data, error = snake_schema.load(post_data)
    if error:
        return jsonify(error, 400)
    snake = Snake(data)
    snake.save()
    data = snake_schema.dump(snake).data
    app.logger.debug(data)
    response_object['status'] = 'success'
    response_object['message'] = 'Successfully added snake.'
    return jsonify(response_object), 201

@snakes_blueprint.route('/api/snake', methods=['GET'])
@authenticate
def get_all_snakes(resp):
    """Get all snakes owned by you"""
    snakes = Snake.get_all_snakes(resp)
    data = snake_schema.dump(snakes, many=True).data
    response_object = {
        'status': 'success',
        'data': data
    }
    return jsonify(response_object), 200
