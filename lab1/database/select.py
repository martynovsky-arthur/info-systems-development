from database.DBcm import DBContextManager
from flask import current_app

def select_list(_sql, param_list: list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(_sql, param_list)
            result = cursor.fetchall()
            print(f'{result = }')
            return result

def select_dict(_sql, user_input: dict):
    # user_list = []
    # for _, value in user_input:
    #     user_list.append(value)
    # print(f'{user_list = }')
    # result = select_list(_sql, user_list)
    # return result

    return select_list(_sql, list(user_input.values()))
