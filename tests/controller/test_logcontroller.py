import hashlib
import os
import shutil
import pytest
from io import StringIO, BytesIO

import har
from har.handler import log
from har.handler.subject import create_subject
from har.model import Log
from tests.log.mocklog import MockLog


class TestLogController:

    @pytest.fixture
    def setup(self):
        har.app.config['TESTING'] = True
        har.app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'test_uploads')
        har.db.drop_all()

        if not os.path.isdir(har.app.config['UPLOAD_FOLDER']):
            os.makedirs(har.app.config['UPLOAD_FOLDER'])

        har.db.create_all()
        self.device, self.token = create_subject('M', 21)

        self.number_of_csv_files = 3
        self.__mock_file(self.number_of_csv_files)

        self.app = har.app.test_client()

        yield

        shutil.rmtree(har.app.config['UPLOAD_FOLDER'])
        har.db.drop_all()

    def __mock_file(self, number_of_csv_files):
        mock = MockLog((number_of_csv_files, 100, 6))
        self.log = mock.mock_csv(['TRAINING#STAND#HANDHELD', '2'], -10, 10)
        self.log_archive = mock.mock_zip(self.log)

    def test_bad_device_identifier(self, setup):
        device = hashlib.sha1("Bad Device Identifier".encode()).hexdigest()
        response = self.app.post('/log/upload', data={'device': device, 'token': 'bad token'})

        assert response.status_code == 401

    def test_bad_device_token(self, setup):
        response = self.app.post('/log/upload', data={'device': self.device, 'token': 'bad token'})

        assert response.status_code == 401

    def __upload_file(self):
        with open(self.log_archive, 'rb') as file:
            data = {
                'file': file,
                'device': self.device,
                'token': self.token
            }
            response = self.app.post('/log/upload', data=data)

        return response

    def test_upload_good_file(self, setup):
        response = self.__upload_file()
        database_entry = Log.query.first() 

        assert len(Log.query.all()) == self.number_of_csv_files
        assert database_entry.log_type == 'training'
        assert database_entry.activity == 'stand'
        assert database_entry.sensor_placement == 'handheld'
        assert response.status_code == 201

        self.assert_log_path(self.device, self.log_archive)

    def assert_log_path(self, device, filepath):
        log_dir = log._generate_log_directory(filepath)
        base_path = os.path.join(har.app.config['UPLOAD_FOLDER'], log_dir)

        logs = log.get_all_log_from_device(device)

        for i, log_file in enumerate(logs):
            log_path = os.path.join(base_path, os.path.basename(self.log[i]))
            assert log_file.path == log_path

    def test_upload_bad_file(self, setup):
        response = self.app.post('/log/upload', data={'file': (BytesIO(b'bad file content'), 'badfile.txt')})
        assert response.status_code == 400

    def test_download_dataset(self, setup):
        self.__upload_file()
        response = self.app.get('/log/download-dataset/new')

        assert response.status_code == 200
        assert response.mimetype == 'application/zip'
