from database.DBcm import DBContextManager
from flask import current_app

def select_list(_sql, param_list: list):
    with DBContextManager(current_app.config['db_config']) as cursor: # Отработали инит и ентер
        if cursor is None:                                             # После ентера сюда поом экс
            raise ValueError('Не удалось подключиться')
        else:
            cursor.execute(_sql, param_list)
            result = cursor.fetchall()
            return result                               #Выполнилось все и передали управление экситу
    # [(k0, v0), (k1, v1), (k2, v2)]

def select_dict(_sql, user_input: dict):
    # user_list = []
    # for _, value in user_input:
    #     user_list.append(value)
    # print(f'{user_list = }')
    # result = select_list(_sql, user_list)
    # return result

    return select_list(_sql, user_input.values())
