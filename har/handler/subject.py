import random
import hashlib

from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from har import db
from har.model import Subject


class SubjectHandler:
    def create(self, user_gender, user_age, sensors={}):
        device, token = self.__generate_device_and_token()
        token_hash = generate_password_hash(token)
        subject = Subject(device, token_hash, user_gender, user_age, sensors)

        db.session.add(subject)
        db.session.commit()

        return device, token

    def __generate_device_and_token(self):
        now = datetime.now().microsecond
        device = now + random.randint(-6000, 6000)
        token = now + random.randint(-6000, 6000)

        device_hash = hashlib.sha1(str(device).encode()).hexdigest()
        token_hash = hashlib.sha1(str(token).encode()).hexdigest()

        return device_hash, token_hash

    def authenticate(self, device, token):
        subject = Subject.query.filter_by(device=device).first()

        if subject:
            return check_password_hash(subject.token, token)
        else:
            return False

    def get_device(self, id):
        return Subject.query.filter_by(device=id).first()
