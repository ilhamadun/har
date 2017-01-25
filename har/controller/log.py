from flask import request
from flask.json import jsonify
from har.handler import LogHandler, SubjectHandler


class LogController:
    def upload(self):
        if self.__authenticate():
            response = self.__handle_file_and_create_response()
        else:
            response = self.__create_failed_authentication_response()

        return response

    def __authenticate(self):
        device = request.form['device']
        token = request.form['token']

        return SubjectHandler().authenticate(device, token)

    def __handle_file_and_create_response(self):
        f = request.files['file']

        if f.mimetype == 'application/zip':
            LogHandler().receive_log(request.form['device'], f)

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

    def __create_failed_authentication_response(self):
        response = jsonify(
            status="Upload Failed",
            message="Authentication Failed"
        )

        response.status_code = 401

        return response
