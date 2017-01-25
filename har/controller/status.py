from flask import render_template
from har.handler import log, SubjectHandler

class StatusController:
    def status(self):
        subjects = SubjectHandler().getLatest(5)
        logs = log.get_latest(5)
        return render_template('status.html', subjects=subjects, logs=logs)
