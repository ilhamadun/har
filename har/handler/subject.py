"""Helper functions to handle the Subject model."""

import random
import hashlib

from datetime import datetime
from sqlalchemy import desc
from flask_bcrypt import generate_password_hash, check_password_hash
from har import db
from har.model import Subject


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
