import os
import zipfile


class LogExtractor:

    def __init__(self, filepath):
        if os.path.isfile(filepath) is False:
            raise IOError('File not found.')

        self.filepath = filepath

    def name_list(self):
        """ Return a list of file name in the archive """
        name_list = []
        with zipfile.ZipFile(self.filepath) as zip_file:
            name_list = zip_file.namelist()

        return name_list

    def extract(self, name):
        """ Extract a file from the archive

        Keyword arguments:
        name -- file name to extract
        """
        extracted_path = None
        with zipfile.ZipFile(self.filepath) as zip_file:
            extracted_path = zip_file.extract(name)

        return extracted_path

    def extract_all(self):
        """ Extract all file from the archive """
        extract_dir = os.path.dirname(os.path.realpath(self.filepath))
        extracted_path = []
        with zipfile.ZipFile(self.filepath) as zip_file:
            zip_file.extractall(extract_dir)
            extracted_path = zip_file.namelist()

        for i in range(len(extracted_path)):
            extracted_path[i] = extract_dir + '/' + extracted_path[i]

        return extracted_path
