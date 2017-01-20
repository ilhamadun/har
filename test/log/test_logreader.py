import os
import unittest

from .mocklog import MockLog
from har.log import LogReader


class LogReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.log_shape = (10, 6)
        mocklog = MockLog((1,) + self.log_shape)
        self.log_info = ['TRAINING', '2']
        self.log_csv = mocklog.mock_csv(self.log_info, -10, 10)

    def tearDown(self):
        os.remove(self.log_csv)

    def test_invalid_file_format(self):
        with self.assertRaises(IOError):
            LogReader('log.cvs')

    def test_read_log_from_csv(self):
        log = LogReader(self.log_csv)
        self.assert_shape(log)

    def test_read_log_from_list_of_csv(self):
        with self.assertRaises(AttributeError):
            LogReader(['log.cvs'])

    def assert_shape(self, log):
        self.assertEqual(log.shape()[0], self.log_shape[0])
        self.assertEqual(log.shape()[1], self.log_shape[1])

    def test_read(self):
        logs = LogReader(self.log_csv)
        metadata, log = logs.read()

        self.assertEqual(metadata[logs.Metadata.TYPE], self.log_info[0])
        self.assertEqual(metadata[logs.Metadata.NUMBER_OF_SENSOR], self.log_info[1])
        self.assertEquals(log.shape, self.log_shape)

    def test_log_type(self):
        log = LogReader(self.log_csv)

        self.assertTrue(log.log_type(), self.log_info[0])


if __name__ == '__main__':
    unittest.main()
