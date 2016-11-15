import csv
import numpy as np

from os.path import splitext


class LogReader:
    class Metadata:
        TYPE = 0
        NUMBER_OF_SENSOR = 1
        TOTAL_SENSOR_AXIS = 2
        NUMBER_OF_ENTRY = 3

    def __init__(self, filepath):
        self.__file = None
        self.__shape = None
        self.__open(filepath)

    def __open(self, filepath):
        file_name, file_extension = splitext(filepath)

        if file_extension == '.csv':
            self.__file = filepath

        else:
            raise IOError('File format not supported')

        self.__read_metadata()

    def __read_metadata(self):
        with open(self.__file, 'rb') as f:
            reader = csv.reader(f)
            metadata = reader.next()

            self.__type = metadata[self.Metadata.TYPE]
            self.__shape = (
                int(metadata[self.Metadata.NUMBER_OF_ENTRY]),
                int(metadata[self.Metadata.TOTAL_SENSOR_AXIS])
            )

    def shape(self):
        """ Returns the shape of each log item stored in this class

        The shape returned is a tuple containing two elements: number of row and number of column, respectively.

        Keyword arguments:
        item -- log item index
        """
        return self.__shape

    def read(self):
        """ Read csv to numpy array """
        metadata = []
        data = np.empty(self.__shape)

        with open(self.__file, 'rb') as f:
            reader = csv.reader(f)
            metadata = reader.next()
            for r, row in enumerate(reader):
                data[r] = np.array(row)

        return metadata, data

    def log_type(self):
        return self.__type
