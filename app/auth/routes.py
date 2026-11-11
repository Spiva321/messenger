from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    return {'message': 'its work'}, 200
