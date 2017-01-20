from flask import request, jsonify
from har.handler import SubjectHandler


class SubjectController:
    def register(self):
        user_gender = request.form['user_gender']
        user_age = request.form['user_age']
        sensors = {
            'accelerometer': request.form.get('accelerometer', False),
            'ambient_temperature': request.form.get('ambient_temperature', False),
            'gravity': request.form.get('gravity', False),
            'gyroscope': request.form.get('gyroscope', False),
            'light': request.form.get('light', False),
            'linear_accelerometer': request.form.get('linear_accelerometer', False),
            'magnetic_field': request.form.get('magnetic_field', False),
            'orientation': request.form.get('orientation', False),
            'pressure': request.form.get('pressure', False),
            'proximity': request.form.get('proximity', False),
            'relative_humidity': request.form.get('relative_humidity', False),
            'rotation_vector': request.form.get('rotation_vector', False),
            'temperature': request.form.get('temperature', False)
        }

        device, token = SubjectHandler().create(user_gender, user_age, sensors)

        response = jsonify(status="Register Success", message="Your device has been registered.",
                           device=device, token=token)

        response.status_code = 201

        return response
