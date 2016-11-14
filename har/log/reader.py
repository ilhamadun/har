import csv
import numpy as np

from os.path import splitext


class LogReader:
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

        self.__count_shape()

    def __count_shape(self):
        with open(self.__file, 'rb') as f:
            reader = csv.reader(f)
            number_of_column = 0
            for row in reader:
                number_of_column = len(row)
                break

            number_of_row = sum(1 for row in reader) + 1
            self.__shape = (number_of_row, number_of_column)

    def shape(self):
        """ Returns the shape of each log item stored in this class

        The shape returned is a tuple containing two elements: number of row and number of column, respectively.

        Keyword arguments:
        item -- log item index
        """
        return self.__shape

    def read(self):
        """ Read csv to numpy array """
        data = np.empty(self.__shape)

        with open(self.__file, 'rb') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                data[r] = np.array(row)

        return data
