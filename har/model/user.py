"""User Model."""

from datetime import datetime
import bcrypt
from flask_login import UserMixin
from har import db

class User(db.Model, UserMixin):
    """Schema for User"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.created_at = datetime.now()

    def __repr__(self):
        return '<user: %s>' % self.email

    def get_id(self):
        return self.id


def create_user(email, password):
    """Create new user

    Args:
        email: user email
        password: user password

    Returns:
        User id

    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(email, hashed)

    db.session.add(user)
    db.session.commit()

    return user.id

def authenticate(email, password):
    """Authenticate user

    Args:
        email: user email
        password: user password

    Returns:
        Whether user is authenticated or not

    """
    user = get_user_by_email(email)

    if user:
        if isinstance(user.password, str):
            clean_password = user.password.encode()
        else:
            clean_password = user.password

        if bcrypt.checkpw(password.encode(), clean_password):
            return True

    return False

def update_last_login(user, time=datetime.now()):
    """Update last login column for a user"""
    user.last_login = time
    db.session.commit()

def get_user_by_email(email):
    """Retreive user by email"""
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """Retreive user by id"""
    return User.query.filter_by(id=user_id).first()
