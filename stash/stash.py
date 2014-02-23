import os
import pickle

import settings as stash_settings


class Stash(object):
    
    def __init__(self, file_name):
        self._file = None
        self._file_name = ""
        self.data = []
        self._build_file_name(file_name)
        self._load_data()
        super(Stash, self).__init__()

    def _build_file_name(self, file_name):
        file_extension = stash_settings.STASH_FILE_EXTENSION
        file_path = stash_settings.STASH_STORAGE_PATH
        self._file_name = "{0}/{1}.{2}".format(file_path, file_name, file_extension)

    def _load_data(self):
        if os.path.exists(self._file_name):
            self._file = open(self._file_name, "r+")
            try:
                self.data = pickle.load(self._file)
            finally:
                self._file.close()
        else:
            self._file = open(self._file_name, "w")
            try:
                pickle.dump(self.data, self._file)
            finally:
                self._file.close()

    def _commit_data(self):
        self._file = open(self._file_name, "r+")
        try:
            pickle.dump(self.data, self._file)
        finally:
            self._file.close()

    def add(self, object_to_add):
        self.data.append(object_to_add)
        self._commit_data()

    def remove(self, index_to_remove):
        self.data.pop(index_to_remove)
        self._commit_data()

    def empty(self):
        self.data = []
        self._commit_data()
