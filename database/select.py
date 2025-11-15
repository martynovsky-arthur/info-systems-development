from database.DBcm import DBContextManager
from flask import current_app

def select_list(_sql: str, param_list: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')

        cursor.execute(_sql, param_list)
        result = cursor.fetchall()

        schema = [item[0] for item in cursor.description]

    return (result, schema)


def select_dict(_sql, user_input: dict):
    user_list = list(user_input.values())
    print(f'{user_list = }')

    result_list, schema = select_list(_sql, user_list)
    print(f'{schema = }')

    return [dict(zip(schema, item)) for item in result_list]
