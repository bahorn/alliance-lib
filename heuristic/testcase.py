import json


class TestCase:
    def __init__(self, file):
        self.filename = file
        f = open(file, 'r')
        self._data = json.load(f)
        f.close()

    def data(self):
        return self._data

    def save(self):
        f = open(self.filename, 'w')
        json.dump(self._data, f)
        f.close()

    def add_key(self, key, value):
        self._data[key] = value
