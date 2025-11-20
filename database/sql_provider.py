import os

class SQLProvider:
    def __init__(self, dir_path):
        self.scripts = {}
        for file in os.listdir(dir_path):
            _sql = open(f'{dir_path}/{file}').read()
            self.scripts[file] = _sql

    def get(self, file):
        print(f'{__name__ = }: {file = }')
        return self.scripts[file]
