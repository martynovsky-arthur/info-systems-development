from database.DBcm import DBContextManager
from flask import current_app


def select_list(_sql, param_list: list | None = None):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(_sql, param_list)
            return cursor.fetchall()

def select_dict(_sql, user_input: dict | None = None):
    if user_input is None:
        return select_list(_sql)
    return select_list(_sql, list(user_input.values()))
