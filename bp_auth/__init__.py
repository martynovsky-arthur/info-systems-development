from flask import Blueprint, render_template, request, session, redirect, url_for
from database.sql_provider import SQLProvider
from model import model_route
import os


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', url_prefix='/auth')

auth_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@bp_auth.route('/', methods=['GET'])
def get_login():
    return render_template('auth_form.html')


@bp_auth.route('/', methods=['POST'])
def post_login():
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('auth_form.html', error='Заполните все поля')

    user_data = {'login': login, 'passwd': password}
    result_info = model_route(auth_provider, 'user_group.sql', user_data)

    if not result_info.status:
        return render_template('auth_form.html', error='Ошибка авторизации')

    user = result_info.result[0]
    session['user_id'] = user['u_id']
    session['user_group'] = user['role']
    return redirect(url_for('main_menu'))
