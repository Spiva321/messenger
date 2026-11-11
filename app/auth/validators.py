from email_validator import validate_email, EmailNotValidError

def validate_password(password):
    if len(password) < 8:
        return {'error': 'Password must be at least 8 characters'}, 400

def validate_email(email):
    try:
        validate_email(email)
    except EmailNotValidError:
        return {'error': 'Email is not valid'}, 400

def validate_username(username):
    pass