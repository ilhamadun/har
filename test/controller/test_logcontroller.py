import har
import hashlib
import os
import shutil
import unittest

from log.mocklog import MockLog
from StringIO import StringIO
from har.handler import SubjectHandler
from har.model import Log


class LogTestCase(unittest.TestCase):

    def setUp(self):
        har.app.config['TESTING'] = True
        har.app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads'

        if not os.path.isdir(har.app.config['UPLOAD_FOLDER']):
            os.makedirs(har.app.config['UPLOAD_FOLDER'])

        har.db.create_all()
        self.__create_user('Android Device', 'Device Token')

        self.number_of_csv_files = 3
        self.__mock_file(self.number_of_csv_files)

        self.app = har.app.test_client()

    def __create_user(self, device, token):
        self.device = hashlib.sha1(device).hexdigest()
        self.token = hashlib.sha1(token).hexdigest()
        SubjectHandler().create(self.device, self.token)

    def __mock_file(self, number_of_csv_files):
        mock = MockLog((number_of_csv_files, 100, 6))
        self.log_archive = mock.mock_zip()

    def tearDown(self):
        shutil.rmtree(har.app.config['UPLOAD_FOLDER'])
        har.db.drop_all()

    def test_bad_device_identifier(self):
        device = hashlib.sha1("Bad Device Identifier").hexdigest()
        response = self.app.post('/log/upload', data={'device': device, 'token': 'bad token'})

        self.assertEqual(response.status_code, 401)

    def test_bad_device_token(self):
        response = self.app.post('/log/upload', data={'device': self.device, 'token': 'bad token'})

        self.assertEqual(response.status_code, 401)

    def test_upload_good_file(self):
        with open(self.log_archive, 'rb') as file:
            data = {
                'file': file,
                'device': self.device,
                'token': self.token
            }
            response = self.app.post('/log/upload', data=data)

            self.assertEqual(len(Log.query.all()), self.number_of_csv_files)
            self.assertEqual(Log.query.first().type, 'TRAINING')
            self.assertEqual(response.status_code, 201)

    def test_upload_bad_file(self):
        response = self.app.post('/log/upload', data={'file': (StringIO('bad file content'), 'badfile.txt')})
        self.assertEqual(response.status_code, 400)
