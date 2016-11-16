from har import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(40), unique=True)
    token = db.Column(db.String(60), unique=True)
    logs = db.relationship('Log', backref='subject')

    def __init__(self, device, token):
        self.device = device
        self.token = token

    def __repr__(self):
        return '<Device %s>' % self.device
