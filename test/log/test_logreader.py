import os
import unittest

from har.log import LogReader
from log.mocklog import MockLog


class LogReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.log_shape = (10, 6)
        mocklog = MockLog((1,) + self.log_shape)
        self.log_csv = mocklog.mock_csv(-10, 10)

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
        log = logs.read()

        self.assertEquals(log.shape, self.log_shape)


if __name__ == '__main__':
    unittest.main()
