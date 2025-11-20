import os

from database.sql_provider import SQLProvider
from flask import Blueprint, redirect, render_template, request, session, url_for
from model import Model


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', url_prefix='/auth')

auth_model: Model

@bp_auth.record
def on_register(setup_state):
    global auth_model
    app = setup_state.app
    auth_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    auth_model = Model(app.config['db_config'], auth_provider)


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
    result = auth_model.select('user_group.sql', user_data)

    if not result:
        return render_template('auth_form.html', error='Ошибка авторизации')

    user = result[0]
    session['user_id'] = user['u_id']
    session['user_group'] = user['role']
    return redirect(url_for('main_menu'))
