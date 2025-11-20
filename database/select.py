from database.DBcm import DBContextManager
from database.sql_provider import SQLProvider
from flask import current_app

def execute_dict(db_config: dict, _sql: str, params: dict):
    print(f'{__name__ = }: {params = }')

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        cursor.execute(_sql, params)
        result = cursor.fetchall()

    print(f'{__name__ = }: {result = }')

    return result
