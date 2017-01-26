"""Routes"""

from flask import redirect, url_for
from flask_login import login_required
from har import app
from har.controller import log as log_controller
from har.controller import status as status_controller
from har.controller import subject as subject_controller
from har.controller import user as user_controller


@app.route('/')
def index():
    """Home page."""
    return redirect(url_for('status'))

@app.route('/subject')
@login_required
def subject_overview():
    """Subject overview page"""
    return subject_controller.overview()

@app.route('/subject/register', methods=['POST'])
def register():
    """POST request to register new subject"""
    return subject_controller.register()

@app.route('/subject/delete/<device>')
@login_required
def delete_subject(device):
    """Delete subject for given device."""
    return subject_controller.delete(device)

@app.route('/log')
@login_required
def log_overview():
    """Log overview page"""
    return log_controller.overview()

@app.route('/log/upload', methods=['POST'])
def upload_log():
    """POST request to upload log files"""
    return log_controller.upload()

@app.route('/log/download-dataset/<dataset_type>')
def download_dataset(dataset_type):
    """Download activity dataset"""
    return log_controller.download_dataset(dataset_type)

@app.route('/log/delete/<id>')
@login_required
def delete_log(log_id):
    """Delete log for given id."""
    return log_controller.delete(log_id)

@app.route('/status', methods=['GET'])
def status():
    """GET request to show status page"""
    return status_controller.status()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render login page"""
    return user_controller.login()

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    return user_controller.logout()
