import os

class SQLProvider:
    def __init__(self, dir_path):
        self.scripts = {}  #Инициализируем словарь
        for file in os.listdir(dir_path):
            _sql = open(f'{dir_path}/{file}').read()  #Проходим по всем файлам директории
            self.scripts[file] = _sql    #Заносим в словарь

    def get(self, file):            #Получаем имя файла
        _sql = self.scripts[file]
        return _sql
