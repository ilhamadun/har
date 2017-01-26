"""Routes"""

from har import app
from har.controller import log as log_controller
from har.controller import status as status_controller
from har.controller import subject as subject_controller


@app.route('/subject/register', methods=['POST'])
def register():
    """POST request to register new subject"""
    return subject_controller.register()


@app.route('/log/upload', methods=['POST'])
def upload_log():
    """POST request to upload log files"""
    return log_controller.upload()

@app.route('/log/download-dataset/<dataset_type>')
def download_dataset(dataset_type):
    """Download activity dataset"""
    return log_controller.download_dataset(dataset_type)

@app.route('/status', methods=['GET'])
def status():
    """GET request to show status page"""
    return status_controller.status()
