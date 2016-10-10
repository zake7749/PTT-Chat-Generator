import os

class FileReader(object):

    def __init__(self):

        pass

    def get_file_list(self, path):

        filenames = [name for name in os.listdir(path) if name[0] != '.')]
        return filenames
