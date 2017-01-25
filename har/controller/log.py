"""Controller for request to /log URLs"""

from flask import request
from flask.json import jsonify
from har.handler.subject import authenticate
from har.handler.log import receive_log


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
        receive_log(request.form['device'], file)

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
