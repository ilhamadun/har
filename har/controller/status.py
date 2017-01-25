from flask import render_template
from har.handler import LogHandler, SubjectHandler

class StatusController:
    def status(self):
        subjects = SubjectHandler().getLatest(5)
        logs = LogHandler().getLatest(5)
        return render_template('status.html', subjects=subjects, logs=logs)
