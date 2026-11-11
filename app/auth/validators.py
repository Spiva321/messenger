import re
from email_validator import validate_email as check_email, EmailNotValidError

def validate_password(password):
    if len(password) < 8:
        return 'Password too short'

    if not re.search('^[a-zA-Z0-9_-]+$', password):
        return 'Invalid password'

    return None

def validate_email(email):
    try:
        check_email(email)
    except EmailNotValidError:
        return 'Invalid email'

    return None

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return 'Username must be between 3 and 20 characters'

    if not re.fullmatch('^[a-zA-Z0-9_-]+$', username):
        return 'Invalid username'

    return None