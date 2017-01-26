"""Controller for request to /log URLs"""

import os
from flask import request, send_from_directory
from flask.json import jsonify
from har.handler.subject import authenticate
from har.handler import log as log_handler
from har.handler import dataset as dataset_handler
from .url import redirect_back


def upload():
    """Authenticate and handle file upload.

    Returns:
        HTTP response with Content-Type application/json.
    """
    if _authenticate():
        response = _handle_file()
    else:
        response = _authentication_failed_response()

    return response

def _authenticate():
    device = request.form['device']
    token = request.form['token']

    return authenticate(device, token)

def _handle_file():
    file = request.files['file']

    if file.mimetype == 'application/zip':
        log_handler.receive_log(request.form['device'], file)

        response = jsonify(
            status="Upload Success",
            message="Your log files has been stored"
        )
        response.status_code = 201

    else:
        response = jsonify(
            status="Upload Failed",
            message="File corrupted, please reupload the log"
        )
        response.status_code = 400

    return response

def _authentication_failed_response():
    response = jsonify(
        status="Upload Failed",
        message="Authentication Failed"
    )

    response.status_code = 401

    return response

def download_dataset(dataset_type='new'):
    """Serve dataset to download

    Args:
        dataset_type: type of dataset, whether new of all

    Returns:
        Response with dataset attached or error response

    """
    if dataset_type == 'new':
        logs = log_handler.get_pending_logs()
    elif dataset_type == 'all':
        logs = log_handler.get_logs()
    else:
        response = jsonify(
            status="Not Found",
            message="Page not found."
        )
        response.status_code = 404

        return response

    if logs:
        dataset = dataset_handler.get_dataset_from_logs(logs)
        if not dataset:
            dataset = dataset_handler.create_dataset_archive(logs)

        dataset_directory = os.path.join(os.getcwd(), os.path.dirname(dataset.path))
        dataset_name = os.path.basename(dataset.path)
        return send_from_directory(dataset_directory, dataset_name, as_attachment=True)

    else:
        response = jsonify(
            status="Download Failed",
            message="No Logs available to download."
        )
        response.status_code = 400

        return response

def delete(log_id):
    """Delete log for given id"""
    log_handler.delete_log(log_id)
    return redirect_back('index')
