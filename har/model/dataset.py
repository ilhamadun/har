"""Dataset Model"""

from datetime import datetime
from har import db


class Dataset(db.Model):
    """Schema for Dataset"""
    id = db.Column(db.Integer, primary_key=True)
    log_start = db.Column(db.Integer)
    log_end = db.Column(db.Integer)
    path = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime)

    def __init__(self, log_start, log_end, path):
        self.log_start = log_start
        self.log_end = log_end
        self.path = path
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<Dataset: %s>' % self.path
