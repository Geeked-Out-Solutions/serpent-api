from flask import Blueprint, jsonify


snakes_blueprint = Blueprint('snakes', __name__, template_folder='./templates')


@snakes_blueprint.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
