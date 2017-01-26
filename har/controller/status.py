"""Controller for request to /status URLs"""

from flask import render_template
from har.model import log, subject

def status():
    """Render Status page

    The status page contains list of subject and log.

    Returns:
        HTTP response with Content-Type text/html.

    """
    subjects = subject.get_latest(5)
    logs = log.get_latest(5)
    return render_template('status.html', subjects=subjects, logs=logs)
