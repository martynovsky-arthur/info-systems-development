# Реализация сценария "меню запросов"

import os

from access import login_required, group_required
from database.sql_provider import SQLProvider
from flask import Blueprint, render_template, request
from model import Model


bp_query = Blueprint('bp_query', __name__, template_folder='templates', url_prefix='/query')

query_model: Model

@bp_query.record
def on_register(setup_state):
    global query_model
    app = setup_state.app
    query_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
    query_model = Model(app.config['db_config'], query_provider)


@bp_query.route('/', methods=['GET'])
@login_required
def query_menu():
    return render_template('query_menu.html')


@bp_query.route('/category', methods=['GET', 'POST'])
@group_required
def get_category():

    if request.method == 'GET':
        return render_template('category_form.html')

    user_input = request.form

    if not user_input.get('prod_category'):
        return render_template('error.html', msg='Не указана категория товаров')

    result = query_model.select('category.sql', user_input)

    return render_template('category_result.html', items=result)
