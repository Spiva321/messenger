from flask import Blueprint, request
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError

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

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return  {'error': 'USERNAME OR EMAIL ALREADY EXISTS'}, 409

    new_user = User(
        username=username,
        email=email
    )

    new_user.password = password

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'USERNAME OR EMAIL ALREADY EXISTS'}

    return {
        'message': 'user registered successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }, 201

