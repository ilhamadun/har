from flask_bcrypt import generate_password_hash, check_password_hash

from har import db
from har.model import Subject


class SubjectHandler:
    def create(self, device, token):
        token_hash = generate_password_hash(token)
        subject = Subject(device, token_hash)

        db.session.add(subject)
        db.session.commit()

    def authenticate(self, device, token):
        subject = Subject.query.filter_by(device=device).first()

        if subject:
            return check_password_hash(subject.token, token)
        else:
            return False

    def get_device(self, id):
        return Subject.query.filter_by(device=id).first()
