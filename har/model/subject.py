"""Subject Model"""

import random
import hashlib
from datetime import datetime
from sqlalchemy import desc
from flask_bcrypt import generate_password_hash, check_password_hash
from har import db


class Subject(db.Model):
    """Schema for Subject model."""
    device = db.Column(db.String(40), primary_key=True)
    token = db.Column(db.String(60), unique=True)
    user_gender = db.Column(db.String(1))
    user_age = db.Column(db.Integer)
    accelerometer = db.Column(db.Boolean)
    ambient_temperature = db.Column(db.Boolean)
    gravity = db.Column(db.Boolean)
    gyroscope = db.Column(db.Boolean)
    light = db.Column(db.Boolean)
    linear_accelerometer = db.Column(db.Boolean)
    magnetic_field = db.Column(db.Boolean)
    orientation = db.Column(db.Boolean)
    pressure = db.Column(db.Boolean)
    proximity = db.Column(db.Boolean)
    relative_humidity = db.Column(db.Boolean)
    rotation_vector = db.Column(db.Boolean)
    temperature = db.Column(db.Boolean)
    logs = db.relationship('Log', backref='subject')

    def __init__(self, device, token, user_gender, user_age, sensors):
        self.device = device
        self.token = token
        self.user_gender = user_gender
        self.user_age = user_age
        self.accelerometer = sensors.get('accelerometer', False)
        self.ambient_temperature = sensors.get('ambient_temperature', False)
        self.gravity = sensors.get('gravity', False)
        self.gyroscope = sensors.get('gyroscope', False)
        self.light = sensors.get('light', False)
        self.linear_accelerometer = sensors.get('linear_accelerometer', False)
        self.magnetic_field = sensors.get('magnetic_field', False)
        self.orientation = sensors.get('orientation', False)
        self.pressure = sensors.get('pressure', False)
        self.proximity = sensors.get('proximity', False)
        self.relative_humidity = sensors.get('relative_humidity', False)
        self.rotation_vector = sensors.get('rotation_vector', False)
        self.temperature = sensors.get('temperature', False)

    def __repr__(self):
        return '<Device %s>' % self.device


def create_subject(user_gender, user_age, sensors=None):
    """Create a new subject.

    Args:
        user_gender: The subject's gender.
        user_age: The subject's age.
        sensor: List of available sensor on the subject's device.

    Returns:
        Device identifier and it's authentification token.
    """
    device, token = _generate_device_and_token()
    token_hash = generate_password_hash(token)

    if sensors is None:
        sensors = {}

    subject = Subject(device, token_hash, user_gender, user_age, sensors)

    db.session.add(subject)
    db.session.commit()

    return device, token

def _generate_device_and_token():
    now = datetime.now().microsecond
    device = now + random.randint(-6000, 6000)
    token = now + random.randint(-6000, 6000)

    device_hash = hashlib.sha1(str(device).encode()).hexdigest()
    token_hash = hashlib.sha1(str(token).encode()).hexdigest()

    return device_hash, token_hash

def authenticate(device, token):
    """Authenticate subject

    Args:
        device: Device identifier.
        token: Authentification token.

    Returns:
        Whether the subject is authenticated or not.

    """
    subject = Subject.query.filter_by(device=device).first()

    if subject:
        return check_password_hash(subject.token, token)
    else:
        return False

def get_subject(device):
    """Retreive a device from database.

    Args:
        device: Device identifier

    Returns:
        A single Subject from database with matching device identifier.

    """
    return Subject.query.filter_by(device=device).first()

def get_latest(limit):
    """Get latest Subjects.

    Args:
        limit: Number of Subjects to retreive

    Returns:
        A list of har.model.Subject entry from database.
    """
    return Subject.query.order_by(desc(Subject.device)).limit(limit).all()

def delete_subject(device):
    """Delete subject with given device id.

    Args:
        device: Device identifier

    Returns:
        Whether delete is success or not

    """
    subject = get_subject(device)

    if subject:
        db.session.delete(subject)
        db.session.commit()

        return True

    else:
        return False
