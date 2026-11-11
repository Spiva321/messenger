import os

from flask import Flask
from .config import config
from .extensions import jwt, db, migrate
from .auth.routes import auth_bp
from app.models import User

def create_app(config_name=None):
    config_name = config_name or os.environ.get('APP_ENV') or 'default'
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)

    return app