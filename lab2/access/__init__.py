from functools import wraps

from flask import (
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('in wrapper')
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main_menu'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            access = current_app.config['db_access']
            user_request = request.endpoint.split('.')[0]

            print(f'{request.endpoint = }')
            print(f'{user_request = }')

            user_role = session.get('user_group')
            if user_role in access and user_request in access[user_role]:
                return func(*args, **kwargs)
            else:
                return render_template('error.html', msg='У вас нет прав на эту функциональность')
        return render_template('error.html', msg='Необходимо авторизоваться')
    return wrapper
