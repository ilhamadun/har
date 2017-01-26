"""Controller for request to /subject URLs"""

from flask import request, jsonify, render_template
from har.model.subject import create_subject, delete_subject, get_latest
from .url import redirect_back


def overview():
    """Render page for overview of subject"""
    subjects = get_latest(10)
    return render_template('subject.html', subjects=subjects)

def register():
    """Register a new subject

    Returns:
        HTTP response with Content-Type application/json.
    """
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

    device, token = create_subject(user_gender, user_age, sensors)

    response = jsonify(status="Register Success", message="Your device has been registered.",
                       device=device, token=token)

    response.status_code = 201

    return response

def delete(device):
    """Delete subject for given device identifier."""
    delete_subject(device)
    return redirect_back('index')

