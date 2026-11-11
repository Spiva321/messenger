from flask import Blueprint, request
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.auth.validators import validate_username, validate_email, validate_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask import jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    return {'message': 'its work'}, 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {'error': 'Invalid request body'}, 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {'error': 'All fields are required'}, 400

    errors = {
        'username': validate_username(username),
        'email': validate_email(email),
        'password': validate_password(password)
    }

    errors = {field: error for field, error in errors.items() if error}

    if errors:
        return {'errors': errors}, 400

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
        return {'error': 'Username or email already exists'}, 409

    return {
        'message': 'user registered successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {'error': 'Invalid request body'}, 400


    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'error': 'All fields are required'}, 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'Invalid username or password'}, 401

    if not user.verify_password(password):
        return {'error': 'Invalid password'}, 401

    access_token = create_access_token(identity=str(user.id))


    response = jsonify({
        'message': 'login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

    set_access_cookies(response, access_token)

    return response, 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()

    user = db.session.get(User, int(current_user_id))

    if not user:
        return {'error': 'User not found'}, 404

    return {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }, 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({
        'message': 'logout successful'
    })

    unset_jwt_cookies(response)

    return response, 200


