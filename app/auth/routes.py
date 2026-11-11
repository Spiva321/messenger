from calendar import day_abbr

from flask import Blueprint, request
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    return {'message': 'its work'}, 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return {'error': 'Request body must contain JSON'}, 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'error': 'All fields are required'}, 400

    return {'message': 'reg endpoint works'}, 200

