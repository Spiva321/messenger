from app.extensions import db
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

password_hasher = PasswordHasher()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, raw_password):
        self.password_hash = password_hasher.hash(raw_password)

    def verify_password(self, raw_password):
        try:
            return password_hasher.verify(self.password_hash, raw_password)
        except (VerifyMismatchError, VerificationError):
            return False



    def __repr__(self):
        return f'<User {self.username}>'