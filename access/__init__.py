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
        if not 'user_id' in session:
            return redirect(url_for('bp_auth.get_login'))
        return func(*args, **kwargs)
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_group' in session:
            return redirect(url_for('bp_auth.get_login'))

        access = current_app.config.get('db_access', {})
        user_request = request.endpoint.split('.')[0]

        # print(f'{request.endpoint = }')
        # print(f'{user_request = }')

        user_role = session.get('user_group', '')

        if not user_request in access.get(user_role, []):
            return render_template('error.html', msg='У вас нет прав на эту функциональность')

        return func(*args, **kwargs)

    return wrapper
