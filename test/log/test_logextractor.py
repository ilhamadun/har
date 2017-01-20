import os
import unittest

from .mocklog import MockLog
from har.log import LogExtractor


class LogExtractorTestCase(unittest.TestCase):

    def setUp(self):
        mocklog = MockLog((5, 10, 6))
        log_info = ['TRAINING', '2']
        self.log = mocklog.mock_csv(log_info, -10, 10)
        self.log_archive = mocklog.mock_zip(self.log)

    def tearDown(self):
        for log in self.log:
            os.remove(log)

        os.remove(self.log_archive)

    def test_open_bad_file(self):
        with self.assertRaises(IOError):
            LogExtractor(os.getcwd() + "/badfile.zip")

    def test_extract_good_file(self):
        extractor = LogExtractor(self.log_archive)
        files = extractor.name_list()

        for i, file in enumerate(files):
            log = extractor.extract(files[i])
            self.assertEqual(log, self.log[i])

    def test_extract_all(self):
        extractor = LogExtractor(self.log_archive)
        files = extractor.extract_all()

        for i, file in enumerate(files):
            self.assertEqual(file, self.log[i])
