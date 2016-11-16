from datetime import datetime
from har import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    type = db.Column(db.String(20))
    number_of_sensor = db.Column(db.Integer)
    total_sensor_axis = db.Column(db.Integer)
    number_of_entry = db.Column(db.Integer)
    path = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime)

    def __init__(self, subject_id, type, number_of_sensor, total_sensor_axis, number_of_entry, path):
        self.subject_id = subject_id
        self.type = type
        self.number_of_sensor = number_of_sensor
        self.total_sensor_axis = total_sensor_axis
        self.number_of_entry = number_of_entry
        self.path = path
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<%s log from subject %i>' % self.type, self.subject
