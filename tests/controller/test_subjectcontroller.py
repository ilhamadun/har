import hashlib
import pytest

from har import app, db
from har.model import Subject


class TestSubjectController:

    @pytest.fixture
    def setup(self):
        app.config['TESTING'] = True
        db.create_all()
        self.app = app.test_client()

        self.device_data = {
            'user_gender': 'M',
            'user_age': '20',
            'accelerometer': '1',
            'ambient_temperature': '0',
            'gravity': '1',
            'gyroscope': '1',
            'light': '1',
            'linear_accelerometer': '1',
            'magnetic_field': '1',
            'orientation': '1',
            'pressure': '0',
            'proximity': '1',
            'relative_humidity': '0',
            'rotation_vector': '1',
            'temperature': '0'
        }

        yield

        db.drop_all()

    def test_register_device(self, setup):
        response = self.app.post('/subject/register', data=self.device_data)

        assert response.status_code == 201
        assert int(Subject.query.first().user_age) == 20
