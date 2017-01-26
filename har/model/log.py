from datetime import datetime
from har import db


class Log(db.Model):
    STATUS_PENDING = "pending"
    STATUS_TRAINED = "trained"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.device'))
    log_type = db.Column(db.String(40))
    activity = db.Column(db.String(40))
    sensor_placement = db.Column(db.String(40))
    number_of_sensor = db.Column(db.Integer)
    total_sensor_axis = db.Column(db.Integer)
    number_of_entry = db.Column(db.Integer)
    path = db.Column(db.String(250))
    status = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime)

    def __init__(self, subject_id, log_type, activity, sensor_placement, number_of_sensor,
                 total_sensor_axis, number_of_entry, path):
        self.subject_id = subject_id
        self.log_type = log_type
        self.activity = activity
        self.sensor_placement = sensor_placement
        self.number_of_sensor = number_of_sensor
        self.total_sensor_axis = total_sensor_axis
        self.number_of_entry = number_of_entry
        self.path = path
        self.status = Log.STATUS_PENDING
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<%s log from subject %i>' % self.log_type, self.subject
