from database.DBcm import DBContextManager
from flask import current_app


def select_dict(_sql: str, params: dict):
    print(f'{__name__ = }: {params = }')

    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        cursor.execute(_sql, params)
        result = cursor.fetchall()

    print(f'{__name__ = }: {result = }')

    return result
