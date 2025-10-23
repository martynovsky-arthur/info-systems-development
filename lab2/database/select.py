from database.DBcm import DBContextManager
from flask import current_app


def select_list(_sql, param_list: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(_sql, param_list)
            return cursor.fetchall()

def select_dict(_sql, user_input: dict):
    return select_list(_sql, list(user_input.values()))
